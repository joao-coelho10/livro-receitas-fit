# Livro de Receitas Fit

Receitas de forno, leves e ricas em proteína, com vídeo animado passo a passo.
É uma app web instalável (PWA): abre no telemóvel, adiciona-se ao ecrã principal e funciona sem internet.

**O que tem:** pesquisa (ignora acentos; várias palavras têm de aparecer todas), filtros combináveis por refeição, proteína e extras (até 30 min, fácil, sem glúten, vegetariana, meal prep, congela bem, económica) com contagens, ordenação, **O que tenho em casa** (marcas os ingredientes que tens e a app mostra o que podes fazer já e o que só precisa de mais 1 ou 2 coisas), página de cada receita com vídeo narrado, ingredientes que se ajustam às doses (e que podes riscar), passos, macros estimadas, “Combina com”, favoritas, **Modo cozinha** (passos em letra grande, ecrã sempre ligado, temporizador) e **Refeição completa** (sugere prato + pão + molho + sobremesa para um alvo de kcal e de proteína).

## Publicar no GitHub Pages

1. Faz push deste repositório para o GitHub (ramo `main`).
2. No repositório: **Settings → Pages → Build and deployment → Source: Deploy from a branch**, ramo `main`, pasta `/ (root)`.
3. Passado um minuto fica em `https://<utilizador>.github.io/<repositório>/`.

Não há passo de build: o site é HTML, CSS e JavaScript simples. Todos os caminhos são relativos, por isso funciona em qualquer subpasta. O ficheiro `.nojekyll` impede o GitHub de processar o site com Jekyll.

## Instalar no telemóvel

- **iPhone (Safari):** Partilhar → *Adicionar ao ecrã principal*.
- **Android (Chrome):** menu ⋮ → *Instalar app*.

Na app, o separador **Offline** permite guardar todos os vídeos de uma vez (cerca de 90 MB). A app e as receitas ficam guardadas sozinhas; os vídeos também se guardam quando os vês (dá para desligar).

## Estrutura

```
index.html, styles.css, app.js   a app (sem dependências)
sw.js                            service worker (offline)
manifest.webmanifest, icons/     instalação como app
recipes.json                     TODAS as receitas (a app lê só isto)
videos/<id>.mp4                  um vídeo por receita
media/<id>.jpg                   poster do vídeo (1.º ecrã)
media/<id>-thumb.webp            miniatura quadrada da lista
tools/                           geração das receitas e dos vídeos
  recipes_src.py                 receitas da 1.ª leva + cálculo de macros, fibra, custo, etc. -> recipes.json
  recipes_extra.py               receitas da 2.ª leva + metadados (dificuldade, conservação, frase de abertura)
  foods.py                       valores por 100 g, fibra, preço aproximado, rótulos e grupos dos alimentos
  video/video2.html              desenha cada fotograma do vídeo a partir da receita
  narration.py                   guião da narração, voz (edge-tts) e mistura com a música
  audio/make_music.py            música de fundo original, sintetizada
  render_all.py                  junta tudo: fotogramas + narração + música -> videos/<id>.mp4
```

## Narração e música dos vídeos

