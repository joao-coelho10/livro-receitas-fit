# Verifica se cada vídeo tem faixa de áudio com fala: transcreve os primeiros 9 s (faster-whisper)
# e confirma que a frase de abertura "Então, hoje vamos fazer…" lá está.
# Uso: python3 tools/audit_audio.py [ids...]
import json, os, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ids = sys.argv[1:] or sorted(f[:-4] for f in os.listdir(f'{ROOT}/videos') if f.endswith('.mp4'))
m = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=2)
bad = []
def heard(i, secs, beam):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-t', str(secs), '-i', f'{ROOT}/videos/{i}.mp4', '-vn', '-f', 'f32le', '-ac', '1', '-ar', '16000', '-'], capture_output=True).stdout
    a = np.frombuffer(raw, np.float32)
    return ' '.join(s.text for s in m.transcribe(a, language='pt', beam_size=beam, temperature=0)[0]).strip() if len(a) else ''
for i in ids:
    # o whisper às vezes devolve vazio com pouco contexto: 2.ª tentativa com mais segundos e beam maior
    txt = heard(i, 9, 1)
    if 'hoje vamos' not in txt.lower(): txt = heard(i, 14, 5)
    ok = 'hoje vamos' in txt.lower()
    if not ok: bad.append(i)
    print(('OK  ' if ok else 'SEM ') + i + ' | ' + txt[:90], flush=True)
print('FALHAS:', bad)
