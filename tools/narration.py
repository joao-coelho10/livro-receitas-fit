# Narração dos vídeos (português europeu, tom informal e bem-disposto, por "tu").
# Gera um texto por cena do vídeo a partir de recipes.json (mesma ordem de cenas que tools/video/video2.html:
# título, ingredientes, passos..., fecho), sintetiza a voz com edge-tts (pt-PT-RaquelNeural) e mistura-a
# com a música de fundo original (tools/audio/make_music.py), baixando a música enquanto há voz.
# Uso direto:  python3 tools/narration.py <id>        -> mostra o guião da receita
# Usado por:   tools/render_all.py (durações das cenas + faixa de áudio de cada vídeo)
import asyncio, hashlib, json, os, re, subprocess, sys, time
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CACHE = f'{ROOT}/.build/tts'
VOICE = os.environ.get('RF_VOICE', 'pt-PT-RaquelNeural')
RATE = os.environ.get('RF_RATE', '+6%')
PITCH = os.environ.get('RF_PITCH', '+2Hz')
SR = 48000
LEAD, TAIL = 0.35, 0.6          # silêncio antes / depois da fala em cada cena (s)
MUSIC_GAP, MUSIC_DUCK = 0.30, 0.10  # ganho da música sem voz / por baixo da voz

# ------------------------------------------------------------------ texto -> fala
FEM = r'(lata|latas|cebola|cebolas|curgete|curgetes|colher|colheres|pera|peras|dose|doses|fatia|fatias|banana|bananas|maçã|maçãs|tortilha|tortilhas|beringela|beringelas|cenoura|cenouras|clara|claras|batata|batatas|lombo|hora|horas)'
def speak(s):
    s = s.replace('\u00a0', ' ').replace('…', '.')
    s = re.sub(r'\(opcional\)', ', se quiseres', s)
    s = re.sub(r'\s*\(([^)]*)\)', r', \1,', s)
    s = s.replace('°C', ' graus').replace('ºC', ' graus')
    s = re.sub(r'(\d+)\s*[–-]\s*(\d+)', r'\1 a \2', s)
    s = re.sub(r'(^|\s)\+(\d+)', r'\1mais \2', s)
    s = re.sub(r'½\s*c\. sopa', 'meia colher de sopa', s); s = re.sub(r'½\s*c\. chá', 'meia colher de chá', s)
    s = re.sub(r'\b1\s*c\. sopa', 'uma colher de sopa', s); s = re.sub(r'\b1\s*c\. chá', 'uma colher de chá', s)
    s = re.sub(r'\b2\s*c\. sopa', 'duas colheres de sopa', s); s = re.sub(r'\b2\s*c\. chá', 'duas colheres de chá', s)
    s = re.sub(r'(\d+)\s*c\. sopa', r'\1 colheres de sopa', s); s = re.sub(r'(\d+)\s*c\. chá', r'\1 colheres de chá', s)
    s = re.sub(r'\b1\s+' + FEM + r'\b', r'uma \1', s); s = re.sub(r'\b2\s+' + FEM + r'\b', r'duas \1', s)
    s = re.sub(r'\b1\s*kg\b', 'um quilo', s); s = re.sub(r'(\d+)\s*kg\b', r'\1 quilos', s)
    s = re.sub(r'(\d+)\s*g\b', r'\1 gramas', s); s = re.sub(r'(\d+)\s*ml\b', r'\1 mililitros', s)
    s = re.sub(r'(\d+)\s*kcal\b', r'\1 calorias', s); s = re.sub(r'(\d+)\s*min\b', r'\1 minutos', s)
    s = re.sub(r'(\d+)\s*%', r'\1 por cento', s); s = re.sub(r'(\d+)\s*h\b', r'\1 horas', s)
    s = s.replace(' · ', ', ').replace('&', 'e')
    s = re.sub(r'(?i)\bskyr\b', 'squir', s)  # pronúncia: "squir"
    s = re.sub(r'\be e\b', 'e', s)
    s = re.sub(r'\s+([,.!?:])', r'\1', s); s = re.sub(r',\s*,', ',', s); s = re.sub(r',\s*([.!?])', r'\1', s)
    return re.sub(r'\s+', ' ', s).strip()

def lc(s): return s[:1].lower() + s[1:] if s and not s[:2].isupper() else s
def sent(s):
    s = s.strip()
    return s if not s or s[-1] in '.!?' else s + '.'
def join_pt(items):
    items = [i for i in items if i]
    return items[0] if len(items) == 1 else ', '.join(items[:-1]) + ' e ' + items[-1]
def btext(b): return ' '.join(b.get('text', [])).replace(', ', ', ').strip()

