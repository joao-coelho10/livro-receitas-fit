# Valores aproximados por 100 g (kcal, proteína, hidratos, gordura), alimentos crus/escorridos.
FOODS = {
 'frango':(120,22.5,0,2.6),'peru':(111,24.6,0,1.0),'vaca5':(137,21,0,5.5),'porco_lombo':(143,21.4,0,5.7),
 'salmao':(208,20,0,13),'atum':(116,26,0,1.0),'ovo':(143,12.6,0.7,9.5),'clara':(52,10.9,0.7,0.2),
 'fiambre_peru':(105,19,2,2.2),'cottage':(84,11,4.3,2.3),'quark':(67,12,4,0.2),'skyr':(63,11,4,0.2),
 'iog_grego':(59,10.2,3.6,0.4),'mozzarella_light':(165,20,2,9),'parmesao':(392,35.8,3.2,25.8),'tofu':(144,15.6,2.8,8.7),
 'batata':(77,2,17,0.1),'batata_doce':(86,1.6,20,0.1),'grao':(139,7,22.5,2.6),'feijao_branco':(105,7,18,0.5),
 'pimento':(27,1,6,0.3),'cebola':(40,1.1,9.3,0.1),'tomate_lata':(32,1.6,5.8,0.3),'tomate_cherry':(18,0.9,3.9,0.2),
 'cogumelos':(22,3.1,3.3,0.3),'feijao_verde':(31,1.8,7,0.2),'couve_bruxelas':(43,3.4,9,0.3),'brocolos':(34,2.8,7,0.4),
 'couve_flor':(25,1.9,5,0.3),'espinafres':(23,2.9,3.6,0.4),'pepino':(15,0.7,3.6,0.1),'alho':(149,6.4,33,0.5),
 'limao':(22,0.4,7,0.2),'azeite':(884,0,0,100),'mostarda':(66,4,6,3.3),'aveia':(379,13,68,6.5),'mel':(304,0.3,82,0),
 'amido':(381,0.3,91,0.1),'eritritol':(0,0,0,0),'caril':(325,14,56,14),'fermento':(53,0,28,0),
 'banana':(89,1.1,23,0.3),'maca':(52,0.3,14,0.2),'frutos_vermelhos':(50,1,12,0.3),
}
UNIT_G = {'ovo':55,'cebola':120,'pimento':150,'banana':120,'maca':150,'alho':4,'clara':33}
SPOON_G = {'azeite':13,'mostarda':15,'mel':20,'limao':15,'fermento':4,'caril':3}

# ---- Alimentos novos (valores aproximados por 100 g: kcal, proteína, hidratos, gordura) ----
FOODS.update({
 'frango_coxa':(121,19.7,0,4.1),'peru_picado':(125,21,0,4.5),'sardinha_lata':(208,24.6,0,11.5),
 'lentilhas':(116,9,20,0.4),'feijao_vermelho':(127,8.7,22.8,0.5),'feijao_preto':(132,8.9,23.7,0.5),'ervilhas':(81,5.4,14.5,0.4),
 'abobora':(45,1,11.7,0.1),'curgete':(17,1.2,3.1,0.3),'cenoura':(41,0.9,9.6,0.2),'beringela':(25,1,6,0.2),
 'pera':(57,0.4,15,0.1),'cacau':(228,19.6,58,13.7),'leite_magro':(35,3.4,5,0.1),'queijo_fresco':(95,11,3.5,4),
 'tortilha_integral':(300,9,48,7),'tomate':(18,0.9,3.9,0.2),'chia':(486,17,42,31),'paprika':(282,14,54,13),
})
UNIT_G.update({'pera':170,'tortilha_integral':40,'curgete':250,'cenoura':80,'tomate':120,'beringela':300})
SPOON_G.update({'cacau':6,'chia':10,'paprika':3})

