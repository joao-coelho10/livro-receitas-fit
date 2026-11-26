# Fonte das receitas: edita aqui e corre `python3 tools/recipes_src.py` para gerar recipes.json com macros recalculados.
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from foods import FOODS, UNIT_G, SPOON_G

def G(q, name, food): return {'q': q, 'u': 'g', 'n': name, 'food': food}
def U(q, sing, plur, food, grams=None): return {'q': q, 'u': 'un', 'n': sing, 'np': plur, 'food': food, 'grams': grams}
def CS(q, name, food): return {'q': q, 'u': 'c. sopa', 'n': name, 'food': food}
def CC(q, name, food): return {'q': q, 'u': 'c. chá', 'n': name, 'food': food}
def T(text): return {'t': text}

# ---------- ícones / formas (para o vídeo) ----------
def sh(shape, c, n=4): return {'k': 'shape', 'shape': shape, 'c': c, 'n': n}
CH = ['#F6DCCB', '#E3A85B']; TU = ['#F3DCCF', '#DDA866']; BEEF = ['#B0585A', '#74412C']; PORK = ['#EFC1B4', '#C98A55']
SAL = ['#F7896B', '#F2A98A']; POT = ['#F2D98A', '#D9A441']; SWEET = ['#F7A540', '#D8701B']; CHK = ['#EAD095', '#C58B38']
WB = ['#F3EBD9', '#E0C9A0']; TOM = ['#E8432F', '#C23422']; BRO = ['#3E8E41', '#2F6E2F']; CAU = ['#F3EBD3', '#D9B26A']
BRU = ['#79B04F', '#55812F']; GB = ['#5DA543', '#3F7F2E']; MUSH = ['#DCC7A8', '#A27B52']; SPIN = ['#3F8F3A', '#2C5F25']
PEPR = ['#E03A2A', '#B02517']; PEPY = ['#F7C531', '#DBA21A']; ONI = ['#B05EAA', '#7C3C7C']; ONW = ['#F1E6D2', '#D9B07A']
CURD = ['#FFFFFF', '#F6E6C8']; PARM = ['#F6E7B0', '#E2B65A']; MOZ = ['#FFF8E6', '#F0C674']; HAM = ['#F2B5B0', '#E39B8C']
TOFU = ['#F2E8D0', '#E2AE4A']; APPLE = ['#F4E6B5', '#D9A85B']; RASP = ['#C8344C', '#A8283E']; BLUE = ['#3B3F78', '#2E3160']
CRUMB = ['#D8B57E', '#B07A3C']; TUNA = ['#D9BC94', '#B98444']; HERB = ['#3E9A4A', '#2F7A38']; LEMON = ['#F7D544', '#E9C030']