def ingr_name(lines):
    s = ' '.join(lines)
    s = re.sub(r'\([^)]*\)', '', s); s = re.sub(r'^(de|do|da|dos|das)\s+', '', s.strip())
    s = re.split(r',| em | às | ao | aos | para | cozid| escorrid| picad| ralad| triturad| descongelad| fresc| sem | com casca', s)[0]
    return s.strip(' ,')

VERBS = set('mistura serve tritura verte arrefece monta prepara espalha molda bate corta recheia junta tempera rega leva polvilha coloca dispõe enrola envolve parte abre finaliza decora deixa passa põe faz cobre acrescenta distribui repousa fatia barra pincela reduz tira volta assa cozinha esmaga mexe liga forra unta enche descansa prova pana calca'.split())
TITLE_FIX = {'Molho de peru': 'faz o molho de peru', 'Manjericão e repouso': 'põe manjericão e deixa repousar'}
CONNECT = ['Agora', 'A seguir', 'Depois', 'Agora']

def script(r):
    """Lista de textos (um por cena), na ordem de video2.html: título, ingredientes, passos, fecho."""
    v = r['video']; m = r['macrosPerServing']; ov = r.get('narr', {})
    out = []
    hook = r.get('hook', '')
    out.append(f"Então, hoje vamos fazer {lc(r.get('short') or r['title'])}! {hook}")
    names = []
    for it in v['ingr']:
        n = ingr_name(it[2])
        if n and n not in names: names.append(n)
    if len(names) > 7: names = names[:6] + ['mais umas coisinhas']
    out.append((f"Para uma dose" if r['servings'] == 1 else f"Para {r['servings']} doses") + f", vais precisar de {join_pt(names)}.")
    k = 0; first = True; steps = v['steps']
    for j, s in enumerate(steps):
        last = j == len(steps) - 1
        con = 'Primeiro' if first else ('Por fim' if last and s['kind'] == 'top' else CONNECT[k % len(CONNECT)])
        first = False
        if s['kind'] == 'preheat':
            t = f"{con}, liga o forno a {s['temp']} graus."
        elif s['kind'] in ('fill', 'top'):
            title = ' '.join(s.get('title', []))
            title = TITLE_FIX.get(title, title)
            first_w = title.split()[0].lower() if title else ''
            if first_w[:1].isdigit(): title = 'serve ' + title
            elif first_w not in VERBS: title = 'junta ' + lc(title)
            auto = first_w not in VERBS and not first_w[:1].isdigit()
            items = []  # frases curtas de cada grupo do passo, juntas numa frase corrida
            for b in s.get('batches', []):
                tx = btext(b).rstrip('.!')
                if not tx: continue
                if b.get('fx') == 'oil' and not re.match(r'(?i)(rega|um fio|azeite)', tx): tx = 'rega com ' + lc(tx)
                elif b.get('fx') == 'oil' and re.match(r'(?i)um fio', tx): tx = 'junta ' + lc(tx)
                elif b.get('fx') == 'spice' and not re.match(r'(?i)tempera', tx): tx = 'tempera com ' + lc(tx)
                tx = tx[:1].lower() + tx[1:] if not tx[:2].isupper() else tx
                if tx.startswith('com ') and items: items[-1] += ' ' + tx
                else: items.append(tx)
            verb = lambda x: x.split()[0].lower() in VERBS or x.split()[0].lower() in ('rega', 'tempera')
            if s['kind'] == 'top' or len(items) <= 1 or (len(items) == 2 and not verb(items[0])):
                if auto and items: parts = [f"{con}, junta {join_pt(items)}."]
                else: parts = [f"{con}, {lc(title)}" + (((' ' if items[0].startswith('com ') else ': ') + join_pt(items)) if items else '') + '.']
            elif verb(items[0]):
                parts = [f"{con}, {lc(title)}."] + [sent(i[:1].upper() + i[1:]) for i in items]
            else:
                mid = ''.join(', depois ' + i for i in items[1:-1])
                parts = [f"{con}, {lc(title)}.", f"Começa por {items[0]}{mid} e, no fim, {items[-1]}."]
            if s.get('mix') and s.get('mixText'): parts.append(sent(' '.join(s['mixText'])))
            if s['kind'] == 'top' and s.get('done'):
                d = re.sub(r'\s*Bom apetite[.!]?', '', s['done']).strip()
                if d: parts.append(sent(d))
            t = ' '.join(parts); k += 1
        elif s['kind'] == 'bake':
            lab = str(s.get('label', s.get('minutes')))
            if lab.startswith('+'): t = f"Volta ao forno mais {lab[1:]} {s.get('sub', 'minutos')}."
            else: t = f"{con}, vai ao forno durante {lab} {s.get('sub', 'minutos')}."
            if s.get('mid'): t += ' ' + sent(re.sub(r'(?i)^mexe a meio do tempo!?$', 'A meio, dá uma mexidela', s['mid']))
            if s.get('after'): t += ' ' + sent(s['after'])
            k += 1
        elif s['kind'] == 'chill':
            lugar = 'congelador' if 'congelador' in ' '.join(s.get('title', [])).lower() else 'frigorífico'
            t = f"{con}, vai ao {lugar} durante {s.get('label', '')} {s.get('sub', 'minutos')}."; k += 1
        else:
            t = sent(' '.join(s.get('title', [])))
        out.append(t)
    out.append(f"Cada dose fica com {m['kcal']} calorias e {m['protein']} gramas de proteína. Bom apetite, e até à próxima!")
    for i, t in ov.items(): out[int(i)] = t
    return [speak(t) for t in out]