# Fibra por 100 g (g)
FIBER = {
 'frango':0,'peru':0,'vaca5':0,'porco_lombo':0,'salmao':0,'atum':0,'ovo':0,'clara':0,'fiambre_peru':0,'cottage':0,'quark':0,'skyr':0,
 'iog_grego':0,'mozzarella_light':0,'parmesao':0,'tofu':2.3,'batata':2.2,'batata_doce':3,'grao':7.6,'feijao_branco':6.3,'pimento':2.1,
 'cebola':1.7,'tomate_lata':1.5,'tomate_cherry':1.2,'cogumelos':1,'feijao_verde':2.7,'couve_bruxelas':3.8,'brocolos':2.6,'couve_flor':2,
 'espinafres':2.2,'pepino':0.5,'alho':2.1,'limao':2.8,'azeite':0,'mostarda':3.3,'aveia':10,'mel':0.2,'amido':0.9,'eritritol':0,'caril':33,
 'fermento':0.2,'banana':2.6,'maca':2.4,'frutos_vermelhos':5,
 'frango_coxa':0,'peru_picado':0,'sardinha_lata':0,'lentilhas':7.9,'feijao_vermelho':6.4,'feijao_preto':8.7,'ervilhas':5.1,'abobora':2,
 'curgete':1,'cenoura':2.8,'beringela':3,'pera':3.1,'cacau':33,'leite_magro':0,'queijo_fresco':0,'tortilha_integral':6,'tomate':1.2,
 'chia':34,'paprika':35,
}
# Preço aproximado em Portugal (€/kg, supermercado, 2026) para estimar o custo por dose
PRICE = {
 'frango':7,'peru':8,'vaca5':11,'porco_lombo':7,'salmao':18,'atum':14,'ovo':4.5,'clara':6,'fiambre_peru':12,'cottage':6,'quark':4.5,
 'skyr':5,'iog_grego':4,'mozzarella_light':10,'parmesao':20,'tofu':8,'batata':1.2,'batata_doce':2.2,'grao':2.5,'feijao_branco':2.5,
 'pimento':3,'cebola':1.2,'tomate_lata':1.8,'tomate_cherry':4,'cogumelos':5,'feijao_verde':4,'couve_bruxelas':4,'brocolos':3.5,
 'couve_flor':3,'espinafres':6,'pepino':1.5,'alho':6,'limao':2,'azeite':9,'mostarda':6,'aveia':2.5,'mel':10,'amido':4,'eritritol':12,
 'caril':30,'fermento':15,'banana':1.5,'maca':2,'frutos_vermelhos':8,
 'frango_coxa':5.5,'peru_picado':8.5,'sardinha_lata':12,'lentilhas':3,'feijao_vermelho':2.5,'feijao_preto':3,'ervilhas':3,'abobora':1.8,
 'curgete':2,'cenoura':1,'beringela':2.5,'pera':2,'cacau':15,'leite_magro':0.8,'queijo_fresco':7,'tortilha_integral':6,'tomate':2,
 'chia':12,'paprika':25,
}
GLUTEN = {'aveia', 'tortilha_integral'}  # aveia só é sem glúten se for certificada
MEAT_FISH = {'frango','peru','vaca5','porco_lombo','salmao','atum','fiambre_peru','frango_coxa','peru_picado','sardinha_lata'}

# Nome simples e grupo de cada alimento (para "O que tenho em casa"). pantry=True: básico de despensa.
LABELS = {
 'frango':('Peito de frango','Carne e aves'),'frango_coxa':('Coxas de frango','Carne e aves'),'peru':('Peru','Carne e aves'),
 'peru_picado':('Peru picado','Carne e aves'),'fiambre_peru':('Fiambre de peru','Carne e aves'),'vaca5':('Carne picada de vaca','Carne e aves'),
 'porco_lombo':('Lombo de porco','Carne e aves'),
 'salmao':('Salmão','Peixe'),'atum':('Atum em lata','Peixe'),'sardinha_lata':('Sardinhas em lata','Peixe'),
 'ovo':('Ovos','Ovos e laticínios'),'clara':('Claras de ovo','Ovos e laticínios'),'cottage':('Queijo cottage','Ovos e laticínios'),
 'quark':('Quark','Ovos e laticínios'),'skyr':('Skyr','Ovos e laticínios'),'iog_grego':('Iogurte grego magro','Ovos e laticínios'),
 'mozzarella_light':('Mozzarella light','Ovos e laticínios'),'parmesao':('Parmesão','Ovos e laticínios'),'queijo_fresco':('Queijo fresco','Ovos e laticínios'),
 'leite_magro':('Leite magro','Ovos e laticínios'),
 'grao':('Grão-de-bico','Leguminosas e tofu'),'feijao_branco':('Feijão branco','Leguminosas e tofu'),'feijao_vermelho':('Feijão vermelho','Leguminosas e tofu'),
 'feijao_preto':('Feijão preto','Leguminosas e tofu'),'lentilhas':('Lentilhas','Leguminosas e tofu'),'ervilhas':('Ervilhas','Leguminosas e tofu'),'tofu':('Tofu','Leguminosas e tofu'),
 'batata':('Batata','Batata, cereais e pão'),'batata_doce':('Batata-doce','Batata, cereais e pão'),'aveia':('Flocos de aveia','Batata, cereais e pão'),
 'tortilha_integral':('Tortilhas integrais','Batata, cereais e pão'),
 'pimento':('Pimento','Legumes'),'cebola':('Cebola','Legumes'),'tomate_lata':('Tomate em lata','Legumes'),'tomate_cherry':('Tomate cherry','Legumes'),
 'tomate':('Tomate','Legumes'),'cogumelos':('Cogumelos','Legumes'),'feijao_verde':('Feijão-verde','Legumes'),'couve_bruxelas':('Couves-de-bruxelas','Legumes'),
 'brocolos':('Brócolos','Legumes'),'couve_flor':('Couve-flor','Legumes'),'espinafres':('Espinafres','Legumes'),'pepino':('Pepino','Legumes'),
 'abobora':('Abóbora','Legumes'),'curgete':('Curgete','Legumes'),'cenoura':('Cenoura','Legumes'),'beringela':('Beringela','Legumes'),
 'banana':('Banana','Fruta'),'maca':('Maçã','Fruta'),'pera':('Pera','Fruta'),'frutos_vermelhos':('Frutos vermelhos','Fruta'),'limao':('Limão','Fruta'),
 'azeite':('Azeite','Despensa básica'),'alho':('Alho','Despensa básica'),'mostarda':('Mostarda','Despensa básica'),'mel':('Mel','Despensa básica'),
 'amido':('Amido de milho','Despensa básica'),'eritritol':('Adoçante','Despensa básica'),'caril':('Caril em pó','Despensa básica'),
 'fermento':('Fermento em pó','Despensa básica'),'paprika':('Colorau','Despensa básica'),'cacau':('Cacau magro','Despensa básica'),'chia':('Sementes de chia','Despensa básica'),
}
PANTRY = {'azeite','alho','mostarda','mel','amido','eritritol','caril','fermento','paprika'}
# Trocas aceitáveis (se tens um, serve para o outro)
SUBS = [['skyr','iog_grego','quark'], ['frango','peru'], ['feijao_branco','feijao_vermelho','feijao_preto'], ['tomate','tomate_cherry']]