RECIPES = [
 dict(id='frango-batata-doce-grao-pimentos', title='Frango com batata-doce, grão e pimentos no forno', short='Frango, batata-doce e grão',
  protein='Frango/Peru', meal='Prato principal', servings=4, handsOn=15, ovenMax=35, oven='30–35 min', temp=210,
  tags=['tabuleiro único', 'sem glúten', 'batata-doce', 'grão'],
  ingredients=[G(600, 'de peito de frango em cubos', 'frango'), G(400, 'de batata-doce em cubos', 'batata_doce'),
   G(240, 'de grão-de-bico escorrido (1 lata)', 'grao'), U(2, 'pimento às tiras', 'pimentos às tiras', 'pimento'),
   U(1, 'cebola roxa às tiras', 'cebolas roxas às tiras', 'cebola'), CS(1, 'de azeite', 'azeite'),
   T('Colorau fumado, alho em pó, cominhos, sal e pimenta a gosto'), G(150, 'de iogurte grego magro com limão e coentros, para servir', 'iog_grego')],
  steps=[('Pré-aquece o forno', 'Liga o forno a 210 °C.'), ('Mistura tudo no tabuleiro', 'Frango, batata-doce, grão, pimentos e cebola, com o azeite e os temperos.'),
   ('Leva ao forno', '30 a 35 minutos, mexendo a meio.'), ('Serve com iogurte', 'Coloca o iogurte grego com limão e coentros por cima.')],
  tip='Corta o frango e a batata-doce em cubos do mesmo tamanho para cozerem por igual.',
  tips=['Se o tabuleiro ficar cheio, usa dois: assim o tabuleiro assa em vez de cozer a vapor.', 'As sobras ficam 3 dias no frigorífico; junta o iogurte só na hora de servir.'],
  pairs=['molho-skyr-alho-ervas', 'crumble-maca-frutos-vermelhos-skyr', 'cheesecake-skyr-forno'],
  video=dict(container='tray', groups=[
    dict(id='a', shape='cube', c=CH, n=30, size=1.05), dict(id='b', shape='cube', c=SWEET, n=26, size=.92), dict(id='c', shape='pea', c=CHK, n=46),
    dict(id='d', shape='strip', c=PEPR, n=9), dict(id='e', shape='strip', c=PEPY, n=8), dict(id='f', shape='arc', c=ONI, n=16),
    dict(id='y', shape='blob', c=CURD, n=5, layout='grid', z=1), dict(id='h', shape='herb', c=HERB, n=34, z=2)],
   ingr=[(sh('cube', CH, 3), '600 g', ['peito de frango em cubos']), ({'k': 'fruit', 'f': 'sweet'}, '400 g', ['batata-doce em cubos']),
    ({'k': 'can', 'c': '#D9A441'}, '1 lata', ['de grão (240 g escorrido)']), ({'k': 'fruit', 'f': 'pepper'}, '2', ['pimentos às tiras']),
    ({'k': 'fruit', 'f': 'onion'}, '1', ['cebola roxa às tiras']), ({'k': 'bottle'}, '1 c. sopa', ['de azeite']),
    ({'k': 'spices'}, 'a gosto', ['colorau fumado, alho em pó,', 'cominhos, sal e pimenta']), ({'k': 'tub', 'c': '#3E8E5A'}, '150 g', ['iogurte grego magro com', 'limão e coentros (para servir)'])],
   steps=[dict(kind='preheat', temp=210, title=['Pré-aquece', 'o forno']),
    dict(kind='fill', target='dish', title=['Mistura tudo', 'no tabuleiro'], batches=[dict(groups=['a', 'b', 'c', 'd', 'e', 'f'], text=['Frango, batata-doce, grão,', 'pimentos e cebola roxa']),
      dict(fx='oil', text=['1 c. sopa de azeite']), dict(fx='spice', text=['Colorau fumado, alho em pó,', 'cominhos, sal e pimenta'])], mix=True, mixText=['Mexe até ficar tudo envolvido']),
    dict(kind='bake', temp=210, minutes=35, label='30–35', sub='minutos', mid='Mexe a meio do tempo!', after='Dourado por fora, tenro por dentro.'),
    dict(kind='top', title=['Serve com', 'iogurte por cima'], batches=[dict(groups=['y'], text=['150 g de iogurte grego magro']), dict(groups=['h'], text=['com limão e coentros'])], done='Pronto! Bom apetite.')])),

 dict(id='almondegas-vaca-feijao-tomate', title='Almôndegas de vaca com feijão branco e tomate no forno', short='Almôndegas de vaca com feijão',
  protein='Vaca/Porco', meal='Prato principal', servings=4, handsOn=20, ovenMax=30, oven='30 min', temp=200,
  tags=['tabuleiro único', 'feijão', 'espinafres', 'comfort food'],
  ingredients=[G(500, 'de carne picada de vaca magra (5% gordura)', 'vaca5'), U(1, 'ovo', 'ovos', 'ovo'), G(30, 'de flocos de aveia', 'aveia'),
   G(400, 'de tomate triturado', 'tomate_lata'), G(240, 'de feijão branco escorrido (1 lata)', 'feijao_branco'), U(1, 'cebola picada', 'cebolas picadas', 'cebola'),
   G(120, 'de espinafres baby', 'espinafres'), G(30, 'de parmesão ralado', 'parmesao'), T('Alho, orégãos, sal e pimenta a gosto')],
  steps=[('Pré-aquece o forno', 'Liga o forno a 200 °C.'), ('Faz as almôndegas', 'Mistura a carne com o ovo, a aveia, alho e sal, e molda 16 bolas.'),
   ('Monta o tabuleiro', 'Tomate, feijão e cebola no fundo, com orégãos; as almôndegas por cima.'), ('Leva ao forno', '25 minutos.'),
   ('Junta espinafres e parmesão', 'Espalha por cima e deixa mais 5 minutos.')],
  tip='Molha as mãos em água fria antes de moldar: as almôndegas ficam lisas e não se desfazem.',
  tips=['Para mais proteína, troca metade do feijão por mais 150 g de carne.', 'Congela bem em porções, já com o molho.'],
  pairs=['pao-proteico-cottage-aveia', 'cheesecake-skyr-forno'],
  video=dict(container='tray', groups=[
    dict(id='t', shape='layer', c=['#C8402E', '#A8321F']), dict(id='w', shape='bean', c=WB, n=40), dict(id='o', shape='arc', c=ONW, n=12, size=.8),
    dict(id='m', shape='ball', c=BEEF, n=16, layout='grid', size=1.5, z=1), dict(id='s', shape='leaf', c=SPIN, n=26, z=2), dict(id='p', shape='shred', c=PARM, n=40, z=3)],
   ingr=[({'k': 'meat', 'c': '#B5474A'}, '500 g', ['carne picada de vaca', 'magra (5% gordura)']), ({'k': 'eggs'}, '1', ['ovo']),
    ({'k': 'sack', 'c': '#C9A26B'}, '30 g', ['de flocos de aveia']), ({'k': 'can', 'c': '#C8402E'}, '400 g', ['de tomate triturado']),
    ({'k': 'can', 'c': '#E0C9A0'}, '1 lata', ['de feijão branco escorrido']), ({'k': 'fruit', 'f': 'onionw'}, '1', ['cebola picada']),
    (sh('leaf', SPIN, 4), '120 g', ['de espinafres baby']), ({'k': 'cheese'}, '30 g', ['de parmesão ralado'])],
   steps=[dict(kind='preheat', temp=200, title=['Pré-aquece', 'o forno']),
    dict(kind='fill', target='dish', title=['Monta o', 'tabuleiro'], batches=[dict(groups=['t'], text=['Tomate triturado no fundo']), dict(groups=['w', 'o'], text=['Feijão branco e cebola']),
      dict(fx='spice', text=['Alho, orégãos, sal e pimenta']), dict(groups=['m'], text=['16 almôndegas por cima'])]),
    dict(kind='bake', temp=200, minutes=25, label='25', sub='minutos', after='O molho borbulha à volta.'),
    dict(kind='top', title=['Espinafres', 'e parmesão'], batches=[dict(groups=['s'], text=['120 g de espinafres baby']), dict(groups=['p'], text=['30 g de parmesão ralado'])], done='Mais 5 min no forno e está pronto!')])),

 dict(id='lombo-porco-batata-couves', title='Lombo de porco com batata e couves-de-bruxelas no tabuleiro', short='Lombo de porco com batata',
  protein='Vaca/Porco', meal='Prato principal', servings=4, handsOn=15, ovenMax=35, oven='35 min', temp=200,
  tags=['tabuleiro único', 'batata', 'mostarda', 'sem glúten'],
  ingredients=[G(600, 'de lombo de porco em medalhões', 'porco_lombo'), G(500, 'de batata em gomos', 'batata'), G(400, 'de couves-de-bruxelas cortadas ao meio', 'couve_bruxelas'),
   U(1, 'cebola em gomos', 'cebolas em gomos', 'cebola'), CS(1, 'de azeite', 'azeite'), CS(1, 'de mostarda', 'mostarda'), T('Alho, alecrim, colorau, sal e pimenta a gosto')],
  steps=[('Pré-aquece o forno', 'Liga o forno a 200 °C.'), ('Batata e couves primeiro', 'Tempera com metade do azeite, alho, alecrim, sal e pimenta; 15 minutos no forno.'),
   ('Junta o porco', 'Pincela os medalhões com a mostarda, o resto do azeite e o colorau, e coloca-os no tabuleiro.'), ('Mais 20 minutos', 'Até o porco ficar dourado e a batata estaladiça.'),
   ('Descansa e serve', 'Deixa repousar 5 minutos antes de servir.')],
  tip='Não passes o lombo: retira-o quando o centro ainda estiver ligeiramente rosado (63 °C), fica muito mais suculento.',
  tips=['Fica ótimo com o molho de quark e pimento assado.', 'Troca as couves por brócolos ou feijão-verde se preferires.'],
  pairs=['molho-quark-pimento-assado', 'molho-skyr-alho-ervas', 'crumble-maca-frutos-vermelhos-skyr'],
  video=dict(container='tray', groups=[
    dict(id='p', shape='wedge', c=POT, n=22), dict(id='b', shape='ball', c=BRU, n=24, size=.75), dict(id='o', shape='arc', c=ONW, n=12),
    dict(id='m', shape='medallion', c=PORK, n=8, layout='grid', z=1), dict(id='h', shape='herb', c=HERB, n=20, z=2)],
   ingr=[({'k': 'meat', 'c': '#EFC1B4'}, '600 g', ['lombo de porco em medalhões']), ({'k': 'fruit', 'f': 'potato'}, '500 g', ['de batata em gomos']),
    (sh('ball', BRU, 4), '400 g', ['de couves-de-bruxelas']), ({'k': 'fruit', 'f': 'onionw'}, '1', ['cebola em gomos']), ({'k': 'bottle'}, '1 c. sopa', ['de azeite']),
    ({'k': 'jar', 'c': '#E5B62E'}, '1 c. sopa', ['de mostarda']), ({'k': 'spices'}, 'a gosto', ['alho, alecrim, colorau,', 'sal e pimenta'])],
   steps=[dict(kind='preheat', temp=200, title=['Pré-aquece', 'o forno']),
    dict(kind='fill', target='dish', title=['Batata e couves', 'primeiro'], batches=[dict(groups=['p', 'b', 'o'], text=['Batata, couves e cebola']), dict(fx='oil', text=['Metade do azeite']), dict(fx='spice', text=['Alho, alecrim, sal e pimenta'])], mix=True, mixText=['Mexe e leva 15 min ao forno']),
    dict(kind='bake', temp=200, minutes=15, label='15', sub='minutos', cookTo=.45, after='Começa a dourar.'),
    dict(kind='fill', target='dish', title=['Junta o porco'], batches=[dict(groups=['m'], text=['Medalhões com mostarda,', 'azeite e colorau'])]),
    dict(kind='bake', temp=200, minutes=20, label='+20', sub='minutos', cookTo=.95, after='Dourado e suculento.'),
    dict(kind='top', title=['Descansa', 'e serve'], batches=[dict(groups=['h'], text=['5 minutos de repouso'])], done='Pronto! Bom apetite.')])),

 dict(id='peru-batata-cogumelos-feijao-verde', title='Peru com batata, cogumelos e feijão-verde no forno', short='Peru com batata e cogumelos',
  protein='Frango/Peru', meal='Prato principal', servings=4, handsOn=15, ovenMax=30, oven='30 min', temp=210,
  tags=['tabuleiro único', 'limão', 'cogumelos', 'sem glúten'],
  ingredients=[G(600, 'de peito de peru em cubos', 'peru'), G(450, 'de batata em cubos pequenos', 'batata'), G(250, 'de cogumelos laminados', 'cogumelos'),
   G(250, 'de feijão-verde', 'feijao_verde'), CS(1, 'de azeite', 'azeite'), CS(2, 'de sumo de limão, mais a raspa', 'limao'), T('Alho, tomilho, sal e pimenta a gosto')],
  steps=[('Pré-aquece o forno', 'Liga o forno a 210 °C.'), ('Tudo no tabuleiro', 'Peru, batata, cogumelos e feijão-verde, com o azeite, alho, tomilho, sal e pimenta.'),
   ('Leva ao forno', '30 minutos, mexendo a meio.'), ('Finaliza com limão', 'Rega com o sumo e a raspa de limão antes de servir.')],
  tip='Corta a batata em cubos pequenos (1,5 cm): assim fica pronta ao mesmo tempo que o peru.',
  tips=['O molho de skyr com alho e ervas fica perfeito por cima.', 'O peito de peru seca depressa: não passes dos 30 minutos.'],
  pairs=['molho-skyr-alho-ervas', 'molho-quark-pimento-assado', 'cheesecake-skyr-forno'],
  video=dict(container='tray', groups=[
    dict(id='a', shape='cube', c=TU, n=28, size=1.05), dict(id='p', shape='cube', c=POT, n=26, size=.8), dict(id='m', shape='mushroom', c=MUSH, n=18),
    dict(id='g', shape='greenbean', c=GB, n=20), dict(id='l', shape='lemon', c=LEMON, n=4, layout='grid', z=1), dict(id='h', shape='herb', c=HERB, n=22, z=2)],
   ingr=[(sh('cube', TU, 3), '600 g', ['peito de peru em cubos']), ({'k': 'fruit', 'f': 'potato'}, '450 g', ['de batata em cubos']),
    (sh('mushroom', MUSH, 3), '250 g', ['de cogumelos laminados']), (sh('greenbean', GB, 4), '250 g', ['de feijão-verde']), ({'k': 'bottle'}, '1 c. sopa', ['de azeite']),
    ({'k': 'fruit', 'f': 'lemon'}, '2 c. sopa', ['de sumo de limão e raspa']), ({'k': 'spices'}, 'a gosto', ['alho, tomilho, sal e pimenta'])],
   steps=[dict(kind='preheat', temp=210, title=['Pré-aquece', 'o forno']),
    dict(kind='fill', target='dish', title=['Tudo no', 'tabuleiro'], batches=[dict(groups=['a', 'p'], text=['Peru e batata']), dict(groups=['m', 'g'], text=['Cogumelos e feijão-verde']), dict(fx='oil', text=['1 c. sopa de azeite']), dict(fx='spice', text=['Alho, tomilho, sal e pimenta'])], mix=True, mixText=['Mexe bem']),
    dict(kind='bake', temp=210, minutes=30, label='30', sub='minutos', mid='Mexe a meio do tempo!', after='Batata dourada, peru suculento.'),
    dict(kind='top', title=['Finaliza', 'com limão'], batches=[dict(groups=['l'], text=['Sumo e raspa de limão']), dict(groups=['h'], text=['Tomilho fresco'])], done='Pronto! Bom apetite.')])),

 dict(id='ovos-forno-tomate-grao-cottage', title='Ovos no forno com tomate, grão e cottage (shakshuka)', short='Shakshuka de forno com cottage',
  protein='Ovos/Queijo', meal='Prato principal', servings=4, handsOn=10, ovenMax=25, oven='25 min', temp=200,
  tags=['vegetariano', 'cottage', 'grão', 'jantar rápido'],
  ingredients=[U(8, 'ovo', 'ovos', 'ovo'), G(400, 'de tomate triturado', 'tomate_lata'), G(240, 'de grão-de-bico escorrido (1 lata)', 'grao'),
   U(1, 'pimento vermelho em cubos', 'pimentos vermelhos em cubos', 'pimento'), U(1, 'cebola picada', 'cebolas picadas', 'cebola'), G(200, 'de queijo cottage', 'cottage'),
   {'q': 0.5, 'u': 'c. sopa', 'n': 'de azeite', 'food': 'azeite'}, T('Cominhos, colorau fumado, coentros, sal e pimenta a gosto')],
  steps=[('Pré-aquece o forno', 'Liga o forno a 200 °C.'), ('Faz o molho no tabuleiro', 'Tomate, grão, pimento, cebola, azeite e temperos numa travessa; 15 minutos no forno.'),
   ('Junta os ovos', 'Abre 8 covas no molho e parte um ovo em cada.'), ('Forno até as claras firmarem', '8 a 10 minutos, com as gemas ainda cremosas.'),
   ('Cottage e coentros', 'Põe colheradas de cottage e coentros por cima e serve.')],
  tip='Tira do forno quando as claras estiverem brancas mas as gemas ainda tremerem: acabam de cozer fora do forno.',
  tips=['Serve com uma fatia de pão proteico de cottage para molhar no molho.', 'Para mais proteína, troca 2 ovos por 150 g de claras à volta.'],
  pairs=['pao-proteico-cottage-aveia', 'crumble-maca-frutos-vermelhos-skyr'],
  video=dict(container='round', groups=[
    dict(id='t', shape='layer', c=['#C8402E', '#A8321F']), dict(id='c', shape='pea', c=CHK, n=36), dict(id='r', shape='cube', c=PEPR, n=20, size=.55), dict(id='o', shape='arc', c=ONW, n=10, size=.7),
    dict(id='e', shape='egg', c=['#FFFFFF', '#FFF6E6'], n=8, layout='grid', z=1), dict(id='q', shape='curd', c=CURD, n=9, z=2), dict(id='h', shape='herb', c=HERB, n=26, z=3)],
   ingr=[({'k': 'eggs'}, '8', ['ovos']), ({'k': 'can', 'c': '#C8402E'}, '400 g', ['de tomate triturado']), ({'k': 'can', 'c': '#D9A441'}, '1 lata', ['de grão (240 g escorrido)']),
    ({'k': 'fruit', 'f': 'pepper'}, '1', ['pimento vermelho em cubos']), ({'k': 'fruit', 'f': 'onionw'}, '1', ['cebola picada']), ({'k': 'tub', 'c': '#2F80C0'}, '200 g', ['de queijo cottage']),
    ({'k': 'bottle'}, '½ c. sopa', ['de azeite']), ({'k': 'spices'}, 'a gosto', ['cominhos, colorau fumado,', 'coentros, sal e pimenta'])],
   steps=[dict(kind='preheat', temp=200, title=['Pré-aquece', 'o forno']),
    dict(kind='fill', target='dish', title=['Faz o molho', 'na travessa'], batches=[dict(groups=['t'], text=['Tomate triturado']), dict(groups=['c', 'r', 'o'], text=['Grão, pimento e cebola']), dict(fx='spice', text=['Cominhos, colorau, sal e azeite'])]),
    dict(kind='bake', temp=200, minutes=15, label='15', sub='minutos', cookTo=.3, after='O molho apura.'),
    dict(kind='fill', target='dish', title=['Junta os ovos'], batches=[dict(groups=['e'], text=['Abre 8 covas e parte', 'um ovo em cada'])]),
    dict(kind='bake', temp=200, minutes=10, label='8–10', sub='minutos', cookTo=.55, after='Claras firmes, gemas cremosas.'),
    dict(kind='top', title=['Cottage', 'e coentros'], batches=[dict(groups=['q'], text=['200 g de queijo cottage']), dict(groups=['h'], text=['Coentros frescos'])], done='Pronto! Bom apetite.')])),

 dict(id='caril-grao-couve-flor-tofu', title='Caril de grão, couve-flor e tofu no forno', short='Caril de grão e couve-flor',
  protein='Vegetariano/Leguminosas', meal='Prato principal', servings=4, handsOn=15, ovenMax=30, oven='30 min', temp=210,
  tags=['vegetariano', 'leguminosas', 'caril', 'skyr'],
  ingredients=[G(600, 'de couve-flor em floretes', 'couve_flor'), G(480, 'de grão-de-bico escorrido (2 latas)', 'grao'), G(300, 'de tofu firme em cubos', 'tofu'),
   G(250, 'de tomate cherry', 'tomate_cherry'), U(1, 'cebola roxa em gomos', 'cebolas roxas em gomos', 'cebola'), CS(1, 'de azeite', 'azeite'), CC(2, 'de caril em pó', 'caril'),
   G(200, 'de skyr natural com limão e coentros, para servir', 'skyr'), T('Sal, alho em pó e pimenta a gosto')],
  steps=[('Pré-aquece o forno', 'Liga o forno a 210 °C.'), ('Tempera tudo no tabuleiro', 'Couve-flor, grão, tofu, tomate e cebola com o azeite, o caril, alho e sal.'),
   ('Leva ao forno', '30 minutos, mexendo a meio.'), ('Serve com skyr', 'Por cima, skyr com sumo de limão e coentros.')],
  tip='Seca bem o tofu com papel de cozinha antes de cortar: fica dourado e firme em vez de mole.',
  tips=['O tofu é soja, uma leguminosa: é o que leva este prato a quase 30 g de proteína por dose.', 'Se não gostares de tofu, usa 250 g de queijo cottage por cima no fim.'],
  pairs=['pao-proteico-cottage-aveia', 'crumble-maca-frutos-vermelhos-skyr'],
  video=dict(container='tray', groups=[
    dict(id='f', shape='floret', c=['#F3EBD3', '#E0A83A'], n=18), dict(id='c', shape='pea', c=['#EAD095', '#D99A2E'], n=44), dict(id='t', shape='cube', c=TOFU, n=20, size=.9),
    dict(id='r', shape='ball', c=TOM, n=14, size=.7), dict(id='o', shape='arc', c=ONI, n=12), dict(id='y', shape='blob', c=CURD, n=4, layout='grid', z=1), dict(id='h', shape='herb', c=HERB, n=28, z=2)],
   ingr=[(sh('floret', CAU, 3), '600 g', ['de couve-flor em floretes']), ({'k': 'can', 'c': '#D9A441'}, '2 latas', ['de grão (480 g escorrido)']), (sh('cube', TOFU, 3), '300 g', ['de tofu firme em cubos']),
    (sh('ball', TOM, 4), '250 g', ['de tomate cherry']), ({'k': 'fruit', 'f': 'onion'}, '1', ['cebola roxa em gomos']), ({'k': 'bottle'}, '1 c. sopa', ['de azeite']),
    ({'k': 'spices', 'c': ['#E0A42A', '#F3E3C3', '#C9852F']}, '2 c. chá', ['de caril em pó']), ({'k': 'tub', 'c': '#5B7BA8'}, '200 g', ['de skyr com limão', 'e coentros (para servir)'])],
   steps=[dict(kind='preheat', temp=210, title=['Pré-aquece', 'o forno']),
    dict(kind='fill', target='dish', title=['Tempera tudo', 'no tabuleiro'], batches=[dict(groups=['f', 'c'], text=['Couve-flor e grão']), dict(groups=['t', 'r', 'o'], text=['Tofu, tomate e cebola']), dict(fx='oil', text=['1 c. sopa de azeite']), dict(fx='spice', text=['Caril, alho e sal'], spice=['#E0A42A', '#F3C14A', '#C9852F', '#FFF4DE'])], mix=True, mixText=['Mexe até ficar tudo amarelo']),
    dict(kind='bake', temp=210, minutes=30, label='30', sub='minutos', mid='Mexe a meio do tempo!', after='Couve-flor tostada nas pontas.'),
    dict(kind='top', title=['Serve', 'com skyr'], batches=[dict(groups=['y'], text=['200 g de skyr com limão']), dict(groups=['h'], text=['e coentros frescos'])], done='Pronto! Bom apetite.')])),

 dict(id='salmao-batata-brocolos', title='Salmão com batata e brócolos no tabuleiro', short='Salmão com batata e brócolos',
  protein='Peixe', meal='Prato principal', servings=4, handsOn=10, ovenMax=35, oven='32–35 min', temp=200,
  tags=['tabuleiro único', 'ómega-3', 'limão', 'sem glúten'],
  ingredients=[G(500, 'de lombos de salmão sem pele', 'salmao'), G(500, 'de batata em rodelas finas', 'batata'), G(400, 'de brócolos em floretes', 'brocolos'),
   U(1, 'limão às rodelas', 'limões às rodelas', 'limao', grams=30), {'q': 0.5, 'u': 'c. sopa', 'n': 'de azeite', 'food': 'azeite'}, T('Alho, endro, sal e pimenta a gosto')],
  steps=[('Pré-aquece o forno', 'Liga o forno a 200 °C.'), ('Batata primeiro', 'Rodelas de batata com o azeite, alho e sal; 20 minutos no forno.'),
   ('Junta brócolos e salmão', 'Brócolos à volta, salmão no meio, com rodelas de limão, endro, sal e pimenta.'), ('Mais 12 a 15 minutos', 'Até o salmão lascar facilmente com um garfo.'),
   ('Serve com molho de skyr', 'Uma colherada de molho de skyr com alho e ervas por cima.')],
  tip='O salmão está no ponto quando o centro fica rosa-opaco e lasca com o garfo; mais tempo seca-o.',
  tips=['Podes trocar o salmão por lombos de atum fresco (8 a 10 minutos).', 'O salmão tem mais gordura, mas é gordura boa (ómega-3); as calorias já contam com isso.'],
  pairs=['molho-skyr-alho-ervas', 'cheesecake-skyr-forno'],
  video=dict(container='tray', groups=[
    dict(id='p', shape='slice', c=POT, n=26), dict(id='b', shape='floret', c=BRO, n=16, z=0), dict(id='s', shape='fillet', c=SAL, n=4, layout='grid', z=1),
    dict(id='l', shape='lemon', c=LEMON, n=4, layout='grid', z=2), dict(id='h', shape='herb', c=HERB, n=22, z=3), dict(id='y', shape='blob', c=CURD, n=4, layout='grid', z=4)],
   ingr=[({'k': 'fish'}, '500 g', ['de lombos de salmão']), ({'k': 'fruit', 'f': 'potato'}, '500 g', ['de batata em rodelas finas']), (sh('floret', BRO, 3), '400 g', ['de brócolos em floretes']),
    ({'k': 'fruit', 'f': 'lemon'}, '1', ['limão às rodelas']), ({'k': 'bottle'}, '½ c. sopa', ['de azeite']), ({'k': 'spices'}, 'a gosto', ['alho, endro, sal e pimenta'])],
   steps=[dict(kind='preheat', temp=200, title=['Pré-aquece', 'o forno']),
    dict(kind='fill', target='dish', title=['Batata', 'primeiro'], batches=[dict(groups=['p'], text=['Rodelas finas de batata']), dict(fx='oil', text=['Azeite, alho e sal'])]),
    dict(kind='bake', temp=200, minutes=20, label='20', sub='minutos', cookTo=.5, after='A batata começa a dourar.'),
    dict(kind='fill', target='dish', title=['Brócolos', 'e salmão'], batches=[dict(groups=['b'], text=['Brócolos à volta']), dict(groups=['s'], text=['Salmão no meio']), dict(groups=['l', 'h'], text=['Limão, endro, sal e pimenta'])]),
    dict(kind='bake', temp=200, minutes=15, label='12–15', sub='minutos', cookTo=.85, after='O salmão lasca com o garfo.'),
    dict(kind='top', title=['Serve com', 'molho de skyr'], batches=[dict(groups=['y'], text=['Molho de skyr, alho e ervas'])], done='Pronto! Bom apetite.')])),

 dict(id='pao-proteico-cottage-aveia', title='Pão proteico de cottage e aveia', short='Pão proteico de cottage',
  protein='Ovos/Queijo', meal='Acompanhamento/Pão', servings=6, handsOn=10, ovenMax=30, oven='30 min', temp=180,
  tags=['pão', 'cottage', 'sem farinha de trigo', 'congela bem'],
  ingredients=[G(250, 'de queijo cottage', 'cottage'), U(3, 'ovo', 'ovos', 'ovo'), G(80, 'de flocos de aveia', 'aveia'), CC(1, 'de fermento em pó', 'fermento'),
   T('Sal, orégãos e sementes de sésamo a gosto (opcional)')],
  steps=[('Pré-aquece o forno', 'Liga o forno a 180 °C e forra uma forma de bolo inglês com papel vegetal.'), ('Tritura tudo', 'Cottage, ovos, aveia, fermento e sal na liquidificadora, até ficar uma massa lisa.'),
   ('Verte na forma', 'Alisa e espalha sementes por cima, se quiseres.'), ('Leva ao forno', '30 minutos, até dourar e um palito sair seco.'), ('Arrefece e fatia', 'Espera 10 minutos antes de cortar em 6 fatias.')],
  tip='Deixa arrefecer antes de fatiar: quente, o miolo ainda está húmido e esfarela.',
  tips=['Torrado fica estaladiço: ótimo com ovos, atum ou com o molho de quark e pimento.', 'Guarda no frigorífico 4 dias, ou congela às fatias.', 'Alternativa: wraps de claras (2 claras + 1 c. sopa de aveia numa frigideira).'],
  pairs=[],
  video=dict(container='loaf', groups=[
    dict(id='q', shape='curd', c=CURD, n=10, inn='bowl'), dict(id='e', shape='yolk', c=['#F7B32B', '#F7B32B'], n=3, inn='bowl', layout='grid'), dict(id='a', shape='pea', c=['#E6D2A8', '#E6D2A8'], n=40, inn='bowl', size=.55),
    dict(id='B', shape='layer', c=['#F1E4C4', '#F1E4C4'], inn='bowl', reveal='mix'), dict(id='L', shape='layer', c=['#EBD9B4', '#B9773A']), dict(id='s', shape='pea', c=['#F3EAD6', '#D9B377'], n=36, size=.3, z=1), dict(id='k', shape='slicelines', c=['#8F5A26', '#8F5A26'], n=5, layout='grid', z=2)],
   ingr=[({'k': 'tub', 'c': '#2F80C0'}, '250 g', ['de queijo cottage']), ({'k': 'eggs'}, '3', ['ovos']), ({'k': 'sack', 'c': '#C9A26B'}, '80 g', ['de flocos de aveia']),
    ({'k': 'jar', 'c': '#E9E2D0'}, '1 c. chá', ['de fermento em pó']), ({'k': 'spices'}, 'a gosto', ['sal, orégãos e sésamo'])],
   steps=[dict(kind='preheat', temp=180, title=['Pré-aquece', 'o forno']),
    dict(kind='fill', target='bowl', title=['Tritura tudo'], batches=[dict(groups=['q'], text=['250 g de queijo cottage']), dict(groups=['e'], text=['3 ovos']), dict(groups=['a'], text=['80 g de aveia e fermento'])], mix='batter', mixText=['Até ficar uma massa lisa']),
    dict(kind='fill', target='dish', title=['Verte', 'na forma'], batches=[dict(groups=['L'], text=['Forma com papel vegetal']), dict(groups=['s'], text=['Sésamo por cima (opcional)'])]),
    dict(kind='bake', temp=180, minutes=30, label='30', sub='minutos', after='Dourado e fofo por dentro.'),
    dict(kind='top', title=['Arrefece', 'e fatia'], batches=[dict(groups=['k'], text=['10 min e corta 6 fatias'])], done='Pronto a acompanhar!')])),

 dict(id='molho-skyr-alho-ervas', title='Molho de skyr com alho e ervas', short='Molho de skyr, alho e ervas',
  protein='Ovos/Queijo', meal='Molho', servings=6, handsOn=10, ovenMax=0, oven='Sem forno', temp=None,
  tags=['molho', 'skyr', 'sem forno', 'tzatziki leve'],
  ingredients=[G(300, 'de skyr natural (ou iogurte grego magro, ou quark)', 'skyr'), G(150, 'de pepino ralado e escorrido', 'pepino'), U(1, 'dente de alho ralado', 'dentes de alho ralados', 'alho'),
   CS(1, 'de sumo de limão', 'limao'), T('Hortelã ou endro picado, sal e pimenta a gosto')],
  steps=[('Rala e escorre o pepino', 'Aperta-o num pano para tirar a água, senão o molho fica aguado.'), ('Mistura tudo', 'Skyr, pepino, alho, limão, ervas, sal e pimenta numa taça.'),
   ('Frigorífico 15 minutos', 'Os sabores juntam-se e o molho fica mais fresco.')],
  tip='Porque skyr e não quark? O skyr é mais cremoso e tem tanta proteína como o quark, com sabor mais suave; o quark também resulta, um pouco mais espesso.',
  tips=['Dura 3 dias no frigorífico.', 'Fica ótimo com frango, peru, salmão ou as bolinhas de atum.'],
  pairs=[],
  video=dict(container='bowl', groups=[
    dict(id='y', shape='blob', c=CURD, n=6, inn='bowl', size=1.2), dict(id='p', shape='pea', c=['#9CCB7A', '#9CCB7A'], n=40, inn='bowl', size=.45), dict(id='g', shape='pea', c=['#F3EAD6', '#F3EAD6'], n=8, inn='bowl', size=.4),
    dict(id='l', shape='lemon', c=LEMON, n=1, inn='bowl', layout='grid'), dict(id='B', shape='layer', c=['#F4F6EE', '#F4F6EE'], inn='bowl', reveal='mix', fleck='#7FB069'), dict(id='h', shape='herb', c=HERB, n=18, inn='bowl', z=1)],
   ingr=[({'k': 'tub', 'c': '#5B7BA8'}, '300 g', ['de skyr natural']), ({'k': 'fruit', 'f': 'cucumber'}, '150 g', ['de pepino ralado e escorrido']), ({'k': 'fruit', 'f': 'garlic'}, '1', ['dente de alho ralado']),
    ({'k': 'fruit', 'f': 'lemon'}, '1 c. sopa', ['de sumo de limão']), ({'k': 'herbs'}, 'a gosto', ['hortelã ou endro,', 'sal e pimenta'])],
   steps=[dict(kind='fill', target='bowl', title=['Mistura', 'tudo'], batches=[dict(groups=['y'], text=['300 g de skyr']), dict(groups=['p'], text=['Pepino ralado e escorrido']), dict(groups=['g', 'l'], text=['Alho e sumo de limão'])], mix='batter', mixText=['Mexe até ficar cremoso']),
    dict(kind='chill', title=['Frigorífico'], label='15', sub='minutos'),
    dict(kind='top', title=['Ervas', 'por cima'], batches=[dict(groups=['h'], text=['Hortelã ou endro picado'])], done='Pronto a servir!')])),

 dict(id='molho-quark-pimento-assado', title='Molho cremoso de quark e pimento assado', short='Molho de quark e pimento',
  protein='Ovos/Queijo', meal='Molho', servings=6, handsOn=10, ovenMax=20, oven='20 min (opcional)', temp=220,
  tags=['molho', 'quark', 'pimento assado', 'para carnes'],
  ingredients=[G(250, 'de quark magro (ou skyr)', 'quark'), G(150, 'de pimento vermelho assado, sem pele', 'pimento'), U(1, 'dente de alho', 'dentes de alho', 'alho'),
   CS(1, 'de sumo de limão', 'limao'), T('Colorau fumado, sal e pimenta a gosto')],
  steps=[('Assa os pimentos (opcional)', '20 minutos a 220 °C até a pele escurecer; ou usa pimentos assados de frasco, escorridos.'), ('Tritura tudo', 'Quark, pimento sem pele, alho, limão e colorau, até ficar liso.'),
   ('Prova e tempera', 'Acerta o sal e a pimenta; serve frio ou à temperatura ambiente.')],
  tip='Pimentos de frasco poupam tempo: escorre-os bem e seca-os com papel para o molho não ficar líquido.',
  tips=['Dura 4 dias no frigorífico.', 'Com skyr fica mais suave; com quark, mais espesso e ótimo para barrar no pão proteico.'],
  pairs=[],
  video=dict(container='bowl', groups=[
    dict(id='q', shape='blob', c=CURD, n=6, inn='bowl', size=1.2), dict(id='r', shape='strip', c=['#D2392A', '#D2392A'], n=10, inn='bowl'), dict(id='g', shape='pea', c=['#F3EAD6', '#F3EAD6'], n=8, inn='bowl', size=.4),
    dict(id='B', shape='layer', c=['#F2A07E', '#F2A07E'], inn='bowl', reveal='mix', fleck='#C0392B'), dict(id='h', shape='herb', c=HERB, n=10, inn='bowl', z=1)],
   ingr=[({'k': 'tub', 'c': '#E07A3A'}, '250 g', ['de quark magro (ou skyr)']), ({'k': 'fruit', 'f': 'pepper'}, '150 g', ['de pimento vermelho assado']), ({'k': 'fruit', 'f': 'garlic'}, '1', ['dente de alho']),
    ({'k': 'fruit', 'f': 'lemon'}, '1 c. sopa', ['de sumo de limão']), ({'k': 'spices'}, 'a gosto', ['colorau fumado, sal e pimenta'])],
   steps=[dict(kind='preheat', temp=220, title=['Assa os', 'pimentos'], note='20 min, ou usa de frasco'),
    dict(kind='fill', target='bowl', title=['Tritura', 'tudo'], batches=[dict(groups=['q'], text=['250 g de quark magro']), dict(groups=['r'], text=['Pimento assado sem pele']), dict(groups=['g'], text=['Alho, limão e colorau'])], mix='batter', mixText=['Até ficar liso']),
    dict(kind='top', title=['Prova e', 'tempera'], batches=[dict(groups=['h'], text=['Sal e pimenta a gosto'])], done='Pronto a servir!')])),

 dict(id='panqueca-forno-aveia-cottage', title='Panqueca de forno de aveia, cottage e frutos vermelhos', short='Panqueca de forno de aveia',
  protein='Ovos/Queijo', meal='Pequeno-almoço', servings=4, handsOn=10, ovenMax=25, oven='25 min', temp=190,
  tags=['pequeno-almoço', 'cottage', 'aveia', 'meal prep'],
  ingredients=[G(120, 'de flocos de aveia', 'aveia'), G(250, 'de queijo cottage', 'cottage'), U(4, 'ovo', 'ovos', 'ovo'), G(100, 'de claras de ovo', 'clara'), U(1, 'banana madura', 'bananas maduras', 'banana'),
   CC(1, 'de fermento em pó', 'fermento'), T('Canela e baunilha a gosto'), G(150, 'de frutos vermelhos', 'frutos_vermelhos')],
  steps=[('Pré-aquece o forno', 'Liga o forno a 190 °C e forra um tabuleiro pequeno com papel vegetal.'), ('Tritura a massa', 'Aveia, cottage, ovos, claras, banana, fermento e canela até ficar lisa.'),
   ('Verte e junta a fruta', 'Espalha a massa no tabuleiro e os frutos vermelhos por cima.'), ('Leva ao forno', '25 minutos, até ficar firme e dourada.'), ('Corta em 4', 'Serve morna ou fria.')],
  tip='Faz no domingo: dura 4 dias no frigorífico e aquece em 30 segundos no micro-ondas.',
  tips=['Uma colher de skyr por cima junta mais 5 g de proteína.', 'Os frutos vermelhos congelados resultam bem, sem descongelar.'],
  pairs=[],
  video=dict(container='tray', groups=[
    dict(id='a', shape='pea', c=['#E6D2A8', '#E6D2A8'], n=40, inn='bowl', size=.55), dict(id='q', shape='curd', c=CURD, n=9, inn='bowl'), dict(id='e', shape='yolk', c=['#F7B32B', '#F7B32B'], n=4, inn='bowl', layout='grid'),
    dict(id='n', shape='slice', c=['#F7EBB0', '#F7EBB0'], n=6, inn='bowl', size=.8), dict(id='B', shape='layer', c=['#EEDDB4', '#EEDDB4'], inn='bowl', reveal='mix'),
    dict(id='L', shape='layer', c=['#E9D3A6', '#C8914A']), dict(id='r', shape='berry', c=RASP, n=18, z=1), dict(id='u', shape='berry', c=BLUE, n=22, z=1, size=.8), dict(id='k', shape='slicelines', c=['#8F5A26', '#8F5A26'], n=2, layout='grid', z=2, cross=True)],
   ingr=[({'k': 'sack', 'c': '#C9A26B'}, '120 g', ['de flocos de aveia']), ({'k': 'tub', 'c': '#2F80C0'}, '250 g', ['de queijo cottage']), ({'k': 'eggs'}, '4', ['ovos e 100 g de claras']),
    ({'k': 'fruit', 'f': 'banana'}, '1', ['banana madura']), ({'k': 'jar', 'c': '#E9E2D0'}, '1 c. chá', ['de fermento em pó']), ({'k': 'spices', 'c': ['#8A4B22', '#F3E3C3', '#B7793D']}, 'a gosto', ['canela e baunilha']),
    (sh('berry', RASP, 5), '150 g', ['de frutos vermelhos'])],
   steps=[dict(kind='preheat', temp=190, title=['Pré-aquece', 'o forno']),
    dict(kind='fill', target='bowl', title=['Tritura', 'a massa'], batches=[dict(groups=['a', 'q'], text=['Aveia e cottage']), dict(groups=['e', 'n'], text=['Ovos, claras e banana']), dict(fx='spice', text=['Fermento e canela'], spice=['#8A4B22', '#B7793D', '#FFF4DE'])], mix='batter', mixText=['Até ficar lisa']),
    dict(kind='fill', target='dish', title=['Verte e junta', 'a fruta'], batches=[dict(groups=['L'], text=['Massa no tabuleiro']), dict(groups=['r', 'u'], text=['150 g de frutos vermelhos'])]),
    dict(kind='bake', temp=190, minutes=25, label='25', sub='minutos', after='Firme e dourada.'),
    dict(kind='top', title=['Corta em 4'], batches=[dict(groups=['k'], text=['Morna ou fria'])], done='Bom pequeno-almoço!')])),

 dict(id='muffins-ovo-peru-espinafres', title='Muffins de ovo com peru e espinafres', short='Muffins de ovo e peru',
  protein='Ovos/Queijo', meal='Pequeno-almoço', servings=4, handsOn=10, ovenMax=20, oven='20 min', temp=180,
  tags=['pequeno-almoço', 'meal prep', 'sem glúten', 'claras'],
  ingredients=[U(6, 'ovo', 'ovos', 'ovo'), G(200, 'de claras de ovo', 'clara'), G(120, 'de fiambre de peito de peru em cubos', 'fiambre_peru'), G(80, 'de espinafres picados', 'espinafres'),
   {'q': 0.5, 'u': 'un', 'n': 'pimento vermelho em cubos', 'np': 'pimentos vermelhos em cubos', 'food': 'pimento'}, G(60, 'de mozzarella light ralada', 'mozzarella_light'), T('Sal, pimenta e orégãos a gosto')],
  steps=[('Pré-aquece o forno', 'Liga o forno a 180 °C e unta levemente uma forma de 12 muffins.'), ('Recheia a forma', 'Distribui o peru, os espinafres e o pimento pelas 12 cavidades.'),
   ('Bate e verte os ovos', 'Bate os ovos com as claras, sal e pimenta e enche cada cavidade.'), ('Queijo por cima', 'Espalha a mozzarella.'), ('Leva ao forno', '20 minutos, até ficarem firmes. Uma dose são 3 muffins.')],
  tip='Usa forma de silicone ou forminhas de papel: os muffins de ovo colam às formas metálicas.',
  tips=['Guarda 4 dias no frigorífico; aquecem em 30 a 40 segundos.', 'Junta uma fatia de pão proteico para um pequeno-almoço completo.'],
  pairs=['pao-proteico-cottage-aveia'],
  video=dict(container='muffin', groups=[
    dict(id='h', shape='cube', c=HAM, n=24, size=.5), dict(id='s', shape='leaf', c=SPIN, n=24, size=.7), dict(id='r', shape='cube', c=PEPR, n=24, size=.4),
    dict(id='L', shape='layer', c=['#F3D36B', '#E2AE48']), dict(id='m', shape='shred', c=MOZ, n=48, z=1), dict(id='o', shape='herb', c=HERB, n=24, z=2, size=.7)],
   ingr=[({'k': 'eggs'}, '6', ['ovos']), ({'k': 'jar', 'c': '#F2EEE2'}, '200 g', ['de claras de ovo']), (sh('cube', HAM, 3), '120 g', ['de fiambre de peito de peru']),
    (sh('leaf', SPIN, 4), '80 g', ['de espinafres picados']), ({'k': 'fruit', 'f': 'pepper'}, '½', ['pimento vermelho em cubos']), ({'k': 'cheese', 'c': '#FFF3D0'}, '60 g', ['de mozzarella light ralada']),
    ({'k': 'spices'}, 'a gosto', ['sal, pimenta e orégãos'])],
   steps=[dict(kind='preheat', temp=180, title=['Pré-aquece', 'o forno']),
    dict(kind='fill', target='dish', title=['Recheia', 'a forma'], batches=[dict(groups=['h'], text=['Peru em cubos']), dict(groups=['s', 'r'], text=['Espinafres e pimento']), dict(groups=['L'], text=['Ovos batidos com claras']), dict(groups=['m'], text=['Mozzarella por cima'])]),
    dict(kind='bake', temp=180, minutes=20, label='20', sub='minutos', after='Fofos e firmes.'),
    dict(kind='top', title=['3 muffins', 'por dose'], batches=[dict(groups=['o'], text=['Orégãos por cima'])], done='Bom pequeno-almoço!')])),

 dict(id='bolinhas-atum-cottage', title='Bolinhas de atum e cottage no forno', short='Bolinhas de atum e cottage',
  protein='Peixe', meal='Snack', servings=4, handsOn=15, ovenMax=18, oven='18 min', temp=200,
  tags=['snack', 'atum', 'cottage', 'lancheira'],
  ingredients=[G(240, 'de atum ao natural escorrido (2 latas)', 'atum'), G(150, 'de queijo cottage', 'cottage'), U(1, 'ovo', 'ovos', 'ovo'), G(40, 'de flocos de aveia', 'aveia'),
   T('Cebolinho, raspa de limão, sal e pimenta a gosto')],
  steps=[('Pré-aquece o forno', 'Liga o forno a 200 °C e forra um tabuleiro com papel vegetal.'), ('Mistura numa taça', 'Atum bem escorrido, cottage, ovo, aveia, cebolinho, limão, sal e pimenta.'),
   ('Molda 16 bolinhas', 'Com as mãos húmidas, e coloca-as no tabuleiro.'), ('Leva ao forno', '18 minutos, virando a meio.'), ('Serve com molho', 'Quentes ou frias, com o molho de skyr.')],
  tip='Escorre muito bem o atum (aperta-o num coador): é o que faz as bolinhas segurarem a forma.',
  tips=['4 bolinhas são um snack de cerca de 23 g de proteína.', 'Levam-se bem na lancheira, frias.'],
  pairs=['molho-skyr-alho-ervas', 'molho-quark-pimento-assado'],
  video=dict(container='tray', groups=[
    dict(id='t', shape='shred', c=['#D9BC94', '#D9BC94'], n=30, inn='bowl', size=1.6), dict(id='q', shape='curd', c=CURD, n=8, inn='bowl'), dict(id='e', shape='yolk', c=['#F7B32B', '#F7B32B'], n=1, inn='bowl', layout='grid'),
    dict(id='a', shape='pea', c=['#E6D2A8', '#E6D2A8'], n=24, inn='bowl', size=.55), dict(id='B', shape='layer', c=['#E3CBA4', '#E3CBA4'], inn='bowl', reveal='mix', fleck='#3E9A4A'),
    dict(id='b', shape='ball', c=TUNA, n=16, layout='grid', size=1.15), dict(id='h', shape='herb', c=HERB, n=18, z=1, size=.7)],
   ingr=[({'k': 'can', 'c': '#5B7BA8'}, '2 latas', ['de atum ao natural (240 g)']), ({'k': 'tub', 'c': '#2F80C0'}, '150 g', ['de queijo cottage']), ({'k': 'eggs'}, '1', ['ovo']),
    ({'k': 'sack', 'c': '#C9A26B'}, '40 g', ['de flocos de aveia']), ({'k': 'herbs'}, 'a gosto', ['cebolinho, limão,', 'sal e pimenta'])],
   steps=[dict(kind='preheat', temp=200, title=['Pré-aquece', 'o forno']),
    dict(kind='fill', target='bowl', title=['Mistura', 'numa taça'], batches=[dict(groups=['t'], text=['Atum bem escorrido']), dict(groups=['q', 'e'], text=['Cottage e ovo']), dict(groups=['a'], text=['Aveia, cebolinho e limão'])], mix='batter', mixText=['Mistura bem']),
    dict(kind='fill', target='dish', title=['Molda 16', 'bolinhas'], batches=[dict(groups=['b'], text=['Com as mãos húmidas'])]),
    dict(kind='bake', temp=200, minutes=18, label='18', sub='minutos', mid='Vira a meio do tempo!', after='Douradas por fora.'),
    dict(kind='top', title=['Serve'], batches=[dict(groups=['h'], text=['Com molho de skyr'])], done='Snack pronto!')])),

 dict(id='grao-crocante-colorau-parmesao', title='Grão crocante com colorau e parmesão', short='Grão crocante com parmesão',
  protein='Vegetariano/Leguminosas', meal='Snack', servings=4, handsOn=5, ovenMax=35, oven='35 min', temp=200,
  tags=['snack', 'leguminosas', 'estaladiço', 'fibra'],
  ingredients=[G(480, 'de grão-de-bico escorrido e bem seco (2 latas)', 'grao'), {'q': 0.5, 'u': 'c. sopa', 'n': 'de azeite', 'food': 'azeite'}, G(20, 'de parmesão ralado', 'parmesao'),
   T('Colorau fumado, alho em pó e sal a gosto')],
  steps=[('Pré-aquece o forno', 'Liga o forno a 200 °C.'), ('Seca bem o grão', 'Esfrega-o num pano limpo e tira as peles que soltarem.'),
   ('Tempera no tabuleiro', 'Azeite, colorau, alho em pó e sal; espalha numa só camada.'), ('Leva ao forno', '30 minutos, mexendo a meio.'), ('Junta o parmesão', 'Mais 5 minutos e deixa arrefecer: fica crocante ao arrefecer.')],
  tip='Quanto mais seco o grão entrar no forno, mais estaladiço sai.',
  tips=['É o snack com mais fibra do livro; para mais proteína, junta um copo de skyr.', 'Guarda num frasco aberto: fechado, amolece.'],
  pairs=['molho-skyr-alho-ervas'],
  video=dict(container='tray', groups=[
    dict(id='c', shape='pea', c=['#EAD095', '#B9772A'], n=110, size=.95), dict(id='p', shape='shred', c=PARM, n=50, z=1)],
   ingr=[({'k': 'can', 'c': '#D9A441'}, '2 latas', ['de grão (480 g escorrido)']), ({'k': 'bottle'}, '½ c. sopa', ['de azeite']), ({'k': 'cheese'}, '20 g', ['de parmesão ralado']),
    ({'k': 'spices'}, 'a gosto', ['colorau fumado,', 'alho em pó e sal'])],
   steps=[dict(kind='preheat', temp=200, title=['Pré-aquece', 'o forno']),
    dict(kind='fill', target='dish', title=['Tempera no', 'tabuleiro'], batches=[dict(groups=['c'], text=['Grão bem seco']), dict(fx='oil', text=['½ c. sopa de azeite']), dict(fx='spice', text=['Colorau, alho em pó e sal'])], mix=True, mixText=['Uma só camada']),
    dict(kind='bake', temp=200, minutes=30, label='30', sub='minutos', mid='Mexe a meio do tempo!', after='Estaladiço por fora.'),
    dict(kind='top', title=['Junta o', 'parmesão'], batches=[dict(groups=['p'], text=['20 g de parmesão ralado'])], done='Mais 5 min e está pronto!')])),

 dict(id='cheesecake-skyr-forno', title='Cheesecake de skyr e quark no forno', short='Cheesecake de skyr',
  protein='Ovos/Queijo', meal='Sobremesa', servings=8, handsOn=15, ovenMax=53, oven='45 min + 4 h de frio', temp=160,
  tags=['sobremesa', 'skyr', 'quark', 'sem açúcar'],
  ingredients=[G(500, 'de skyr natural', 'skyr'), G(250, 'de quark magro', 'quark'), U(3, 'ovo', 'ovos', 'ovo'), G(30, 'de amido de milho', 'amido'),
   G(60, 'de eritritol (ou adoçante a gosto)', 'eritritol'), G(70, 'de flocos de aveia, para a base', 'aveia'), CS(1, 'de mel, para a base', 'mel'), T('Raspa de 1 limão e baunilha a gosto'),
   G(150, 'de frutos vermelhos, para servir', 'frutos_vermelhos')],
  steps=[('Pré-aquece o forno', 'Liga o forno a 160 °C e forra uma forma de aro de 20 cm.'), ('Faz a base', 'Tritura a aveia com o mel e 2 c. sopa de água; calca no fundo e leva 8 minutos ao forno.'),
   ('Bate o creme', 'Skyr, quark, ovos, amido, adoçante, raspa de limão e baunilha, só até ligar.'), ('Leva ao forno', 'Verte sobre a base e coze 45 minutos; o centro deve ainda tremer.'),
   ('Arrefece e refrigera', 'Deixa arrefecer no forno com a porta entreaberta e depois 4 horas no frigorífico.'), ('Frutos vermelhos', 'Por cima, na hora de servir.')],
  tip='Não batas demasiado o creme: o ar que entra faz a cheesecake rachar no forno.',
  tips=['O quark dá firmeza; com só skyr fica mais cremosa e leve.', 'Dura 4 dias no frigorífico.'],
  pairs=[],
  video=dict(container='round', groups=[
    dict(id='y', shape='blob', c=CURD, n=6, inn='bowl', size=1.2), dict(id='e', shape='yolk', c=['#F7B32B', '#F7B32B'], n=3, inn='bowl', layout='grid'), dict(id='l', shape='lemon', c=LEMON, n=1, inn='bowl', layout='grid'),
    dict(id='B', shape='layer', c=['#FBF3DF', '#FBF3DF'], inn='bowl', reveal='mix'), dict(id='L', shape='layer', c=['#FBF3DF', '#ECCB8E']), dict(id='r', shape='berry', c=RASP, n=20, z=1), dict(id='u', shape='berry', c=BLUE, n=24, z=1, size=.8), dict(id='m', shape='herb', c=HERB, n=6, z=2)],
   ingr=[({'k': 'tub', 'c': '#5B7BA8'}, '500 g', ['de skyr natural']), ({'k': 'tub', 'c': '#E07A3A'}, '250 g', ['de quark magro']), ({'k': 'eggs'}, '3', ['ovos']),
    ({'k': 'jar', 'c': '#F2EEE2'}, '30 g', ['de amido de milho']), ({'k': 'jar', 'c': '#FFFFFF'}, '60 g', ['de eritritol']), ({'k': 'sack', 'c': '#C9A26B'}, '70 g', ['de aveia (base)']),
    ({'k': 'jar', 'c': '#E5A82E'}, '1 c. sopa', ['de mel (base)']), (sh('berry', RASP, 5), '150 g', ['de frutos vermelhos'])],
   steps=[dict(kind='preheat', temp=160, title=['Pré-aquece', 'o forno']),
    dict(kind='fill', target='bowl', title=['Bate', 'o creme'], batches=[dict(groups=['y'], text=['Skyr e quark']), dict(groups=['e'], text=['3 ovos e amido']), dict(groups=['l'], text=['Adoçante, limão e baunilha'])], mix='batter', mixText=['Só até ligar']),
    dict(kind='fill', target='dish', title=['Verte', 'sobre a base'], batches=[dict(groups=['L'], text=['Base de aveia e mel', 'já cozida 8 min'])]),
    dict(kind='bake', temp=160, minutes=45, label='45', sub='minutos', after='O centro ainda treme.'),
    dict(kind='chill', title=['Frigorífico'], label='4 h', sub='no mínimo'),
    dict(kind='top', title=['Frutos', 'vermelhos'], batches=[dict(groups=['r', 'u'], text=['150 g por cima']), dict(groups=['m'], text=['Hortelã, se quiseres'])], done='Bom apetite!')])),

 dict(id='crumble-maca-frutos-vermelhos-skyr', title='Crumble de maçã e frutos vermelhos com skyr', short='Crumble de maçã com skyr',
  protein='Ovos/Queijo', meal='Sobremesa', servings=4, handsOn=10, ovenMax=25, oven='25 min', temp=190,
  tags=['sobremesa', 'fruta', 'aveia', 'skyr'],
  ingredients=[U(3, 'maçã em cubos', 'maçãs em cubos', 'maca'), G(200, 'de frutos vermelhos', 'frutos_vermelhos'), G(60, 'de flocos de aveia', 'aveia'), U(1, 'clara de ovo', 'claras de ovo', 'clara'),
   CS(1, 'de mel', 'mel'), T('Canela a gosto'), G(300, 'de skyr natural com baunilha, para servir', 'skyr')],
  steps=[('Pré-aquece o forno', 'Liga o forno a 190 °C.'), ('Fruta no fundo', 'Maçã e frutos vermelhos com canela numa travessa.'),
   ('Faz o crumble', 'Mistura a aveia com a clara e o mel e espalha por cima da fruta.'), ('Leva ao forno', '25 minutos, até a cobertura dourar.'), ('Serve com skyr', 'Morno, com uma colherada de skyr com baunilha.')],
  tip='A clara de ovo substitui a manteiga: o crumble fica estaladiço com uma fração das calorias.',
  tips=['Pera ou ananás também resultam bem.', 'Com skyr de baunilha já adoçado, dispensa o mel.'],
  pairs=[],
  video=dict(container='tray', groups=[
    dict(id='a', shape='cube', c=APPLE, n=30, size=.85), dict(id='r', shape='berry', c=RASP, n=22), dict(id='u', shape='berry', c=BLUE, n=26, size=.8),
    dict(id='c', shape='crumb', c=CRUMB, n=120, z=1, size=1.7), dict(id='y', shape='blob', c=CURD, n=4, layout='grid', z=2), dict(id='m', shape='herb', c=HERB, n=6, z=3)],
   ingr=[({'k': 'fruit', 'f': 'apple'}, '3', ['maçãs em cubos']), (sh('berry', RASP, 5), '200 g', ['de frutos vermelhos']), ({'k': 'sack', 'c': '#C9A26B'}, '60 g', ['de flocos de aveia']),
    ({'k': 'eggs'}, '1', ['clara de ovo']), ({'k': 'jar', 'c': '#E5A82E'}, '1 c. sopa', ['de mel']), ({'k': 'spices', 'c': ['#8A4B22', '#B7793D', '#F3E3C3']}, 'a gosto', ['canela']),
    ({'k': 'tub', 'c': '#5B7BA8'}, '300 g', ['de skyr com baunilha', '(para servir)'])],
   steps=[dict(kind='preheat', temp=190, title=['Pré-aquece', 'o forno']),
    dict(kind='fill', target='dish', title=['Fruta', 'no fundo'], batches=[dict(groups=['a'], text=['3 maçãs em cubos']), dict(groups=['r', 'u'], text=['200 g de frutos vermelhos']), dict(fx='spice', text=['Canela'], spice=['#8A4B22', '#B7793D'])]),
    dict(kind='fill', target='dish', title=['Faz o', 'crumble'], batches=[dict(groups=['c'], text=['Aveia, clara e mel por cima'])]),
    dict(kind='bake', temp=190, minutes=25, label='25', sub='minutos', after='Cobertura dourada e estaladiça.'),
    dict(kind='top', title=['Serve', 'com skyr'], batches=[dict(groups=['y'], text=['Skyr com baunilha']), dict(groups=['m'], text=['Hortelã, se quiseres'])], done='Bom apetite!')])),
]