- **Guião:** `tools/narration.py` escreve uma fala por cena (título, ingredientes, cada passo, fecho) a partir dos dados da receita, em português de Portugal, por “tu”, com tom bem-disposto (“Então, hoje vamos fazer…”). A frase de abertura de cada receita é o campo `hook`. Para mudar a fala de uma cena, põe na receita `narr={índice_da_cena: 'texto'}`. Vê o guião com `python3 tools/narration.py <id>`.
- **Voz:** [edge-tts](https://github.com/rany2/edge-tts) com a voz neural `pt-PT-RaquelNeural` (português europeu), ligeiramente mais rápida (`+6%`). Precisa de internet. As falas ficam em cache em `.build/tts/` (fora do git). Para outra voz: `RF_VOICE=pt-PT-DuarteNeural`.
- **Tempo:** cada cena do vídeo dura pelo menos o tempo da fala + 1 s (`window.SCENE_DUR` em `video2.html`), por isso a imagem acompanha sempre a voz.
- **Música:** `tools/audio/make_music.py` sintetiza uma faixa original de 37 s que dá a volta sem cortes (ukulele, baixo, marimba e percussão leve, 104 BPM). Não usa samples nem música de terceiros: é obra própria, dedicada ao domínio público (CC0). Toca baixinho e baixa ainda mais enquanto há voz (“ducking”).
- **Áudio final:** AAC estéreo a 96 kbps, normalizado para −16 LUFS; vídeo H.264 com `faststart`. Sem narração: `python3 tools/render_all.py <id> --mudo`.
- Dependências: `pip install playwright edge-tts numpy` e ffmpeg.

## Acrescentar uma receita

A app é guiada pelos dados: uma receita nova = uma entrada em `recipes.json` + o seu vídeo (+ poster e miniatura).

1. **Escreve a receita** em `tools/recipes_extra.py` (com `R(...)`), copiando uma existente:
   `id` (único, sem acentos, com hífenes), `title`, `short`, `protein` e `meal` (um dos valores das listas `proteinTypes`/`mealTypes`), `servings`, `handsOn` e `ovenMax` (minutos), `oven`, `temp`, `tags`, `ingredients` (com `G()`, `U()`, `CS()`, `CC()`, `T()`), `steps`, `tip`, `tips`, `pairs` (ids de receitas que combinam), `difficulty`, `storage`, `mealPrep`, `freezer`, `hook` (1.ª frase da narração), `unit` (só para pão: `['fatia', 'fatias']`) e `video` (a cena animada). Cada ingrediente tem uma chave `food` de `tools/foods.py`; é isso que alimenta as macros, a fibra, o custo, o “sem glúten” e o “O que tenho em casa”.
   Se usares um alimento novo, junta a `tools/foods.py` os valores por 100 g, a fibra (`FIBER`), o preço (`PRICE`) e o rótulo/grupo (`LABELS`).
2. **Gera o `recipes.json`** (recalcula as macros por dose):
   ```bash
   python3 tools/recipes_src.py
   ```
3. **Gera o vídeo, o poster e a miniatura** (precisa de Python com Playwright e de ffmpeg):
   ```bash
   pip install playwright edge-tts numpy && playwright install chromium   # só da primeira vez
   python3 tools/render_all.py <id> --preview   # opcional: fotogramas de amostra em .frames/<id>/
   python3 tools/render_all.py <id>             # videos/<id>.mp4 (com narração e música) + media/<id>.jpg + media/<id>-thumb.webp
   ```
   Para usar o Chrome do sistema: `CHROME=/usr/bin/google-chrome python3 tools/render_all.py <id>`.
4. **Experimenta localmente:** `python3 -m http.server 8000` e abre `http://localhost:8000/`.
5. Faz commit e push. Quem já tem a app recebe a receita nova na próxima abertura com internet.

Notas:
- Se tiveres um vídeo feito de outra forma, põe-no em `videos/<id>.mp4` e corre `python3 tools/make_media.py <id> --reencode` para o comprimir (H.264, `faststart`) e gerar o poster e a miniatura.
- Também podes editar o `recipes.json` à mão; os campos que a app usa são os de cima mais `macrosPerServing` (`kcal`, `protein`, `carbs`, `fat`) e, opcionalmente, `macroBreakdownWholeRecipe`. O campo `video` só serve para gerar o vídeo.
- Se mudares `index.html`, `styles.css` ou `app.js`, a app atualiza-se sozinha (na abertura seguinte). Se quiseres limpar as caches antigas de todos, aumenta `VERSION` em `sw.js`. Se voltares a gerar vídeos que já existiam, muda também o nome da cache de vídeos (`VIDEOS` em `sw.js` e `VIDEO_CACHE` em `app.js`, iguais) para quem os guardou receber os novos.
- Mantém cada vídeo pequeno (os atuais têm 1,5 a 3,5 MB); o GitHub recusa ficheiros com mais de 100 MB e avisa acima de 50 MB.

As macros, a fibra e o custo por dose (€ até 1,50 €, €€ até 3 €, €€€ acima) são estimativas a partir dos ingredientes crus e variam com as marcas e o tamanho dos ingredientes.
