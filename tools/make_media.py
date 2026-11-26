# Uso: python3 tools/make_media.py [ids...] [--reencode]
# Gera, para cada receita, o poster (media/<id>.jpg) e a miniatura (media/<id>-thumb.webp)
# a partir de videos/<id>.mp4. Com --reencode, volta a comprimir o vídeo (H.264, CRF 26, faststart).
import json, os, subprocess, sys, shutil, tempfile
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ENC = ['-c:v', 'libx264', '-crf', '26', '-preset', 'slow', '-tune', 'animation', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-an']

def run(*a): subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *a], check=True)

def reencode(mp4):
    tmp = tempfile.mktemp(suffix='.mp4'); run('-i', mp4, *ENC, tmp); shutil.move(tmp, mp4)

def media(rid):
    mp4 = f'{ROOT}/videos/{rid}.mp4'
    os.makedirs(f'{ROOT}/media', exist_ok=True)
    # Poster: ecrã de título com doses, kcal e proteína (aos 3 s)
    run('-ss', '3', '-i', mp4, '-frames:v', '1', '-vf', 'scale=960:-2', '-q:v', '4', f'{ROOT}/media/{rid}.jpg')
    # Miniatura quadrada: recorte do tabuleiro/forma (lado direito do ecrã de título)
    run('-ss', '1.2', '-i', mp4, '-frames:v', '1', '-vf', 'crop=600:600:635:60,scale=360:360', '-quality', '78', f'{ROOT}/media/{rid}-thumb.webp')

if __name__ == '__main__':
    data = json.load(open(f'{ROOT}/recipes.json'))
    ids = [a for a in sys.argv[1:] if not a.startswith('--')] or [r['id'] for r in data['recipes']]
    for rid in ids:
        mp4 = f'{ROOT}/videos/{rid}.mp4'
        if not os.path.exists(mp4): print('sem vídeo:', rid); continue
        if '--reencode' in sys.argv: reencode(mp4)
        media(rid)
        print(rid, os.path.getsize(mp4) // 1024, 'KB')