from recipes_extra import RECIPES_EXTRA, META
from foods import FIBER, PRICE, GLUTEN, MEAT_FISH, LABELS, PANTRY, SUBS
for _r in RECIPES:
    _m = dict(META.get(_r['id'], {}))
    _r['pairs'] = _r['pairs'] + [p for p in _m.pop('addPairs', []) if p not in _r['pairs']]
    _r.update(_m)
RECIPES += RECIPES_EXTRA

def grams_of(ing):
    if 't' in ing: return 0
    f = ing['food']; q = ing['q']
    if ing['u'] == 'g': return q
    if ing['u'] == 'un': return q * (ing.get('grams') or UNIT_G[f])
    if ing['u'] == 'c. sopa': return q * SPOON_G[f]
    if ing['u'] == 'c. chá': return q * SPOON_G[f] / 3
    raise ValueError(ing)

def build():
    out = []
    for r in RECIPES:
        tot = [0, 0, 0, 0]; br = []
        for ing in r['ingredients']:
            g = grams_of(ing)
            if not g: continue
            v = FOODS[ing['food']]
            vals = [v[i] * g / 100 for i in range(4)]
            tot = [a + b for a, b in zip(tot, vals)]
            label = (ing['n'][3:] if ing['n'].startswith('de ') else ing['n'])
            label = label[0].upper() + label[1:]
            br.append({'item': label.split(',')[0].split(' (')[0], 'g': round(g), 'kcal': round(vals[0]), 'protein': round(vals[1])})
        s = r['servings']
        m = {'kcal': round(tot[0] / s / 5) * 5, 'protein': round(tot[1] / s), 'carbs': round(tot[2] / s), 'fat': round(tot[3] / s)}
        rr = dict(r); rr['macrosPerServing'] = m; rr['macroBreakdownWholeRecipe'] = br
        rr['proteinPer100kcal'] = round(tot[1] / tot[0] * 100, 1)
        foods = [i['food'] for i in r['ingredients'] if 'food' in i]
        fib = sum(FIBER[i['food']] * grams_of(i) / 100 for i in r['ingredients'] if 'food' in i)
        cost = sum(PRICE[i['food']] * grams_of(i) / 1000 for i in r['ingredients'] if 'food' in i) / s
        m['fiber'] = round(fib / s)
        rr['totalMin'] = r['handsOn'] + r['ovenMax']
        rr['costPerServing'] = round(cost, 2)
        rr['cost'] = '€' if cost < 1.5 else ('€€' if cost < 3 else '€€€')
        rr['glutenFree'] = not any(f in GLUTEN for f in foods)
        rr['vegetarian'] = not any(f in MEAT_FISH for f in foods)
        rr['difficulty'] = r.get('difficulty', 'Fácil')
        rr['mealPrep'] = bool(r.get('mealPrep'))
        rr['freezer'] = bool(r.get('freezer'))
        rr['storage'] = r.get('storage', '')
        rr['foods'] = sorted(set(foods), key=foods.index)
        tags = [t for t in r['tags'] if t != 'sem glúten']
        if rr['glutenFree']: tags.append('sem glúten')
        rr['tags'] = tags
        rr['steps'] = [{'title': a, 'detail': b} for a, b in r['steps']]
        rr['videoFile'] = f"videos/{r['id']}.mp4"
        out.append(rr)
    book = {'title': 'Livro de Receitas Fit do Chef', 'language': 'pt-PT',
            'proteinTypes': ['Frango/Peru', 'Vaca/Porco', 'Ovos/Queijo', 'Vegetariano/Leguminosas', 'Peixe'],
            'mealTypes': ['Prato principal', 'Acompanhamento/Pão', 'Molho', 'Pequeno-almoço', 'Snack', 'Sobremesa'],
            'foods': {k: {'label': LABELS[k][0], 'group': LABELS[k][1], 'pantry': k in PANTRY} for k in LABELS},
            'foodGroups': ['Carne e aves', 'Peixe', 'Ovos e laticínios', 'Leguminosas e tofu', 'Batata, cereais e pão', 'Legumes', 'Fruta', 'Despensa básica'],
            'subs': SUBS,
            'notes': 'Macros por dose são estimativas a partir de ingredientes crus (tools/foods.py). Para acrescentar uma receita: junta-a a tools/recipes_src.py, corre o script e gera o vídeo com tools/render_all.py (ver README.md).'}
    json.dump({'book': book, 'recipes': out}, open(os.path.join(os.path.dirname(__file__), '..', 'recipes.json'), 'w'), ensure_ascii=False, indent=1)
    for r in out:
        m = r['macrosPerServing']; print(f"{r['id']:42s} {r['meal']:18s} {m['kcal']:4d} kcal {m['protein']:3d} P {m['carbs']:3d} C {m['fat']:3d} F  P/100={r['proteinPer100kcal']} fib={m['fiber']} {r['cost']}{r['costPerServing']} gf={int(r['glutenFree'])} veg={int(r['vegetarian'])}")

if __name__ == '__main__': build()
