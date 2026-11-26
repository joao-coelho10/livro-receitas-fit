# Livro de Receitas Fit

Receitas de forno, leves e ricas em proteína, com vídeo animado passo a passo.
É uma app web instalável (PWA): abre no telemóvel, adiciona-se ao ecrã principal e funciona sem internet.

**O que tem:** pesquisa (ignora acentos; várias palavras têm de aparecer todas), filtros combináveis por refeição e por proteína com contagens, ordenação, página de cada receita com vídeo, ingredientes que se ajustam às doses (e que podes riscar), passos, macros estimadas, “Combina com”, favoritas, **Modo cozinha** (passos em letra grande, ecrã sempre ligado, temporizador) e **Refeição completa** (sugere prato + pão + molho + sobremesa para um alvo de kcal e de proteína).

## Publicar no GitHub Pages

1. Faz push deste repositório para o GitHub (ramo `main`).
2. No repositório: **Settings → Pages → Build and deployment → Source: Deploy from a branch**, ramo `main`, pasta `/ (root)`.
3. Passado um minuto fica em `https://<utilizador>.github.io/<repositório>/`.

Não há passo de build: o site é HTML, CSS e JavaScript simples. Todos os caminhos são relativos, por isso funciona em qualquer subpasta. O ficheiro `.nojekyll` impede o GitHub de processar o site com Jekyll.

## Instalar no telemóvel

- **iPhone (Safari):** Partilhar → *Adicionar ao ecrã principal*.
- **Android (Chrome):** menu ⋮ → *Instalar app*.

Na app, o separador **Offline** permite guardar todos os vídeos de uma vez (cerca de 20 MB). A app e as receitas ficam guardadas sozinhas; os vídeos também se guardam quando os vês (dá para desligar).

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
```

## Acrescentar uma receita

A app é guiada pelos dados: uma receita nova = uma entrada em `recipes.json` + o seu vídeo (+ poster e miniatura).

1. **Escreve a receita** em `tools/recipes_src.py`, copiando uma existente para a lista `RECIPES`:
   `id` (único, sem acentos, com hífenes), `title`, `short`, `protein` e `meal` (um dos valores das listas `proteinTypes`/`mealTypes`), `servings`, `handsOn` e `ovenMax` (minutos), `oven`, `temp`, `tags`, `ingredients` (com `G()`, `U()`, `CS()`, `CC()`, `T()`), `steps`, `tip`, `tips`, `pairs` (ids de receitas que combinam) e `video` (a cena animada).
   Se usares um alimento novo, junta os valores por 100 g a `tools/foods.py`.
2. **Gera o `recipes.json`** (recalcula as macros por dose):
   ```bash
   python3 tools/recipes_src.py
   ```
3. **Gera o vídeo, o poster e a miniatura** (precisa de Python com Playwright e de ffmpeg):
   ```bash
   pip install playwright && playwright install chromium   # só da primeira vez
   python3 tools/render_all.py <id> --preview   # opcional: fotogramas de amostra em .frames/<id>/
   python3 tools/render_all.py <id>             # videos/<id>.mp4 + media/<id>.jpg + media/<id>-thumb.webp
   ```
   Para usar o Chrome do sistema: `CHROME=/usr/bin/google-chrome python3 tools/render_all.py <id>`.
4. **Experimenta localmente:** `python3 -m http.server 8000` e abre `http://localhost:8000/`.
5. Faz commit e push. Quem já tem a app recebe a receita nova na próxima abertura com internet.

Notas:
- Se tiveres um vídeo feito de outra forma, põe-no em `videos/<id>.mp4` e corre `python3 tools/make_media.py <id> --reencode` para o comprimir (H.264, `faststart`) e gerar o poster e a miniatura.
- Também podes editar o `recipes.json` à mão; os campos que a app usa são os de cima mais `macrosPerServing` (`kcal`, `protein`, `carbs`, `fat`) e, opcionalmente, `macroBreakdownWholeRecipe`. O campo `video` só serve para gerar o vídeo.
- Se mudares `index.html`, `styles.css` ou `app.js`, a app atualiza-se sozinha (na abertura seguinte). Se quiseres limpar as caches antigas de todos, aumenta `VERSION` em `sw.js`.
- Mantém cada vídeo pequeno (os atuais têm 0,7 a 1,8 MB); o GitHub recusa ficheiros com mais de 100 MB e avisa acima de 50 MB.

As macros são estimativas a partir dos ingredientes crus e variam com as marcas e o tamanho dos ingredientes.