# ---- 3.ª leva: pequenos-almoços, snacks, saladas e pratos de volume ----
_NEW = {  # chave: (kcal, P, C, G por 100 g), fibra, €/kg, rótulo, grupo
 'quinoa':((120,4.4,21.3,1.9),2.8,4.5,'Quinoa (cozida)','Batata, cereais e pão'),
 'pao_integral':((247,13,41,3.4),7,3.5,'Pão integral','Batata, cereais e pão'),
 'bolacha_arroz':((387,8,81,2.8),4,6,'Bolachas de arroz','Batata, cereais e pão'),
 'milho_pipoca':((375,11,74,4.3),15,3,'Milho para pipocas','Batata, cereais e pão'),
 'alface':((15,1.4,2.9,0.2),1.3,3,'Alface / mistura de folhas','Legumes'),
 'rucula':((25,2.6,3.7,0.7),1.6,9,'Rúcula','Legumes'),
 'couve':((32,2.5,6,0.6),2.5,2.5,'Couve portuguesa / lombarda','Legumes'),
 'alho_frances':((61,1.5,14,0.3),1.8,2.5,'Alho-francês','Legumes'),
 'beterraba':((43,1.6,10,0.2),2.8,2.5,'Beterraba cozida','Legumes'),
 'milho':((86,3.3,19,1.4),2.7,3,'Milho doce','Legumes'),
 'aipo':((16,0.7,3,0.2),1.6,2.5,'Aipo','Legumes'),
 'morangos':((32,0.7,7.7,0.3),2,5,'Morangos','Fruta'),
 'kiwi':((61,1.1,15,0.5),3,3,'Kiwi','Fruta'),
 'laranja':((47,0.9,12,0.1),2.4,1.5,'Laranja','Fruta'),
 'abacate':((160,2,8.5,14.7),6.7,6,'Abacate','Fruta'),
 'manteiga_amendoim':((588,25,20,50),6,9,'Manteiga de amendoim','Despensa básica'),
 'amendoim_po':((400,50,24,12),8,22,'Amendoim em pó (PB2)','Despensa básica'),
 'whey':((380,78,8,5),0,25,'Proteína em pó (whey)','Ovos e laticínios'),
 'iog_natural':((56,4.5,6,1.5),0,2,'Iogurte natural magro','Ovos e laticínios'),
 'requeijao':((170,11,4,12),0,9,'Requeijão','Ovos e laticínios'),
 'feta_light':((180,17,1,12),0,11,'Feta light','Ovos e laticínios'),
 'salmao_fumado':((117,18,0,4.3),0,30,'Salmão fumado','Peixe'),
 'presunto':((180,30,0,6),0,25,'Presunto (sem gordura)','Carne e aves'),
 'edamame':((121,11.9,8.9,5.2),5.2,8,'Edamame','Leguminosas e tofu'),
 'canela':((247,4,81,1.2),53,25,'Canela','Despensa básica'),
}
for _k, (_m, _f, _p, _l, _g) in _NEW.items():
    FOODS[_k] = _m; FIBER[_k] = _f; PRICE[_k] = _p; LABELS[_k] = (_l, _g)
UNIT_G.update({'kiwi':75,'laranja':180,'abacate':150,'pao_integral':35,'bolacha_arroz':8,'morangos':15,'aipo':40,'alho_frances':150})
SPOON_G.update({'manteiga_amendoim':16,'amendoim_po':8,'canela':3,'whey':10})
GLUTEN |= {'pao_integral'}
MEAT_FISH |= {'salmao_fumado','presunto'}
PANTRY |= {'canela'}
SUBS += [['alface','rucula','espinafres'], ['iog_natural','iog_grego','skyr'], ['laranja','kiwi']]