# ------------------------------------------------------------------ voz (edge-tts) com cache
def tts(text):
    os.makedirs(CACHE, exist_ok=True)
    h = hashlib.sha1(f'{VOICE}|{RATE}|{PITCH}|{text}'.encode()).hexdigest()[:16]
    mp3 = f'{CACHE}/{h}.mp3'
    if os.path.exists(mp3) and os.path.getsize(mp3) > 1000: return mp3
    exe = os.path.join(os.path.dirname(sys.executable), 'edge-tts')
    cmd = [exe if os.path.exists(exe) else 'edge-tts', '--voice', VOICE, f'--rate={RATE}', f'--pitch={PITCH}', '--text', text, '--write-media', mp3 + '.tmp']
    err = None
    for a in range(30):
        try:  # num processo à parte, com tempo limite: o serviço às vezes fica pendurado
            subprocess.run(cmd, check=True, timeout=45, capture_output=True)
            if os.path.getsize(mp3 + '.tmp') > 1000: os.replace(mp3 + '.tmp', mp3); return mp3
        except Exception as e:
            err = e
        time.sleep(min(3 + a * 2, 30))
    raise RuntimeError(f'edge-tts falhou: {text[:40]}… ({err})')

def decode(path, ch=1):
    import numpy as np
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', str(ch), '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, dtype=np.float32)
    return a.reshape(-1, ch) if ch > 1 else a

def trim(a, thr=0.003):
    import numpy as np
    idx = np.where(np.abs(a) > thr)[0]
    return a[max(0, idx[0] - 240): idx[-1] + 2400] if len(idx) else a

def prepare(r):
    """Sintetiza as falas. Devolve (lista de clips numpy, durações mínimas por cena)."""
    clips = [trim(decode(tts(t))) for t in script(r)]
    return clips, [LEAD + len(c) / SR + TAIL for c in clips]

def mix(clips, scenes, total, out_wav, music=f'{ROOT}/.build/musica-fundo.wav'):
    import numpy as np, wave
    n = int(total * SR) + SR // 2
    voice = np.zeros(n, np.float32); mask = np.zeros(n, np.float32)
    for c, s in zip(clips, scenes):
        a = int((s['S'] + LEAD) * SR); b = min(n, a + len(c))
        voice[a:b] += c[:b - a] * 0.95
        mask[max(0, a - int(.2 * SR)): min(n, b + int(.35 * SR))] = 1
    # envolvente suave (0,25 s) para baixar/subir a música sem saltos
    k = int(.25 * SR); ker = np.ones(k, np.float32) / k
    env = np.convolve(mask, ker, 'same'); env = np.clip(env, 0, 1)
    gain = MUSIC_GAP - (MUSIC_GAP - MUSIC_DUCK) * env
    if not os.path.exists(music):
        subprocess.run([sys.executable, f'{ROOT}/tools/audio/make_music.py', music], check=True)
    mus = decode(music, 2)
    reps = n // len(mus) + 1
    mus = np.tile(mus, (reps, 1))[:n]
    fade = np.ones(n, np.float32); fi = int(.6 * SR); fo = int(2.2 * SR)
    fade[:fi] = np.linspace(0, 1, fi); fade[-fo:] = np.linspace(1, 0, fo)
    st = mus * (gain * fade)[:, None] + voice[:, None]
    st = np.tanh(st * 1.1) / np.tanh(1.1)  # limitador suave
    pcm = (np.clip(st, -1, 1) * 32767).astype('<i2')
    with wave.open(out_wav, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

def mux(video, wav, out):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '48000', '-c:a', 'aac', '-b:a', '96k', '-shortest', '-movflags', '+faststart', out], check=True)

if __name__ == '__main__':
    data = json.load(open(f'{ROOT}/recipes.json'))
    for r in data['recipes']:
        if len(sys.argv) > 1 and r['id'] not in sys.argv[1:]: continue
        print('##', r['id'])
        for i, t in enumerate(script(r)): print(f'  [{i}] {t}')
