# Gera a música de fundo original (sintetizada aqui, sem samples externos -> domínio público / CC0).
# Uso: python3 tools/audio/make_music.py [saida.wav]
# Estilo: ukulele dedilhado (Karplus-Strong), baixo suave, marimba, shaker e bombo leves. 104 BPM, Dó maior.
import sys, wave
import numpy as np
SR = 48000; BPM = 104; BEAT = 60 / BPM; BAR = 4 * BEAT
rng = np.random.default_rng(7)
N2F = lambda n: 440.0 * 2 ** ((n - 69) / 12)

def ks(freq, dur, bright=0.5, decay=0.996):
    """Corda dedilhada (Karplus-Strong)."""
    n = int(SR * dur); p = max(2, int(SR / freq))
    buf = rng.uniform(-1, 1, p)
    buf = np.convolve(buf, [bright, 1 - bright], 'same')
    out = np.empty(n); idx = 0
    for i in range(n):
        v = buf[idx]; nxt = buf[(idx + 1) % p]
        buf[idx] = decay * 0.5 * (v + nxt); out[i] = v; idx = (idx + 1) % p
    return out * np.exp(-np.linspace(0, dur * 2.2, n))

def marimba(freq, dur=0.9):
    t = np.arange(int(SR * dur)) / SR
    return (np.sin(2 * np.pi * freq * t) * np.exp(-t * 6) + 0.35 * np.sin(2 * np.pi * freq * 4 * t) * np.exp(-t * 22)) * (1 - np.exp(-t * 400))

def bass(freq, dur):
    t = np.arange(int(SR * dur)) / SR
    s = np.sin(2 * np.pi * freq * t) + 0.25 * np.sin(2 * np.pi * 2 * freq * t)
    return s * np.exp(-t * 3.2) * (1 - np.exp(-t * 300))

def kick(dur=0.25):
    t = np.arange(int(SR * dur)) / SR
    f = 110 * np.exp(-t * 18) + 45
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14)

def shaker(dur=0.09):
    n = int(SR * dur); x = rng.normal(0, 1, n); x = np.diff(np.concatenate([[0], x]))  # agudos
    return x * np.exp(-np.linspace(0, 9, n)) * np.minimum(1, np.linspace(0, 6, n))

def snap(dur=0.12):
    n = int(SR * dur); x = rng.normal(0, 1, n)
    x = np.convolve(x, np.ones(6) / 6, 'same') - np.convolve(x, np.ones(40) / 40, 'same')
    return x * np.exp(-np.linspace(0, 12, n))

CHORDS = {  # voicings de ukulele (G4 C4 E4 A4 reentrante) em MIDI
    'C': [67, 60, 64, 72], 'G': [67, 62, 66 + 1, 71], 'Am': [69, 60, 64, 69], 'F': [69, 60, 65, 69],
    'Dm': [69, 62, 65, 69], 'E7': [68, 62, 64, 71]}
ROOT = {'C': 36, 'G': 43, 'Am': 45, 'F': 41, 'Dm': 38, 'E7': 40}
PROG = ['C', 'G', 'Am', 'F', 'C', 'G', 'F', 'G', 'C', 'G', 'Am', 'F', 'Dm', 'G', 'C', 'C']
STRUM = [(0, 'D'), (1, 'D'), (1.5, 'U'), (2.5, 'U'), (3, 'D'), (3.5, 'U')]  # em tempos
MEL_A = [(0, 76), (0.5, 79), (1.5, 76), (2, 74), (3, 72)]
MEL_B = [(0, 72), (1, 74), (1.5, 76), (2.5, 79), (3, 81)]
MEL_C = [(0, 81), (0.5, 79), (1, 76), (2, 74), (2.5, 76)]

def render():
    total = len(PROG) * BAR
    L = np.zeros(int(SR * (total + 2))); R = np.zeros_like(L)
    def add(sig, t, gl, gr):
        i = int(t * SR); j = min(len(L), i + len(sig)); L[i:j] += sig[:j - i] * gl; R[i:j] += sig[:j - i] * gr
    for b, ch in enumerate(PROG):
        t0 = b * BAR
        for beat, d in STRUM:
            notes = CHORDS[ch] if d == 'D' else CHORDS[ch][::-1]
            acc = 0.75 if beat in (0, 2) else 0.5
            for k, n in enumerate(notes):
                add(ks(N2F(n), 1.1, bright=0.35 if d == 'D' else 0.6) * acc * 0.22, t0 + beat * BEAT + k * 0.012, 0.75, 0.45)
        for beat in (0, 1, 2, 3):
            n = ROOT[ch] + (12 if beat == 3 else 0) + (7 if beat == 2 else 0)
            add(bass(N2F(n), BEAT * 0.95) * 0.32, t0 + beat * BEAT, 0.6, 0.6)
        for beat in (0, 2):
            add(kick() * 0.33, t0 + beat * BEAT, 0.6, 0.6)
        for beat in (1, 3):
            add(snap() * 0.10, t0 + beat * BEAT, 0.5, 0.6)
        for e in range(8):
            add(shaker() * (0.055 if e % 2 else 0.035), t0 + e * BEAT / 2 + (0.012 if e % 2 else 0), 0.35, 0.65)
        mel = MEL_A if b % 4 in (0, 2) else (MEL_B if b % 4 == 1 else MEL_C)
        if b >= 4:
            for beat, n in mel:
                transpose = {'G': -1, 'F': -3, 'Am': 0, 'Dm': -3}.get(ch, 0)
                pent = [60, 62, 64, 67, 69, 72, 74, 76, 79, 81, 84]
                nn = min(pent, key=lambda p: abs(p - (n + transpose)))
                add(marimba(N2F(nn)) * 0.16, t0 + beat * BEAT, 0.4, 0.8)
    n = int(total * SR)
    # cauda do fim volta ao início para o loop não ter costura
    tailL, tailR = L[n:], R[n:]; L, R = L[:n].copy(), R[:n].copy(); L[:len(tailL)] += tailL; R[:len(tailR)] += tailR
    st = np.stack([L, R], 1)
    st /= np.max(np.abs(st)) / 0.8
    return st

def save(path, st):
    pcm = (np.clip(st, -1, 1) * 32767).astype('<i2')
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'musica-fundo.wav'
    st = render(); save(out, st); print(out, round(len(st) / SR, 1), 's')
