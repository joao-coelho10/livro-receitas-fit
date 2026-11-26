# Testes automáticos (Playwright, telemóvel): filtros, isolamento do "Em casa", coleções, barra fixa, vídeos.
# Uso: python3 tests/test_app.py [chromium|webkit ...]   (servidor: python3 -m http.server 8765 na pasta acima de app/)
import json, os, random, sys, time
from playwright.sync_api import sync_playwright
BASE = os.environ.get('BASE', 'http://127.0.0.1:8765/app/')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SHOTS = os.environ.get('SHOTS')  # pasta para capturas (opcional)
DATA = json.load(open(f'{ROOT}/recipes.json'))
R = DATA['recipes']; MEALS = DATA['book']['mealTypes']; PROTS = DATA['book']['proteinTypes']
QUICK = {'rapida': lambda r: r['totalMin'] <= 30, 'saciante': lambda r: r.get('volume'), 'salada': lambda r: r.get('salad'),
         'facil': lambda r: r['difficulty'] == 'Fácil', 'semgluten': lambda r: r['glutenFree'], 'veg': lambda r: r['vegetarian'],
         'prep': lambda r: r['mealPrep'], 'congela': lambda r: r['freezer'], 'barata': lambda r: r['cost'] == '€'}
fails = []; errs = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name, flush=True)
    if not cond: fails.append(name)
def expected(st):
    return [r for r in R if (not st['meal'] or r['meal'] == st['meal']) and (not st['prot'] or r['protein'] == st['prot']) and all(QUICK[k](r) for k in st['quick'])]
def tap_model(st, dim, v):
    st = {'meal': st['meal'], 'prot': st['prot'], 'quick': set(st['quick'])}
    if dim == 'quick': st['quick'] ^= {v}
    else: st[dim] = '' if (v == '' or st[dim] == v) else v
    return st
def ui_state(pg):
    return pg.evaluate("""()=>{const g=(id)=>[...document.querySelectorAll('#'+id+' .chip')].map(c=>[c.dataset.v,c.getAttribute('aria-pressed')==='true',+(c.querySelector('.n')||{textContent:'-1'}).textContent]);
      return {meal:g('chipsMeal'),prot:g('chipsProt'),quick:g('chipsQuick'),count:parseInt(document.querySelector('#count b').textContent),hash:location.hash}}""")
def check(pg, st, label):
    u = ui_state(pg); exp = len(expected(st))
    good = u['count'] == exp
    good &= [v for v, on, _ in u['meal'] if on] == [st['meal']]
    good &= [v for v, on, _ in u['prot'] if on] == [st['prot']]
    good &= set(v for v, on, _ in u['quick'] if on) == st['quick']
    for dim, rows in (('meal', u['meal']), ('prot', u['prot']), ('quick', u['quick'])):
        for v, on, n in rows:
            if dim == 'quick': s2 = dict(st, quick=st['quick'] | {v})
            else: s2 = dict(st, **{dim: v})
            if n != len(expected(s2)): good = False; print('   chip count wrong', dim, v, n, len(expected(s2)))
    if not good: print('   UI', u['count'], 'exp', exp, st)
    return good
def tap(pg, dim, v):
    sel = {'meal': '#chipsMeal', 'prot': '#chipsProt', 'quick': '#chipsQuick'}[dim] + f' .chip[data-v="{v}"]'
    pg.locator(sel).scroll_into_view_if_needed(); pg.locator(sel).tap(); pg.wait_for_timeout(60)

