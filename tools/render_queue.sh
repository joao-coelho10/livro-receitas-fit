#!/usr/bin/env bash
# Gera, uma a uma, os vídeos narrados que ainda não têm áudio (retoma onde ficou se for interrompido).
# Uso: tools/render_queue.sh [ids...]   (sem ids: todas as receitas de recipes.json, novas primeiro)
cd "$(dirname "$0")/.."
ids="$*"; [ -z "$ids" ] && ids=$(python3 -c "import json;r=json.load(open('recipes.json'))['recipes'];print(' '.join([x['id'] for x in r[16:]]+[x['id'] for x in r[:16]]))")
for id in $ids; do
  f="videos/$id.mp4"
  if [ -f "$f" ] && [ -n "$(ffprobe -v error -select_streams a -show_entries stream=codec_name -of csv=p=0 "$f")" ]; then echo "$(date +%H:%M) ja feito: $id"; continue; fi
  echo "$(date +%H:%M) a gerar: $id"
  python3 tools/render_all.py "$id" || echo "$(date +%H:%M) FALHOU: $id"
done
echo "$(date +%H:%M) FIM"
