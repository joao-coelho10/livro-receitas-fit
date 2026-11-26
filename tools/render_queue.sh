#!/usr/bin/env bash
# Gera, uma a uma, os vídeos narrados que faltam ou estão desatualizados (retoma onde ficou se for interrompido).
# Um vídeo está "feito" se tem faixa de áudio e a chave guardada em .build/rendered/<id> é igual à atual
# (tools/render_key.py: hash do texto narrado + cena). Mudou a narração ou a cena? Volta a ser gerado.
# Uso: tools/render_queue.sh [ids...]   (sem ids: todas as receitas de recipes.json, as mais recentes primeiro)
cd "$(dirname "$0")/.."
mkdir -p .build/rendered
ids="$*"; [ -z "$ids" ] && ids=$(python3 -c "import json;r=json.load(open('recipes.json'))['recipes'];print(' '.join(x['id'] for x in r[::-1]))")
for id in $ids; do
  f="videos/$id.mp4"; key=$(python3 tools/render_key.py "$id")
  if [ -f "$f" ] && [ "$(cat .build/rendered/$id 2>/dev/null)" = "$key" ] && [ -n "$(ffprobe -v error -select_streams a -show_entries stream=codec_name -of csv=p=0 "$f")" ]; then echo "$(date +%H:%M) ja feito: $id"; continue; fi
  echo "$(date +%H:%M) a gerar: $id"
  if python3 tools/render_all.py "$id"; then echo "$key" > ".build/rendered/$id"; python3 tools/recipes_src.py > /dev/null; echo "$(date +%H:%M) ok: $id"
  else echo "$(date +%H:%M) FALHOU: $id"; fi
done
echo "$(date +%H:%M) FIM"