def run(pw, engine):
    if engine == 'webkit':
        dev = pw.devices['iPhone 13']; b = pw.webkit.launch()
        ctx = b.new_context(**dev)
    else:
        b = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    pg = ctx.new_page(); E = engine
    pg.on('console', lambda m: errs.append((E, m.type, m.text)) if m.type in ('error',) else None)
    pg.on('pageerror', lambda e: errs.append((E, 'pageerror', str(e))))
    pg.on('response', lambda r: errs.append((E, 'http', r.status, r.url)) if r.status >= 400 else None)
    pg.goto(BASE); pg.wait_for_selector('.card')
    ok(f'{E}: lista mostra {len(R)} receitas', ui_state(pg)['count'] == len(R))
    # 1) sequências de troques aleatórias (com navegação pelo meio)
    rnd = random.Random(7); st = {'meal': '', 'prot': '', 'quick': set()}; good = True
    opts = [('meal', '')] + [('meal', m) for m in MEALS] + [('prot', '')] + [('prot', p) for p in PROTS] + [('quick', k) for k in QUICK]
    for i in range(70):
        dim, v = rnd.choice(opts)
        if i % 9 == 8:  # sai e volta (abre uma receita e volta atrás / vai ao Em casa e volta pela barra)
            if pg.locator('.card').count():
                pg.locator('.card').first.tap(); pg.wait_for_selector('.r-head'); pg.go_back(); pg.wait_for_selector('#filters')
            else:
                pg.locator('#tabbar a[data-tab="casa"]').tap(); pg.wait_for_selector('[data-food]'); pg.locator('#tabbar a[data-tab="home"]').tap(); pg.wait_for_selector('#filters')
            if not check(pg, st, 'nav'): good = False; print('   after nav', i)
        tap(pg, dim, v); st = tap_model(st, dim, v)
        if not check(pg, st, f'{i}'): good = False; print('   step', i, dim, v)
    ok(f'{E}: 70 toques aleatórios (troca de filtros, estado e contagens corretas)', good)
    # 2) troca direta numa escolha única
    pg.goto(BASE + '#/'); pg.wait_for_selector('#filters'); st = {'meal': '', 'prot': '', 'quick': set()}
    seq = [('meal', 'Snack'), ('meal', 'Pequeno-almoço'), ('meal', 'Pequeno-almoço'), ('prot', 'Frango/Peru'), ('prot', 'Vaca/Porco'), ('prot', ''), ('quick', 'facil'), ('quick', 'semgluten'), ('quick', 'facil'), ('meal', '')]
    good = True
    for dim, v in seq:
        tap(pg, dim, v); st = tap_model(st, dim, v); good &= check(pg, st, '')
    ok(f'{E}: trocar Snack→Pequeno-almoço, Frango→Vaca, Todas, extras', good)
    # 3) endereço e recarregar
    tap(pg, 'meal', 'Snack'); st = tap_model(st, 'meal', 'Snack'); h = pg.evaluate('location.hash')
    pg.reload(); pg.wait_for_selector('#filters')
    ok(f'{E}: estado no endereço sobrevive a recarregar ({h})', check(pg, st, 'reload'))
    # 4) "Limpar filtros"
    pg.locator('#clearAll').tap(); pg.wait_for_timeout(80)
    ok(f'{E}: limpar filtros', check(pg, {'meal': '', 'prot': '', 'quick': set()}, 'clear'))
    # 5) pesquisa + filtro
    pg.fill('#q', 'frango'); pg.wait_for_timeout(100); n1 = ui_state(pg)['count']
    tap(pg, 'meal', 'Snack'); n2 = ui_state(pg)['count']
    expn = len([r for r in expected({'meal': 'Snack', 'prot': '', 'quick': set()}) if 'frango' in json.dumps(r, ensure_ascii=False).lower()])
    ok(f'{E}: pesquisa + filtro combinam ({n1}→{n2})', 0 < n2 <= n1)
    pg.locator('#clearAll').tap(); pg.wait_for_timeout(80)
    # 6) isolamento do Em casa
    before = ui_state(pg)
    pg.locator('#tabbar a[data-tab="casa"]').tap(); pg.wait_for_selector('[data-food]')
    for f in ['frango', 'ovo', 'batata']: pg.locator(f'[data-food="{f}"]').tap()
    pg.locator('#tabbar a[data-tab="home"]').tap(); pg.wait_for_selector('#filters')
    after = ui_state(pg)
    ok(f'{E}: Em casa não mexe na lista de Receitas', after['count'] == before['count'] == len(R) and after['meal'] == before['meal'] and after['quick'] == before['quick'])
    pg.reload(); pg.wait_for_selector('#filters')
    ok(f'{E}: … nem depois de recarregar', ui_state(pg)['count'] == len(R))
    # 6b) página da receita: com vídeo mostra o leitor; sem vídeo ainda mostra o aviso
    live = pg.evaluate("RF.recipes.map(r => [r.id, r.hasVideo])")  # o que a app carregou (os vídeos podem estar a ser gerados)
    for rid_, hv in [x for x in live if x[1]][:1] + [x for x in live if not x[1]][:1]:
        pg.goto(BASE + '#/receita/' + rid_); pg.wait_for_selector('.r-head')
        ok(f"{E}: receita {'com' if hv else 'sem'} vídeo", pg.locator('#vid' if hv else '.video-soon').count() == 1)
    # 7) coleções
    rid = R[0]['id']
    pg.goto(BASE + '#/receita/' + rid); pg.wait_for_selector('.r-head')
    pg.locator('.actions [data-fav]').tap(); pg.locator('.actions [data-cols]').tap(); pg.wait_for_selector('.sheet')
    pg.fill('#newColName', 'Jantares rápidos'); pg.locator('#newColForm button').tap(); pg.wait_for_timeout(150)
    cols = pg.evaluate('RF.cols')
    ok(f'{E}: criar coleção e guardar receita', len(cols) == 2 and rid in cols[1]['ids'] and rid in cols[0]['ids'])
    pg.locator('.sheet [data-close].btn').tap(); pg.wait_for_timeout(300)
    pg.locator('#tabbar a[data-tab="fav"]').tap(); pg.wait_for_selector('#colChips')
    pg.locator('#colChips a.chip').nth(1).tap(); pg.wait_for_selector('#renCol')
    ok(f'{E}: ver coleção', pg.locator('.card').count() == 1)
    if SHOTS and engine == 'chromium': pg.screenshot(path=f'{SHOTS}/v4-colecoes.png')
    pg.locator('#renCol').tap(); pg.fill('#nameInp', 'Jantares'); pg.locator('#nameForm button[type=submit]').tap(); pg.wait_for_timeout(150)
    ok(f'{E}: mudar o nome', pg.evaluate('RF.cols[1].name') == 'Jantares')
    pg.locator('#delCol').tap(); pg.locator('#okBtn').tap(); pg.wait_for_timeout(200)
    ok(f'{E}: apagar coleção (favoritas ficam)', len(pg.evaluate('RF.cols')) == 1 and pg.evaluate('RF.cols[0].ids.length') == 1)
    # 8) barra de baixo sempre no fundo
    pg.goto(BASE + '#/'); pg.wait_for_selector('.card')
    vh = pg.evaluate('innerHeight')
    pos = []
    for y in (0, 3000, 99999):
        pg.evaluate(f"document.querySelector('#main').scrollTop={y}"); pg.wait_for_timeout(100)
        pg.mouse.wheel(0, 800) if engine == 'chromium' else None
        pos.append(pg.evaluate("Math.round(document.querySelector('#tabbar').getBoundingClientRect().bottom)"))
    pg.evaluate('window.scrollTo(0, 500)'); pos.append(pg.evaluate("Math.round(document.querySelector('#tabbar').getBoundingClientRect().bottom)"))
    ok(f'{E}: barra fixa no fundo {pos} (altura {vh})', all(abs(p - vh) <= 1 for p in pos) and pg.evaluate('window.scrollY') == 0)
    b.close()

with sync_playwright() as pw:
    for eng in (sys.argv[1:] or ['chromium', 'webkit']): run(pw, eng)
print('ERROS', len(errs)); [print('  ', e) for e in errs[:15]]
print('FALHAS', fails); sys.exit(1 if fails or errs else 0)
