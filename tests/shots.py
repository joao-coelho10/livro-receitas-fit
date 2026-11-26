# Capturas v4 (telemóvel): python3 tests/shots.py [chromium|webkit] [dark]
# Precisa do servidor: python3 -m http.server 8765 --bind 127.0.0.1 (na pasta acima de app/)
import sys, json, time
from playwright.sync_api import sync_playwright
BASE = 'http://127.0.0.1:8765/app/'
OUT = '/workspace/livro-receitas/app-screens/'
eng = sys.argv[1] if len(sys.argv) > 1 else 'chromium'; dark = 'dark' in sys.argv
R = json.load(open('recipes.json'))['recipes']
rid = next((r['id'] for r in R[::-1] if r['videoFile'] and r.get('salad')), None) or next(r['id'] for r in R if r['videoFile'])
COLS = [{'id': 'fav', 'name': 'Favoritas', 'ids': [R[0]['id'], R[40]['id'], R[60]['id']]},
        {'id': 'c1', 'name': 'Jantares rápidos', 'ids': [R[60]['id'], R[68]['id'], R[3]['id']]},
        {'id': 'c2', 'name': 'Lanches para o trabalho', 'ids': [R[49]['id'], R[52]['id']]}]
with sync_playwright() as p:
    cs = 'dark' if dark else 'light'
    if eng == 'webkit':
        b = p.webkit.launch(); ctx = b.new_context(**p.devices['iPhone 13'], color_scheme=cs)
    else:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True, color_scheme=cs)
    pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    pg.goto(BASE); pg.wait_for_selector('#filters')
    pg.evaluate("c => { localStorage.setItem('rf-cols', JSON.stringify(c)); localStorage.setItem('rf-casa', JSON.stringify(['frango','ovo','curgete','tomate','cebola','iog_grego','alface'])) }", COLS)
    sfx = f"-{eng}" + ('-dark' if dark else '')
    for name, route, wait in [('lista-filtros', '#/?r=Prato%20principal&f=saciante,salada', '#filters'), ('em-casa', '#/casa', 'main'),
                              ('colecoes', '#/favoritas/c1', 'main'), ('receita', '#/receita/' + rid, '.r-head')]:
        pg.goto(BASE + route); pg.reload(); pg.wait_for_selector(wait); time.sleep(2.5)
        pg.screenshot(path=f'{OUT}v4-{name}{sfx}.png')
    print(eng, 'dark' if dark else 'light', 'erros', errs[:5])
