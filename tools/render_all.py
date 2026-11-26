# Uso: python3 tools/render_all.py [ids...] [--preview]
# Gera o vídeo animado de cada receita (videos/<id>.mp4) a partir de recipes.json,
# desenhando cada fotograma com tools/video/video2.html num Chrome sem janela (Playwright),
# e depois o poster e a miniatura (media/). Sem ids, gera todas as receitas.
# --preview: só tira 2 fotogramas por cena para .frames/<id>/ (para rever rapidamente).
import json, sys, os, subprocess, shutil
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.dirname(__file__))
from make_media import ENC, media
FPS = 30
CHROME = os.environ.get('CHROME')  # ex.: /usr/bin/google-chrome; vazio = Chromium do Playwright
data = json.load(open(f'{ROOT}/recipes.json'))
args = [a for a in sys.argv[1:] if not a.startswith('--')]; preview = '--preview' in sys.argv
recs = [r for r in data['recipes'] if not args or r['id'] in args]

def open_page(p, r):
    kw = {'args': ['--no-sandbox']}
    if CHROME: kw['executable_path'] = CHROME
    b = p.chromium.launch(**kw)
    pg = b.new_page(viewport={'width': 1280, 'height': 720})
    pg.add_init_script('window.RECIPE=' + json.dumps(r, ensure_ascii=False))
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(f'file://{ROOT}/tools/video/video2.html'); pg.evaluate('document.fonts.ready'); pg.evaluate("document.fonts.load('800 20px Inter')")
    if errs: raise RuntimeError(errs)
    return b, pg

def frames(r, chunk, outdir):
    with sync_playwright() as p:
        b, pg = open_page(p, r)
        for name, t in chunk:
            pg.evaluate(f'render({t})'); pg.screenshot(path=f'{outdir}/{name}.png')
        b.close()

for r in recs:
    out = f'{ROOT}/.frames/{r["id"]}'; shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    with sync_playwright() as p:
        b, pg = open_page(p, r); total = pg.evaluate('TOTAL'); scenes = pg.evaluate('SCENES'); b.close()
    if preview:
        ts = []
        for s in scenes: ts += [s['S'] + s['d'] * 0.5, s['S'] + s['d'] - 0.5]
        frames(r, [(f'p{i:02d}', t) for i, t in enumerate(ts)], out)
        print(r['id'], 'preview', len(ts), 'fotogramas em', out); continue
    n = int(total * FPS); idx = [(f'f_{i:05d}', i / FPS) for i in range(n)]; K = 6
    with ThreadPoolExecutor(K) as ex: list(ex.map(lambda c: frames(r, c, out), [idx[k::K] for k in range(K)]))
    os.makedirs(f'{ROOT}/videos', exist_ok=True)
    mp4 = f'{ROOT}/videos/{r["id"]}.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{out}/f_%05d.png', *ENC, mp4], check=True)
    shutil.rmtree(out)
    media(r['id'])
    print(r['id'], round(total, 1), 's', os.path.getsize(mp4) // 1024, 'KB', flush=True)
