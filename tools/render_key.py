# Imprime uma "chave" por receita: hash do texto narrado + da cena do vídeo.
# O render_queue.sh guarda-a em .build/rendered/<id> depois de gerar o vídeo e volta a gerar se mudar.
# Uso: python3 tools/render_key.py <id>
import json, sys, os, hashlib
sys.path.insert(0, os.path.dirname(__file__))
import narration
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rid = sys.argv[1]
r = next(x for x in json.load(open(f'{ROOT}/recipes.json'))['recipes'] if x['id'] == rid)
print(hashlib.sha1(json.dumps({'s': narration.script(r), 'v': r['video']}, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:12])
