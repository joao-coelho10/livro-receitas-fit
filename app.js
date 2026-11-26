/* Livro de Receitas Fit — app sem build (JavaScript simples).
   Lê recipes.json; tudo o resto é gerado a partir dos dados. */
(() => {
'use strict';

const VIDEO_CACHE = 'rf-videos-v3'; // tem de ser igual ao sw.js
const MEDIA_CACHE = 'rf-media-v2';
const PROTEIN_COLORS = { 'Frango/Peru': '#F2B53A', 'Vaca/Porco': '#B0585A', 'Ovos/Queijo': '#F6D77A', 'Vegetariano/Leguminosas': '#5DA543', 'Peixe': '#F7896B' };
const SORTS = [
  ['p100', 'Proteína por 100 kcal'], ['kcal', 'Menos calorias'], ['protein', 'Mais proteína'], ['time', 'Mais rápidas'], ['az', 'Nome (A–Z)'],
];

/* ---------- utilitários ---------- */
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));
const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const norm = (s) => String(s || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
const fmt1 = (n) => n.toFixed(1).replace('.', ',');
const fmt2 = (n) => n.toFixed(2).replace('.', ',');
const store = {
  get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* modo privado */ } },
};
const abs = (rel) => new URL(rel, location.href).href;
const icon = {
  search: '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>',
  x: '<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg>',
  heart: '<svg viewBox="0 0 24 24"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/></svg>',
  clock: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/><path d="M12 8v4l2.5 2.5"/></svg>',
  flame: '<svg viewBox="0 0 24 24"><path d="M12 21c-4 0-6.5-2.6-6.5-6 0-3.8 3.3-5.6 4.2-9.5 2.9 1.6 4.3 4.3 4.3 6.6 1-.6 1.6-1.6 1.8-2.8 1.6 1.4 2.7 3.6 2.7 5.7 0 3.4-2.5 6-6.5 6z"/></svg>',
  users: '<svg viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.5"/><path d="M3 20c.6-3.4 3-5.5 6-5.5s5.4 2.1 6 5.5M16 4.8a3.5 3.5 0 0 1 0 6.4M18 14.8c1.6.8 2.7 2.6 3 5.2"/></svg>',
  chef: '<svg viewBox="0 0 24 24"><path d="M7 14.5V20h10v-5.5M7 14.5A4 4 0 1 1 8.6 7a4 4 0 0 1 6.8 0A4 4 0 1 1 17 14.5z"/></svg>',
  down: '<svg viewBox="0 0 24 24"><path d="M12 4v11m0 0l-4-4m4 4l4-4M5 20h14"/></svg>',
  check: '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
  share: '<svg viewBox="0 0 24 24"><path d="M12 15V4m0 0L8 8m4-4l4 4M5 13v6h14v-6"/></svg>',
  chev: '<svg class="chev" viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg>',
  left: '<svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg>',
  right: '<svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg>',
  home: '<svg viewBox="0 0 24 24"><path d="M4 11l8-6.5 8 6.5M6 9.5V20h12V9.5"/><path d="M10 20v-5h4v5"/></svg>',
  leaf: '<svg viewBox="0 0 24 24"><path d="M5 19c0-8 5-13 14-14 0 9-5 14-13 14"/><path d="M5 19l7-7"/></svg>',
  folder: '<svg viewBox="0 0 24 24"><path d="M3.5 7.5a2 2 0 0 1 2-2h4l2 2h7a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-13a2 2 0 0 1-2-2z"/><path d="M12 11v5M9.5 13.5h5"/></svg>',
  edit: '<svg viewBox="0 0 24 24"><path d="M4 20h4l10.5-10.5a2.8 2.8 0 0 0-4-4L4 16z"/></svg>',
  trash: '<svg viewBox="0 0 24 24"><path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/></svg>',
};

let toastTimer;
function toast(msg) {
  const t = $('#toast'); t.textContent = msg; t.classList.add('show');
  clearTimeout(toastTimer); toastTimer = setTimeout(() => t.classList.remove('show'), 2600);
}

/* ---------- dados ---------- */
let BOOK = {}, RECIPES = [], BY_ID = {}, HAY = {};
let PROTEINS = [], MEALS = [];

function prepare(data) {
  BOOK = data.book || {};
  PROTEINS = BOOK.proteinTypes || [];
  MEALS = BOOK.mealTypes || [];
  RECIPES = (data.recipes || []).map((r) => {
    const m = r.macrosPerServing || {};
    return Object.assign({}, r, {
      kcal: m.kcal || 0, p: m.protein || 0, c: m.carbs || 0, f: m.fat || 0,
      pairs: r.pairs || [], tags: r.tags || [], tips: r.tips || [], steps: r.steps || [], ingredients: r.ingredients || [],
      // recipes.json traz videoFile/poster/thumb vazios enquanto o vídeo ainda não foi gerado
      hasVideo: r.videoFile !== '',
      videoSrc: r.videoFile === undefined ? 'videos/' + r.id + '.mp4' : r.videoFile,
      posterSrc: r.poster === undefined ? 'media/' + r.id + '.jpg' : r.poster,
      thumbSrc: r.thumb || (r.thumb === '' ? 'icons/icon-192.png' : 'media/' + r.id + '-thumb.webp'),
      need: Array.from(new Set((r.ingredients || []).filter((i) => i.food && !/opcional/i.test(i.n || '')).map((i) => i.food))),
    });
  });
  BY_ID = {}; HAY = {};
  RECIPES.forEach((r) => {
    BY_ID[r.id] = r;
    HAY[r.id] = norm([r.title, r.short, r.protein, r.meal, r.tags.join(' '), r.ingredients.map((i) => i.t || i.n || '').join(' ')].join(' '));
  });
  RECIPES.forEach((r) => { if (!PROTEINS.includes(r.protein)) PROTEINS.push(r.protein); if (!MEALS.includes(r.meal)) MEALS.push(r.meal); });
}

/* ---------- formatação (igual à Page) ---------- */
function frac(n) {
  const q = Math.round(n * 4) / 4, whole = Math.floor(q), rest = q - whole;
  const sym = rest === 0.25 ? '¼' : rest === 0.5 ? '½' : rest === 0.75 ? '¾' : '';
  if (whole === 0) return sym || '0';
  return String(whole) + sym;
}
function fmtIng(i, f) {
  if (i.t) return i.t;
  const q = (i.q || 0) * f;
  let n = i.n || '';
  n = n.replace(/\((\d+) latas?\)/, (_m, k) => { const c = Number(k) * f; return '(' + frac(c) + (c > 1 ? ' latas)' : ' lata)'); });
  if (i.u === 'g') return String(q >= 50 ? Math.round(q / 5) * 5 : Math.round(q)) + ' g ' + n;
  if (i.u === 'un') return frac(q) + ' ' + (q > 1 && i.np ? i.np : n);
  return frac(q) + ' ' + i.u + ' ' + n;
}
const totalMin = (r) => (r.handsOn || 0) + (r.ovenMax || 0);
const timeText = (r) => totalMin(r) + ' min' + (String(r.oven || '').indexOf('frio') >= 0 ? ' + frio' : '');
const p100 = (r) => (r.kcal > 0 ? (r.p / r.kcal) * 100 : 0);
const plural = (n, one, many) => n + ' ' + (n === 1 ? one : many);

/* ---------- favoritas e vídeos guardados ---------- */
/* Coleções: 'fav' (Favoritas, fixa) + as que o utilizador cria. Migra as favoritas antigas (rf-favs). */
const COLS = (() => {
  const saved = store.get('rf-cols', null);
  if (saved && Array.isArray(saved) && saved.length && saved[0].id === 'fav') return saved;
  return [{ id: 'fav', name: 'Favoritas', ids: store.get('rf-favs', []) }];
})();
const saveCols = () => { store.set('rf-cols', COLS); store.set('rf-favs', COLS[0].ids); };
const colById = (id) => COLS.find((c) => c.id === id);
const inCol = (cid, rid) => { const c = colById(cid); return !!c && c.ids.indexOf(rid) >= 0; };
const isFav = (id) => inCol('fav', id);
const colsOf = (rid) => COLS.filter((c) => c.ids.indexOf(rid) >= 0);
function setInCol(cid, rid, on) {
  const c = colById(cid); if (!c) return;
  const i = c.ids.indexOf(rid);
  if (on && i < 0) c.ids.unshift(rid); else if (!on && i >= 0) c.ids.splice(i, 1);
  saveCols(); syncFavButtons(rid);
}
function syncFavButtons(rid) {
  $$('[data-fav="' + rid + '"]').forEach((b) => b.setAttribute('aria-pressed', String(isFav(rid))));
  const n = colsOf(rid).filter((c) => c.id !== 'fav').length;
  $$('[data-cols="' + rid + '"]').forEach((b) => { b.classList.toggle('has', n > 0); const l = b.querySelector('.lbl'); if (l) l.textContent = n ? 'Em ' + plural(n, 'coleção', 'coleções') : 'Coleções'; });
}
function toggleFav(id) {
  const on = !isFav(id); setInCol('fav', id, on);
  toast(on ? 'Guardada nas favoritas' : 'Removida das favoritas');
}
function newCol(name) {
  name = String(name || '').trim().slice(0, 40); if (!name) return null;
  const c = { id: 'c' + Date.now().toString(36), name, ids: [] }; COLS.push(c); saveCols(); return c;
}

/* Folha inferior (bottom sheet) genérica */
function openSheet(html, onReady) {
  closeSheet();
  const back = document.createElement('div'); back.className = 'sheet-back'; back.id = 'sheet';
  back.innerHTML = '<div class="sheet" role="dialog" aria-modal="true">' + '<div class="grab" aria-hidden="true"></div>' + html + '</div>';
  document.body.appendChild(back);
  requestAnimationFrame(() => back.classList.add('open'));
  back.addEventListener('click', (e) => { if (e.target === back || e.target.closest('[data-close]')) closeSheet(); });
  const sh = back.querySelector('.sheet');
  if (onReady) onReady(sh);
  const f = sh.querySelector('input,button'); if (f && f.tagName === 'INPUT' && !matchMedia('(pointer:coarse)').matches) f.focus();
  return sh;
}
function closeSheet() { const s = $('#sheet'); if (s) s.remove(); }
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeSheet(); });
function colSheet(rid) {
  const r = BY_ID[rid]; if (!r) return;
  const draw = (sh) => {
    sh.querySelector('#colList').innerHTML = COLS.map((c) => '<label class="check-row"><input type="checkbox" data-col="' + esc(c.id) + '"' + (inCol(c.id, rid) ? ' checked' : '') + '><span class="cbox">' + icon.check + '</span><span class="nm">' + (c.id === 'fav' ? '♥ ' : '') + esc(c.name) + '</span><span class="small">' + c.ids.length + '</span></label>').join('');
  };
  openSheet('<h2>Guardar em…</h2><p class="small sheet-sub">' + esc(r.title) + '</p><div id="colList" class="check-list"></div>' +
    '<form class="new-col" id="newColForm"><input id="newColName" maxlength="40" placeholder="Nova coleção (ex.: Jantares rápidos)" aria-label="Nome da nova coleção" autocomplete="off"><button class="btn" type="submit">Criar</button></form>' +
    '<button class="btn primary full" data-close>Feito</button>', (sh) => {
    draw(sh);
    sh.querySelector('#colList').addEventListener('change', (e) => { const cb = e.target.closest('[data-col]'); if (cb) { setInCol(cb.dataset.col, rid, cb.checked); draw(sh); } });
    sh.querySelector('#newColForm').addEventListener('submit', (e) => {
      e.preventDefault(); const inp = sh.querySelector('#newColName'); const c = newCol(inp.value);
      if (c) { setInCol(c.id, rid, true); inp.value = ''; draw(sh); toast('Coleção “' + c.name + '” criada'); }
    });
  });
}
function nameSheet(title, value, okLabel, cb) {
  openSheet('<h2>' + esc(title) + '</h2><form id="nameForm" class="name-form"><input id="nameInp" maxlength="40" value="' + esc(value || '') + '" aria-label="Nome" autocomplete="off" required>' +
    '<div class="sheet-actions"><button type="button" class="btn" data-close>Cancelar</button><button class="btn primary" type="submit">' + esc(okLabel) + '</button></div></form>', (sh) => {
    sh.querySelector('#nameForm').addEventListener('submit', (e) => { e.preventDefault(); const v = sh.querySelector('#nameInp').value.trim(); if (v) { closeSheet(); cb(v); } });
  });
}
function confirmSheet(title, text, okLabel, cb) {
  openSheet('<h2>' + esc(title) + '</h2><p class="sheet-sub">' + esc(text) + '</p><div class="sheet-actions"><button class="btn" data-close>Cancelar</button><button class="btn danger" id="okBtn">' + esc(okLabel) + '</button></div>',
    (sh) => { sh.querySelector('#okBtn').addEventListener('click', () => { closeSheet(); cb(); }); });
}

let SAVED = new Set();
async function refreshSaved() {
  SAVED = new Set();
  if (!('caches' in window)) return;
  try {
    const c = await caches.open(VIDEO_CACHE);
    const current = new Set(RECIPES.map((r) => abs(r.videoSrc)));
    for (const req of await c.keys()) {
      if (current.size && !current.has(req.url)) await c.delete(req); // versão antiga de um vídeo (outro ?v=)
      else SAVED.add(req.url);
    }
  } catch (e) { /* sem cache */ }
}
const isSaved = (r) => SAVED.has(abs(r.videoSrc));
async function saveRecipe(r) {
  if (!r.hasVideo) throw new Error('O vídeo desta receita ainda está a ser preparado.');
  if (!('caches' in window)) throw new Error('Este navegador não permite guardar para offline.');
  const vc = await caches.open(VIDEO_CACHE);
  const url = abs(r.videoSrc);
  if (!(await vc.match(url))) {
    const res = await fetch(url, { cache: 'no-store' });
    if (!res.ok) throw new Error('Falhou o download do vídeo (' + res.status + ').');
    await vc.put(url, res);
  }
  const mc = await caches.open(MEDIA_CACHE);
  await Promise.all([r.posterSrc, r.thumbSrc].map(async (u) => {
    try { if (!(await mc.match(abs(u)))) { const res = await fetch(abs(u)); if (res.ok) await mc.put(abs(u), res); } } catch (e) { /* opcional */ }
  }));
  SAVED.add(url);
}
async function unsaveRecipe(r) {
  const vc = await caches.open(VIDEO_CACHE);
  await vc.delete(abs(r.videoSrc));
  SAVED.delete(abs(r.videoSrc));
}
const autoSave = () => store.get('rf-autosave', true);

/* ---------- estado da lista ---------- */
/* Estado da lista de receitas. Regras (simples e previsíveis):
   - Refeição e Proteína: escolha ÚNICA por grupo. Tocar noutra opção troca; tocar na escolhida (ou em “Todas”) volta a “Todas”.
   - Mais filtros: podes juntar vários (têm de se cumprir todos); tocar liga/desliga.
   - O número em cada opção é quantas receitas vais ver se a escolheres (com os outros filtros e a pesquisa).
   - O estado fica no endereço (#/?r=…&p=…&f=…&q=…), por isso voltar atrás repõe a lista igual; a ordenação fica guardada.
   - O “O que tenho em casa” tem estado próprio e NUNCA mexe nesta lista. */
const F = { q: '', meal: '', prot: '', quick: new Set(), sort: store.get('rf-sort', 'p100'), shown: 0 };
const PAGE = 24;
const QUICK = [
  ['rapida', 'Até 30 min', (r) => totalMin(r) <= 30],
  ['saciante', 'Saciante / volume', (r) => r.volume],
  ['salada', 'Saladas', (r) => r.salad],
  ['facil', 'Fácil', (r) => r.difficulty === 'Fácil'],
  ['semgluten', 'Sem glúten', (r) => r.glutenFree],
  ['veg', 'Vegetariana', (r) => r.vegetarian],
  ['prep', 'Meal prep', (r) => r.mealPrep],
  ['congela', 'Congela bem', (r) => r.freezer],
  ['barata', 'Económica (€)', (r) => r.cost === '€'],
];
const QBY = Object.fromEntries(QUICK.map((q) => [q[0], q]));
function filterList(st) {
  const toks = norm(st.q).split(/\s+/).filter(Boolean);
  return RECIPES.filter((r) => matchQ(r, toks) && (!st.meal || r.meal === st.meal) && (!st.prot || r.protein === st.prot) &&
    Array.from(st.quick).every((k) => QBY[k] && QBY[k][2](r)));
}
const stateWith = (patch) => Object.assign({ q: F.q, meal: F.meal, prot: F.prot, quick: new Set(F.quick) }, patch);
function listHash() {
  const q = [];
  if (F.meal) q.push('r=' + encodeURIComponent(F.meal));
  if (F.prot) q.push('p=' + encodeURIComponent(F.prot));
  if (F.quick.size) q.push('f=' + Array.from(F.quick).join(','));
  if (F.q.trim()) q.push('q=' + encodeURIComponent(F.q.trim()));
  return '#/' + (q.length ? '?' + q.join('&') : '');
}
function readListHash(hash) {
  const i = hash.indexOf('?'); const sp = new URLSearchParams(i >= 0 ? hash.slice(i + 1) : '');
  F.meal = MEALS.includes(sp.get('r')) ? sp.get('r') : '';
  F.prot = PROTEINS.includes(sp.get('p')) ? sp.get('p') : '';
  F.quick = new Set((sp.get('f') || '').split(',').filter((k) => QBY[k]));
  F.q = sp.get('q') || '';
}
function syncListHash() {
  const h = listHash();
  if (location.hash !== h && (location.hash || '#/') !== h) { history.replaceState(null, '', h); currentHash = h; }
  const tab = $('#tabbar a[data-tab="home"]'); if (tab) tab.setAttribute('href', h);
}
const tokens = () => norm(F.q).split(/\s+/).filter(Boolean);
function matchQ(r, toks) { return toks.every((t) => HAY[r.id].indexOf(t) >= 0); }
function sortList(list) {
  const s = list.slice();
  if (F.sort === 'p100') s.sort((a, b) => p100(b) - p100(a));
  if (F.sort === 'kcal') s.sort((a, b) => a.kcal - b.kcal);
  if (F.sort === 'protein') s.sort((a, b) => b.p - a.p);
  if (F.sort === 'time') s.sort((a, b) => totalMin(a) - totalMin(b));
  if (F.sort === 'az') s.sort((a, b) => a.title.localeCompare(b.title, 'pt'));
  return s;
}

/* ---------- componentes ---------- */
function cardHTML(r) {
  return '<a class="card" href="#/receita/' + esc(r.id) + '">' +
    '<div class="thumb"><img loading="lazy" decoding="async" src="' + esc(r.thumbSrc) + '" alt="" onerror="this.onerror=null;this.src=\'icons/icon-192.png\'"></div>' +
    '<div class="body"><span class="kicker">' + esc(r.meal) + '</span><h3>' + esc(r.title) + '</h3>' +
    '<div class="meta"><span><b>' + r.kcal + '</b> kcal</span><span><b>' + r.p + ' g</b> proteína</span><span>' + esc(timeText(r)) + '</span>' +
    (isSaved(r) ? '<span class="saved-dot" title="Vídeo disponível offline">' + icon.check + 'offline</span>' : '') + '</div>' +
    '<div class="badges"><span class="badge">' + fmt1(p100(r)) + ' g / 100 kcal</span>' + (r.cost ? '<span class="badge soft" title="Custo aproximado por dose">' + esc(r.cost) + '</span>' : '') +
    (r.mealPrep ? '<span class="badge soft">meal prep</span>' : '') + '</div></div>' +
    '</a><button class="fav-btn" data-fav="' + esc(r.id) + '" aria-pressed="' + isFav(r.id) + '" aria-label="Favorita: ' + esc(r.short || r.title) + '">' + icon.heart + '</button>' +
    '<button class="col-btn' + (colsOf(r.id).some((c) => c.id !== 'fav') ? ' has' : '') + '" data-cols="' + esc(r.id) + '" aria-label="Guardar em coleção: ' + esc(r.short || r.title) + '">' + icon.folder + '</button>';
}
const cardWrap = (r) => '<div class="card-wrap" data-rid="' + esc(r.id) + '">' + cardHTML(r) + '</div>';
function rowHTML(r, detail, role) {
  return '<a class="row" href="#/receita/' + esc(r.id) + '"><img loading="lazy" src="' + esc(r.thumbSrc) + '" alt="" onerror="this.onerror=null;this.src=\'icons/icon-192.png\'">' +
    '<div class="t">' + (role ? '<span class="role">' + esc(role) + '</span>' : '') + '<b>' + esc(r.title) + '</b><span>' + esc(detail) + '</span></div>' + icon.chev + '</a>';
}
function selectHTML(id, options, value, label) {
  return '<div class="select"><select id="' + id + '" aria-label="' + esc(label) + '">' +
    options.map((o) => '<option value="' + esc(o[0]) + '"' + (String(o[0]) === String(value) ? ' selected' : '') + '>' + esc(o[1]) + '</option>').join('') + '</select></div>';
}

/* ---------- vista: lista ---------- */
function renderHome(main) {
  main.innerHTML =
    '<div class="hero"><h1>Livro de Receitas Fit</h1><p>' + plural(RECIPES.length, 'receita', 'receitas') + ' · muita proteína, poucas calorias</p></div>' +
    '<a class="casa-cta" href="#/casa">' + icon.home + '<span><b>O que tenho em casa?</b><small>Escolhe ingredientes e vê o que dá para fazer</small></span>' + icon.chev + '</a>' +
    '<div class="search">' + icon.search + '<input id="q" type="search" inputmode="search" enterkeyhint="search" autocomplete="off" placeholder="Pesquisa: cottage, batata…" aria-label="Pesquisar receitas" value="' + esc(F.q) + '">' +
    '<button class="clear-q" id="clearQ" aria-label="Limpar pesquisa"' + (F.q ? '' : ' hidden') + '>' + icon.x + '</button></div>' +
    '<div id="filters">' +
    '<div class="filter-label" id="lblMeal">Refeição</div><div class="chips" id="chipsMeal" role="radiogroup" aria-labelledby="lblMeal"></div>' +
    '<div class="filter-label" id="lblProt">Proteína</div><div class="chips" id="chipsProt" role="radiogroup" aria-labelledby="lblProt"></div>' +
    '<div class="filter-label" id="lblQuick">Mais filtros <span>podes juntar vários</span></div><div class="chips" id="chipsQuick" role="group" aria-labelledby="lblQuick"></div>' +
    '</div>' +
    '<div class="toolbar"><div class="count" id="count" aria-live="polite"></div>' + selectHTML('sort', SORTS, F.sort, 'Ordenar por') + '</div>' +
    '<div id="results"></div>';
  const q = $('#q', main);
  q.addEventListener('input', () => { F.q = q.value; $('#clearQ').hidden = !F.q; updateHome(true); });
  q.addEventListener('keydown', (e) => { if (e.key === 'Enter') q.blur(); });
  $('#clearQ', main).addEventListener('click', () => { F.q = ''; q.value = ''; $('#clearQ').hidden = true; updateHome(true); q.focus(); });
  $('#sort', main).addEventListener('change', (e) => { F.sort = e.target.value; store.set('rf-sort', F.sort); updateHome(true); });
  // um só ouvinte, num elemento novo a cada render (antes ficava no <main> e acumulava-se a cada visita)
  $('#filters', main).addEventListener('click', (e) => {
    const c = e.target.closest('.chip[data-dim]'); if (!c) return;
    const v = c.dataset.v, dim = c.dataset.dim;
    if (dim === 'quick') { if (F.quick.has(v)) F.quick.delete(v); else F.quick.add(v); }
    else { F[dim] = (v === '' || F[dim] === v) ? '' : v; }
    updateHome(true);
  });
  $('#results', main).addEventListener('click', (e) => {
    if (e.target.closest('#more')) { F.shown += PAGE; drawResults(); }
    if (e.target.closest('#clearAll2')) clearFilters();
  });
  updateHome(false);
  $$('#filters .chips', main).forEach((row) => { const on = row.querySelector('.chip[aria-pressed="true"]:not([data-v=""])'); if (on) row.scrollLeft = Math.max(0, on.offsetLeft - 20); });
}
function clearFilters() {
  F.q = ''; F.meal = ''; F.prot = ''; F.quick.clear();
  const q = $('#q'); if (q) { q.value = ''; $('#clearQ').hidden = true; }
  updateHome(true);
}
let RESULTS = [];
function updateHome(reset) {
  if (reset || !F.shown) F.shown = PAGE;
  RESULTS = sortList(filterList(F));
  const n = (patch) => filterList(stateWith(patch)).length;
  const chip = (dim, v, label, cnt, on, dot) => '<button class="chip' + (cnt === 0 && !on ? ' zero' : '') + '" data-dim="' + dim + '" data-v="' + esc(v) + '" ' +
    (dim === 'quick' ? 'aria-pressed="' + on + '"' : 'role="radio" aria-checked="' + on + '" aria-pressed="' + on + '"') + '>' +
    (dim === 'quick' ? '<span class="tick" aria-hidden="true">' + icon.check + '</span>' : '') +
    (dot ? '<i class="dot" style="background:' + dot + '"></i>' : '') + esc(label) + (cnt != null ? ' <span class="n">' + cnt + '</span>' : '') + '</button>';
  $('#chipsMeal').innerHTML = chip('meal', '', 'Todas', n({ meal: '' }), !F.meal) + MEALS.map((m) => chip('meal', m, m, n({ meal: m }), F.meal === m)).join('');
  $('#chipsProt').innerHTML = chip('prot', '', 'Todas', n({ prot: '' }), !F.prot) + PROTEINS.map((p) => chip('prot', p, p, n({ prot: p }), F.prot === p, PROTEIN_COLORS[p])).join('');
  $('#chipsQuick').innerHTML = QUICK.map((qq) => { const on = F.quick.has(qq[0]); const st = new Set(F.quick); st.add(qq[0]); return chip('quick', qq[0], qq[1], on ? RESULTS.length : n({ quick: st }), on); }).join('');
  const filtered = F.q.trim() || F.meal || F.prot || F.quick.size;
  $('#count').innerHTML = '<b>' + plural(RESULTS.length, 'receita', 'receitas') + '</b>' + (filtered ? '<button class="link-btn" id="clearAll">Limpar filtros</button>' : '');
  const ca = $('#clearAll'); if (ca) ca.addEventListener('click', clearFilters);
  drawResults();
  syncListHash();
}
function drawResults() {
  const box = $('#results'); if (!box) return;
  if (!RESULTS.length) {
    box.innerHTML = '<div class="empty"><div class="empty-ico" aria-hidden="true">🔎</div><h3>Nenhuma receita encontrada</h3><p>Não há receitas' + (F.q.trim() ? ' com “' + esc(F.q.trim()) + '”' : '') + ' com estes filtros juntos.</p><p><button class="btn" id="clearAll2">Limpar filtros</button></p></div>';
    return;
  }
  const list = RESULTS.slice(0, F.shown);
  box.innerHTML = '<div class="grid">' + list.map(cardWrap).join('') + '</div>' +
    (RESULTS.length > list.length ? '<button class="btn full more" id="more">Mostrar mais ' + Math.min(PAGE, RESULTS.length - list.length) + ' <span class="small">(' + list.length + ' de ' + RESULTS.length + ')</span></button>' : '');
  const more = $('#more');
  if (more && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver((en) => { if (en[0].isIntersecting) { io.disconnect(); F.shown += PAGE; drawResults(); } }, { root: $('#main'), rootMargin: '400px' });
    io.observe(more);
  }
}

/* ---------- vista: favoritas e coleções ---------- */
function renderFav(main, cid) {
  const col = colById(cid) || COLS[0];
  const list = col.ids.map((id) => BY_ID[id]).filter(Boolean);
  main.innerHTML = '<div class="hero"><h1>Favoritas e coleções</h1><p>Agrupa as receitas como quiseres. Toque longo num cartão (ou no ícone de pasta) para guardar.</p></div>' +
    '<div class="chips" id="colChips" role="tablist" aria-label="Coleções">' + COLS.map((c) => '<a class="chip" role="tab" href="#/favoritas' + (c.id === 'fav' ? '' : '/' + esc(c.id)) + '" aria-selected="' + (c.id === col.id) + '" aria-pressed="' + (c.id === col.id) + '">' + (c.id === 'fav' ? '♥ ' : '') + esc(c.name) + ' <span class="n">' + c.ids.filter((id) => BY_ID[id]).length + '</span></a>').join('') +
    '<button class="chip add" id="addCol">+ Nova coleção</button></div>' +
    '<div class="col-head"><h2>' + (col.id === 'fav' ? '♥ ' : '') + esc(col.name) + ' <small>' + plural(list.length, 'receita', 'receitas') + '</small></h2>' +
    (col.id === 'fav' ? '' : '<div class="col-actions"><button class="icon-btn" id="renCol" aria-label="Mudar o nome da coleção">' + icon.edit + '</button><button class="icon-btn" id="delCol" aria-label="Apagar coleção">' + icon.trash + '</button></div>') + '</div>' +
    (list.length ? '<div class="grid">' + list.map(cardWrap).join('') + '</div>'
      : '<div class="empty"><div class="empty-ico" aria-hidden="true">' + (col.id === 'fav' ? '♥' : '📁') + '</div><h3>' + (col.id === 'fav' ? 'Ainda não tens favoritas' : 'Coleção vazia') + '</h3><p>' +
        (col.id === 'fav' ? 'Toca no ♥ de uma receita para a guardares aqui.' : 'Numa receita, toca em “Coleções” (ou faz um toque longo no cartão) e escolhe “' + esc(col.name) + '”.') + '</p><p><a class="btn primary" href="#/">Ver receitas</a></p></div>');
  $('#addCol').onclick = () => nameSheet('Nova coleção', '', 'Criar', (v) => { const c = newCol(v); if (c) location.hash = '#/favoritas/' + c.id; });
  const rn = $('#renCol'); if (rn) rn.onclick = () => nameSheet('Mudar o nome', col.name, 'Guardar', (v) => { col.name = v.slice(0, 40); saveCols(); renderFav(main, col.id); $('#topTitle').textContent = col.name; });
  const dl = $('#delCol'); if (dl) dl.onclick = () => confirmSheet('Apagar “' + col.name + '”?', 'As receitas não são apagadas, só a coleção.', 'Apagar', () => { COLS.splice(COLS.indexOf(col), 1); saveCols(); toast('Coleção apagada'); location.hash = '#/favoritas'; });
  const on = $('#colChips [aria-selected="true"]'); if (on) on.scrollIntoView({ inline: 'center', block: 'nearest' });
}

/* ---------- vista: receita ---------- */
const DOSES = {}; const CHECKED = {};
function renderRecipe(main, r) {
  const doses = DOSES[r.id] || r.servings;
  const f = doses / r.servings;
  const checked = CHECKED[r.id] || (CHECKED[r.id] = new Set());
  const pairIds = r.pairs.filter((id) => BY_ID[id]);
  RECIPES.forEach((x) => { if (x.id !== r.id && x.pairs.indexOf(r.id) >= 0 && pairIds.indexOf(x.id) < 0) pairIds.push(x.id); });
  const br = r.macroBreakdownWholeRecipe || [];
  const tot = br.reduce((a, b) => [a[0] + (b.kcal || 0), a[1] + (b.protein || 0)], [0, 0]);
  const maxKcal = 700, maxP = 60;
  const macro = (v, unit, label, w, c) => '<div class="macro"><b>' + v + '</b><span>' + unit + label + '</span><i style="--w:' + Math.min(100, w) + '%;--c:' + c + '"></i></div>';
  main.innerHTML =
    (r.hasVideo ? '<div class="video-wrap"><video id="vid" playsinline webkit-playsinline preload="none" poster="' + esc(r.posterSrc) + '" src="' + esc(r.videoSrc) + '" aria-label="Vídeo passo a passo: ' + esc(r.title) + '"></video>' +
    '<button class="play" id="playBtn" aria-label="Ver vídeo passo a passo"><img src="' + esc(r.posterSrc) + '" alt="" onerror="this.remove()"><span><svg viewBox="0 0 24 24"><path d="M8 5.5v13l11-6.5z"/></svg>Ver vídeo passo a passo</span></button></div>'
     : '<div class="video-soon"><span>' + icon.clock + '</span><b>Vídeo narrado a caminho</b><small>A receita está completa aqui em baixo; o vídeo chega numa próxima atualização.</small></div>') +
    '<div class="r-head"><span class="kicker">' + esc(r.meal) + ' · ' + esc(r.protein) + '</span><h1>' + esc(r.title) + '</h1>' +
    '<div class="facts"><span class="fact">' + icon.clock + esc(r.handsOn) + ' min prep.</span>' +
    '<span class="fact">' + icon.flame + esc(r.temp ? r.temp + ' °C · ' + r.oven : r.oven) + '</span>' +
    '<span class="fact">' + icon.users + esc(plural(r.servings, 'dose', 'doses')) + '</span>' +
    (r.difficulty ? '<span class="fact">' + icon.chef + esc(r.difficulty) + '</span>' : '') +
    (r.cost ? '<span class="fact" title="Custo aproximado por dose">' + esc(r.cost) + (r.costPerServing ? ' · ~' + fmt2(r.costPerServing) + ' €/dose' : '') + '</span>' : '') + '</div></div>' +
    '<div class="actions">' +
    '<a class="btn primary full" href="#/receita/' + esc(r.id) + '/cozinha">' + icon.chef + 'Modo cozinha</a>' +
    '<button class="btn" data-fav="' + esc(r.id) + '" aria-pressed="' + isFav(r.id) + '">' + icon.heart + 'Favorita</button>' +
    '<button class="btn' + (colsOf(r.id).some((c) => c.id !== 'fav') ? ' has' : '') + '" data-cols="' + esc(r.id) + '">' + icon.folder + '<span class="lbl">' + (function () { const n = colsOf(r.id).filter((c) => c.id !== 'fav').length; return n ? 'Em ' + plural(n, 'coleção', 'coleções') : 'Coleções'; })() + '</span></button>' +
    '<button class="btn" id="saveBtn"' + (r.hasVideo ? '' : ' disabled title="Vídeo em preparação"') + '>' + (isSaved(r) ? icon.check + 'Guardada offline' : icon.down + 'Guardar offline') + '</button>' +
    '<button class="btn" id="shareBtn">' + icon.share + 'Partilhar</button></div>' +
    '<section class="sec"><h2>Macros por dose <small>estimativa</small></h2><div class="macros">' +
    macro(r.kcal, '', 'kcal', r.kcal / maxKcal * 100, 'var(--orange)') + macro(r.p + ' g', '', 'proteína', r.p / maxP * 100, 'var(--yellow)') +
    macro(r.c + ' g', '', 'hidratos', r.c / 80 * 100, '#8CC7A1') + macro(r.f + ' g', '', 'gordura', r.f / 30 * 100, '#E9A15B') +
    (r.macrosPerServing && r.macrosPerServing.fiber != null ? macro(r.macrosPerServing.fiber + ' g', '', 'fibra', r.macrosPerServing.fiber / 12 * 100, '#7FB069') : '') + '</div>' +
    '<p class="note">Estimativa a partir dos ingredientes crus · ' + fmt1(p100(r)) + ' g de proteína por 100 kcal · 1 dose = 1/' + r.servings + ' da receita.</p></section>' +
    infoHTML(r) +
    '<section class="sec"><h2>Ingredientes <small>toca para riscar</small></h2><div class="panel">' +
    '<div class="stepper"><button id="dMinus" aria-label="Menos doses">−</button><output id="dOut" aria-live="polite">' + esc(plural(doses, 'dose', 'doses')) + '</output><button id="dPlus" aria-label="Mais doses">+</button>' +
    (doses !== r.servings ? '<button class="link-btn reset" id="dReset">Repor ' + r.servings + '</button>' : '') + '</div>' +
    '<ul class="ing">' + r.ingredients.map((i, k) => '<li class="' + (i.t ? 'free' : '') + (checked.has(k) ? ' done' : '') + '" data-k="' + k + '"' + (i.t ? '' : ' role="checkbox" tabindex="0" aria-checked="' + checked.has(k) + '"') + '><span class="box">' + icon.check + '</span><span>' + esc(fmtIng(i, f)) + '</span></li>').join('') + '</ul></div></section>' +
    '<section class="sec"><h2>Modo de preparação</h2><ol class="steps">' + r.steps.map((s) => '<li><b>' + esc(s.title) + '</b><p>' + esc(s.detail) + '</p></li>').join('') + '</ol>' +
    (r.tip ? '<div class="tip"><span>💡</span><span><b>Dica:</b> ' + esc(r.tip) + '</span></div>' : '') + '</section>' +
    (pairIds.length ? '<section class="sec"><h2>Combina com</h2><div class="list">' + pairIds.map((id) => { const x = BY_ID[id]; return rowHTML(x, x.meal + ' · ' + x.kcal + ' kcal · ' + x.p + ' g de proteína'); }).join('') + '</div></section>' : '') +
    (r.tips.length ? '<section class="sec"><h2>Mais dicas</h2><div class="panel"><ul class="bul">' + r.tips.map((t) => '<li>' + esc(t) + '</li>').join('') + '</ul></div></section>' : '') +
    (br.length ? '<section class="sec"><details class="panel"><summary>Como chegámos às macros</summary><table><thead><tr><th>Ingrediente</th><th class="n">kcal</th><th class="n">Proteína</th></tr></thead><tbody>' +
      br.map((b) => '<tr><td>' + esc(b.item) + (b.g ? ' <span class="small">(' + b.g + ' g)</span>' : '') + '</td><td class="n">' + b.kcal + '</td><td class="n">' + b.protein + ' g</td></tr>').join('') +
      '<tr class="tot"><td>Total da receita</td><td class="n">' + tot[0] + '</td><td class="n">' + tot[1] + ' g</td></tr></tbody></table><p class="note">Valores aproximados por 100 g de cada alimento cru. Variam com as marcas.</p></details></section>' : '') +
    '<div class="tags">' + r.tags.map((t) => '<a class="tag" href="#/?q=' + encodeURIComponent(t) + '">#' + esc(t) + '</a>').join('') + '</div>';

  const setDoses = (d) => { DOSES[r.id] = Math.max(1, Math.min(r.servings * 4, d)); const y = main.scrollTop; renderRecipe(main, r); main.scrollTop = y; };
  $('#dMinus').onclick = () => setDoses(doses - 1);
  $('#dPlus').onclick = () => setDoses(doses + 1);
  const dr = $('#dReset'); if (dr) dr.onclick = () => setDoses(r.servings);
  $$('.ing li[role=checkbox]', main).forEach((li) => {
    const tog = () => { const k = Number(li.dataset.k); if (checked.has(k)) checked.delete(k); else checked.add(k); li.classList.toggle('done'); li.setAttribute('aria-checked', String(checked.has(k))); };
    li.onclick = tog; li.onkeydown = (e) => { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); tog(); } };
  });
  const vid = $('#vid');
  if (vid) {
  $('#playBtn').onclick = () => { $('#playBtn').hidden = true; vid.controls = true; const pr = vid.play(); if (pr) pr.catch(() => {}); };
  vid.addEventListener('play', () => { if (autoSave() && !isSaved(r) && navigator.onLine) saveRecipe(r).catch(() => {}); }, { once: true });
  vid.addEventListener('error', () => { if (!navigator.onLine && !isSaved(r)) toast('Este vídeo ainda não está guardado para offline.'); });
  }
  const sb = $('#saveBtn');
  sb.onclick = async () => {
    sb.disabled = true;
    try {
      if (isSaved(r)) { await unsaveRecipe(r); toast('Vídeo removido do dispositivo'); }
      else { sb.innerHTML = icon.down + 'A guardar…'; await saveRecipe(r); toast('Receita e vídeo disponíveis offline'); }
    } catch (e) { toast(e.message || 'Não foi possível guardar.'); }
    sb.disabled = false; sb.innerHTML = isSaved(r) ? icon.check + 'Guardada offline' : icon.down + 'Guardar offline';
  };
  $('#shareBtn').onclick = async () => {
    const url = location.href.split('#')[0] + '#/receita/' + r.id;
    try {
      if (navigator.share) await navigator.share({ title: r.title, text: r.title + ' · ' + r.kcal + ' kcal, ' + r.p + ' g de proteína por dose', url });
      else { await navigator.clipboard.writeText(url); toast('Link copiado'); }
    } catch (e) { /* cancelado */ }
  };
}

function infoHTML(r) {
  const items = [];
  items.push(['⏱', 'Tempo total', timeText(r) + ' (' + (r.handsOn || 0) + ' min de preparação)']);
  if (r.storage) items.push(['🧊', 'Conservação', r.storage]);
  const flags = [];
  if (r.mealPrep) flags.push('boa para meal prep');
  if (r.freezer) flags.push('congela bem');
  if (r.glutenFree) flags.push('sem glúten');
  if (r.vegetarian) flags.push('vegetariana');
  if (flags.length) items.push(['✅', 'Bom saber', flags.join(' · ').replace(/^./, (c) => c.toUpperCase())]);
  return '<section class="sec"><div class="panel info">' + items.map((x) => '<div class="info-row"><span class="ico" aria-hidden="true">' + x[0] + '</span><div><b>' + esc(x[1]) + '</b><span>' + esc(x[2]) + '</span></div></div>').join('') + '</div></section>';
}

/* ---------- vista: o que tenho em casa ---------- */
const CASA = { sel: new Set(store.get('rf-casa', [])), pantry: store.get('rf-casa-despensa', true), q: '' };
const saveCasa = () => { store.set('rf-casa', Array.from(CASA.sel)); store.set('rf-casa-despensa', CASA.pantry); };
function foodsUsed() {
  const used = new Set(); RECIPES.forEach((r) => r.need.forEach((f) => used.add(f)));
  return used;
}
const foodLabel = (k) => (BOOK.foods && BOOK.foods[k] ? BOOK.foods[k].label : k);
function haveFood(k) {
  if (CASA.sel.has(k)) return { ok: true };
  if (CASA.pantry && BOOK.foods && BOOK.foods[k] && BOOK.foods[k].pantry) return { ok: true };
  for (const g of (BOOK.subs || [])) {
    if (g.indexOf(k) >= 0) { const alt = g.find((x) => x !== k && CASA.sel.has(x)); if (alt) return { ok: true, sub: alt }; }
  }
  return { ok: false };
}
function casaRank() {
  const out = [];
  RECIPES.forEach((r) => {
    if (!r.need.length) return;
    const missing = [], subs = []; let mine = 0;
    r.need.forEach((k) => { const h = haveFood(k); if (!h.ok) missing.push(k); else { if (CASA.sel.has(k) || h.sub) mine++; if (h.sub) subs.push([k, h.sub]); } });
    if (mine === 0 || missing.length > 2) return;
    out.push({ r, missing, subs, mine, share: mine / r.need.length });
  });
  out.sort((a, b) => a.missing.length - b.missing.length || b.share - a.share || p100(b.r) - p100(a.r));
  return out;
}
function renderCasa(main) {
  const used = foodsUsed();
  const groups = (BOOK.foodGroups || []).map((g) => [g, Object.keys(BOOK.foods || {}).filter((k) => BOOK.foods[k].group === g && used.has(k))]).filter((g) => g[1].length);
  main.innerHTML = '<div class="hero"><h1>O que tenho em casa</h1><p>Marca o que tens e eu digo-te o que dá para cozinhar.</p></div>' +
    '<div class="search">' + icon.search + '<input id="cq" type="search" autocomplete="off" enterkeyhint="search" placeholder="Procura: frango, ovos, batata…" aria-label="Procurar ingrediente" value="' + esc(CASA.q) + '"></div>' +
    '<label class="toggle casa-pantry">Tenho o básico da despensa<small>sal, pimenta, especiarias, azeite, alho, mostarda, mel, fermento…</small><span class="switch"><input type="checkbox" id="cPantry"' + (CASA.pantry ? ' checked' : '') + '><span></span></span></label>' +
    '<div class="casa-bar"><span id="cCount"></span><button class="link-btn" id="cClear">Limpar</button></div>' +
    '<div id="cGroups">' + groups.map((g) => '<div class="casa-group" data-group="' + esc(g[0]) + '"><div class="filter-label">' + esc(g[0]) + '</div><div class="chips wrap">' +
      g[1].map((k) => '<button class="chip" data-food="' + esc(k) + '" data-label="' + esc(norm(foodLabel(k))) + '"></button>').join('') + '</div></div>').join('') +
    '<p class="small" id="cNone" hidden>Nenhum ingrediente com esse nome.</p></div>' +
    '<section class="sec" id="cRes" aria-live="polite"></section>';
  const draw = () => {
    $$('[data-food]', main).forEach((b) => {
      const k = b.dataset.food, isP = BOOK.foods[k].pantry && CASA.pantry;
      const on = CASA.sel.has(k) || isP;
      b.setAttribute('aria-pressed', String(on)); b.disabled = isP;
      b.innerHTML = (on ? icon.check : '') + esc(foodLabel(k));
      b.title = isP ? 'Incluído no básico da despensa' : '';
    });
    const qn = norm(CASA.q.trim()); let any = false;
    $$('.casa-group', main).forEach((g) => {
      let vis = 0;
      $$('[data-food]', g).forEach((b) => { const show = !qn || b.dataset.label.indexOf(qn) >= 0; b.hidden = !show; if (show) vis++; });
      g.hidden = vis === 0; if (vis) any = true;
    });
    $('#cNone').hidden = any;
    $('#cCount').innerHTML = CASA.sel.size ? '<b>' + plural(CASA.sel.size, 'ingrediente escolhido', 'ingredientes escolhidos') + '</b>' : 'Ainda não escolheste nada';
    $('#cClear').hidden = !CASA.sel.size;
    const res = $('#cRes');
    if (!CASA.sel.size) { res.innerHTML = '<div class="empty"><h3>Toca nos ingredientes que tens</h3><p>Mostro primeiro as receitas que podes fazer já e depois as que só precisam de mais 1 ou 2 coisas.</p></div>'; return; }
    const list = casaRank();
    const sect = (title, items, note) => items.length ? '<h2 class="casa-h">' + title + ' <small>' + items.length + '</small></h2>' + (note ? '<p class="small" style="margin:-4px 0 10px">' + note + '</p>' : '') + '<div class="list">' + items.map((x) => {
      let d = x.r.meal + ' · ' + x.r.kcal + ' kcal · ' + x.r.p + ' g prot.';
      const miss = x.missing.length ? '<span class="miss">Falta: ' + esc(x.missing.map(foodLabel).join(', ')) + '</span>' : '';
      const sub = x.subs.length ? '<span class="subn">Troca: ' + esc(x.subs.map((s) => foodLabel(s[0]) + ' → ' + foodLabel(s[1]).toLowerCase()).join(', ')) + '</span>' : '';
      return '<a class="row" href="#/receita/' + esc(x.r.id) + '"><img loading="lazy" src="' + esc(x.r.thumbSrc) + '" alt="" onerror="this.onerror=null;this.src=\'icons/icon-192.png\'"><div class="t"><b>' + esc(x.r.title) + '</b><span>' + esc(d) + '</span>' + miss + sub + '</div>' + icon.chev + '</a>';
    }).join('') + '</div>' : '';
    const g0 = list.filter((x) => !x.missing.length), g1 = list.filter((x) => x.missing.length === 1), g2 = list.filter((x) => x.missing.length === 2);
    res.innerHTML = (list.length ? sect('Podes fazer já', g0) + sect('Falta 1 ingrediente', g1) + sect('Faltam 2 ingredientes', g2)
      : '<div class="empty"><h3>Ainda nada completo</h3><p>Com estes ingredientes faltam 3 ou mais coisas em todas as receitas. Junta mais alguns, por exemplo ovos, cebola ou batata.</p></div>') +
      '<p class="small" style="margin-top:12px">Conta os ingredientes principais de cada receita; sal, pimenta e ervas a gosto não entram. Ingredientes opcionais também não.</p>';
  };
  main.querySelector('#cGroups').addEventListener('click', (e) => {
    const b = e.target.closest('[data-food]'); if (!b || b.disabled) return;
    const k = b.dataset.food; if (CASA.sel.has(k)) CASA.sel.delete(k); else CASA.sel.add(k);
    saveCasa(); draw();
  });
  $('#cq').addEventListener('input', (e) => { CASA.q = e.target.value; draw(); });
  $('#cq').addEventListener('keydown', (e) => { if (e.key === 'Enter') e.target.blur(); });
  $('#cPantry').addEventListener('change', (e) => { CASA.pantry = e.target.checked; saveCasa(); draw(); });
  $('#cClear').addEventListener('click', () => { CASA.sel.clear(); saveCasa(); draw(); });
  draw();
}

/* ---------- vista: modo cozinha ---------- */
let wakeLock = null, cookActive = false;
async function lockScreen() {
  try { if ('wakeLock' in navigator) { wakeLock = await navigator.wakeLock.request('screen'); wakeLock.addEventListener('release', () => { wakeLock = null; updateWL(); }); } } catch (e) { wakeLock = null; }
  updateWL();
}
function updateWL() { const el = $('#wl'); if (el) el.textContent = wakeLock ? 'Ecrã sempre ligado' : ('wakeLock' in navigator ? 'Ecrã normal' : ''); if (el) el.hidden = !el.textContent; }
document.addEventListener('visibilitychange', () => { if (cookActive && document.visibilityState === 'visible' && !wakeLock) lockScreen(); });
function releaseLock() { cookActive = false; if (wakeLock) { wakeLock.release().catch(() => {}); wakeLock = null; } }

const TIMER = { end: 0, label: '', iv: 0, rang: false };
function minutesIn(s) { const m = /(\d+)(?:\s*(?:a|–|-)\s*(\d+))?\s*min/.exec(s); return m ? Number(m[1]) : 0; }
function beep() {
  try { const A = window.AudioContext || window.webkitAudioContext; const ctx = new A(); [0, .35, .7].forEach((t) => { const o = ctx.createOscillator(), g = ctx.createGain(); o.frequency.value = 880; o.connect(g); g.connect(ctx.destination); g.gain.setValueAtTime(.25, ctx.currentTime + t); g.gain.exponentialRampToValueAtTime(.001, ctx.currentTime + t + .3); o.start(ctx.currentTime + t); o.stop(ctx.currentTime + t + .3); }); } catch (e) { /* sem som */ }
  if (navigator.vibrate) navigator.vibrate([300, 150, 300, 150, 300]);
}
function tick() {
  const el = $('#timerBox'); const left = Math.max(0, TIMER.end - Date.now());
  if (TIMER.end && left === 0 && !TIMER.rang) { TIMER.rang = true; beep(); toast('⏰ ' + TIMER.label + ': tempo!'); }
  if (!el) return;
  if (!TIMER.end) return;
  const s = Math.ceil(left / 1000);
  $('.clock', el).textContent = String(Math.floor(s / 60)).padStart(2, '0') + ':' + String(s % 60).padStart(2, '0');
  el.classList.toggle('ring', left === 0);
}
function timerHTML(mins, label) {
  if (TIMER.end) return '<div class="timer" id="timerBox"><span class="clock">--:--</span><span>' + esc(TIMER.label) + '</span><button class="btn" id="tStop">Parar</button></div>';
  if (!mins) return '';
  return '<div class="timer" id="timerBox"><button class="btn" id="tStart" data-m="' + mins + '" data-l="' + esc(label) + '">' + icon.clock + 'Temporizador ' + mins + ' min</button></div>';
}

function renderCook(main, r, startStep) {
  cookActive = true; document.body.classList.add('cook'); lockScreen();
  const f = (DOSES[r.id] || r.servings) / r.servings;
  const screens = [{ kind: 'ing' }].concat(r.steps.map((s, i) => ({ kind: 'step', s, i }))).concat([{ kind: 'done' }]);
  let i = Math.max(0, Math.min(screens.length - 1, startStep || 0));
  const draw = () => {
    const sc = screens[i];
    let body = '';
    if (sc.kind === 'ing') body = '<span class="num">Antes de começar</span><h2>Junta os ingredientes</h2><ul class="ingr">' + r.ingredients.map((x) => '<li>' + esc(fmtIng(x, f)) + '</li>').join('') + '</ul>' + (r.temp ? '<p>Forno a ' + r.temp + ' °C.</p>' : '');
    else if (sc.kind === 'step') body = '<span class="num">Passo ' + (sc.i + 1) + ' de ' + r.steps.length + '</span><h2>' + esc(sc.s.title) + '</h2><p>' + esc(sc.s.detail) + '</p>' + timerHTML(minutesIn(sc.s.detail + ' ' + sc.s.title), sc.s.title);
    else body = '<span class="num">Pronto</span><h2>Bom apetite! 🍽️</h2>' + (r.tip ? '<p>' + esc(r.tip) + '</p>' : '');
    if (sc.kind !== 'step' && TIMER.end) body += timerHTML(0, '');
    main.innerHTML = '<div class="cook-view view-enter" id="cook">' +
      '<div class="cook-top"><button class="icon-btn" id="cookClose" aria-label="Sair do modo cozinha">' + icon.x + '</button><span class="ttl">' + esc(r.title) + '</span><span class="wl" id="wl" hidden></span></div>' +
      '<div class="cook-dots">' + screens.map((_, k) => '<i class="' + (k <= i ? 'on' : '') + '"></i>').join('') + '</div>' +
      '<div class="cook-body" aria-live="polite">' + body + '</div>' +
      '<div class="cook-nav"><button class="btn" id="cPrev"' + (i === 0 ? ' disabled' : '') + '>' + icon.left + 'Anterior</button>' +
      '<button class="btn next" id="cNext">' + (i === screens.length - 1 ? 'Terminar' : (i === 0 ? 'Começar' : 'Seguinte')) + icon.right + '</button></div></div>';
    updateWL(); tick();
    $('#cookClose').onclick = exit;
    $('#cPrev').onclick = () => go(-1);
    $('#cNext').onclick = () => (i === screens.length - 1 ? exit() : go(1));
    const ts = $('#tStart'); if (ts) ts.onclick = () => { TIMER.end = Date.now() + Number(ts.dataset.m) * 60000; TIMER.label = ts.dataset.l; TIMER.rang = false; clearInterval(TIMER.iv); TIMER.iv = setInterval(tick, 250); draw(); };
    const tp = $('#tStop'); if (tp) tp.onclick = () => { TIMER.end = 0; clearInterval(TIMER.iv); draw(); };
  };
  const go = (d) => { const n = i + d; if (n < 0 || n >= screens.length) return; i = n; history.replaceState(null, '', '#/receita/' + r.id + '/cozinha/' + i); draw(); };
  const exit = () => { if (history.length > 1 && cameFromApp) history.back(); else location.hash = '#/receita/' + r.id; };
  draw();
  let x0 = null, y0 = 0;
  main.ontouchstart = (e) => { x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; };
  main.ontouchend = (e) => { if (x0 == null) return; const dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0; if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) go(dx < 0 ? 1 : -1); x0 = null; };
  cookKeys = (e) => { if (e.key === 'ArrowRight') go(1); if (e.key === 'ArrowLeft') go(-1); if (e.key === 'Escape') exit(); };
}
let cookKeys = null;
document.addEventListener('keydown', (e) => { if (cookKeys && cookActive) cookKeys(e); });

/* ---------- vista: refeição completa (mesmo algoritmo da Page) ---------- */
function buildCombos(kind, pref, dessert, target, minP) {
  const by = (m) => RECIPES.filter((r) => r.meal === m);
  const coreMeal = kind === 'almoco' ? 'Prato principal' : kind === 'pa' ? 'Pequeno-almoço' : 'Snack';
  let cores = by(coreMeal);
  const prefOk = pref === 'Qualquer' || cores.some((r) => r.protein === pref);
  if (pref !== 'Qualquer' && prefOk) cores = cores.filter((r) => r.protein === pref);
  const coreQty = kind === 'lanche' ? [1, 2] : [1, 1.5];
  const breadQty = kind === 'pa' ? [0, 1, 2] : [0, 1];
  const breads = by('Acompanhamento/Pão'), sauces = by('Molho'), desserts = by('Sobremesa');
  const all = [];
  cores.forEach((core) => coreQty.forEach((cq) => {
    const breadOpts = [null];
    breads.forEach((b) => breadQty.forEach((q) => { if (q > 0) breadOpts.push({ r: b, qty: q, role: 'Pão' }); }));
    breadOpts.forEach((bread) => {
      const sauceOpts = [null];
      if (kind !== 'pa' || bread) sauces.forEach((s) => sauceOpts.push({ r: s, qty: 1, role: 'Molho' }));
      sauceOpts.forEach((sauce) => {
        const dOpts = [null];
        if ((kind === 'almoco' && dessert) || kind === 'lanche') desserts.forEach((d) => dOpts.push({ r: d, qty: 1, role: 'Sobremesa' }));
        dOpts.forEach((ds) => {
          if (kind === 'almoco' && dessert && !ds) return;
          const parts = [{ r: core, qty: cq, role: coreMeal }];
          [bread, sauce, ds].forEach((x) => { if (x) parts.push(x); });
          let kcal = 0, p = 0, c = 0, f = 0;
          parts.forEach((x) => { kcal += x.r.kcal * x.qty; p += x.r.p * x.qty; c += x.r.c * x.qty; f += x.r.f * x.qty; });
          const diff = (kcal - target) / target;
          let score = Math.abs(diff) * 100 * (diff > 0 ? 1.3 : 1) + Math.max(0, minP - p) * 3 + (parts.length - 1) * 1.5 + (cq > 1 ? 2 : 0);
          parts.slice(1).forEach((x) => { score += core.pairs.indexOf(x.r.id) >= 0 ? -6 : x.role === 'Molho' ? 4 : x.role === 'Pão' ? 2 : 0; });
          all.push({ parts, kcal, p, c, f, score });
        });
      });
    });
  }));
  all.sort((a, b) => a.score - b.score);
  const good = all.filter((x) => Math.abs(x.kcal - target) / target <= 0.12 && x.p >= minP);
  const base = good.length ? good : all.slice(0, 15);
  const groups = {}, order = [];
  base.forEach((x) => { const k = x.parts[0].r.id; if (!groups[k]) { groups[k] = []; order.push(k); } groups[k].push(x); });
  const pool = [];
  for (let round = 0; pool.length < 15 && round < 6; round++) order.forEach((k) => { if (groups[k][round] && pool.length < 15) pool.push(groups[k][round]); });
  return { pool, exact: good.length > 0, prefOk, total: all.length };
}
const MS = Object.assign({ kind: 'almoco', target: '550', minP: '35', pref: 'Qualquer', dessert: false, idx: 0 }, store.get('rf-meal', {}));
function renderMeal(main) {
  const kinds = [['almoco', 'Almoço/jantar'], ['pa', 'Pequeno-almoço'], ['lanche', 'Lanche']];
  main.innerHTML = '<div class="hero"><h1>Refeição completa</h1><p>Escolhe o alvo e eu junto prato, pão, molho e sobremesa.</p></div>' +
    '<div class="seg" role="group" aria-label="Tipo de refeição" style="margin-top:14px">' + kinds.map((k) => '<button data-kind="' + k[0] + '" aria-pressed="' + (MS.kind === k[0]) + '">' + k[1] + '</button>').join('') + '</div>' +
    '<div class="form">' +
    '<div class="field"><label for="mTarget">Alvo de kcal</label>' + selectHTML('mTarget', ['250', '300', '350', '400', '450', '500', '550', '600', '650', '700', '800'].map((v) => [v, v + ' kcal']), MS.target, 'Alvo de kcal') + '</div>' +
    '<div class="field"><label for="mMinP">Proteína mínima</label>' + selectHTML('mMinP', ['0', '15', '20', '25', '30', '35', '40', '45', '50'].map((v) => [v, v === '0' ? 'Sem mínimo' : v + ' g']), MS.minP, 'Proteína mínima') + '</div>' +
    '<div class="field full"><label for="mPref">Proteína preferida</label>' + selectHTML('mPref', [['Qualquer', 'Qualquer']].concat(PROTEINS.map((p) => [p, p])), MS.pref, 'Proteína preferida') + '</div>' +
    (MS.kind === 'almoco' ? '<label class="toggle">Incluir sobremesa<span class="switch"><input type="checkbox" id="mDessert"' + (MS.dessert ? ' checked' : '') + '><span></span></span></label>' : '') +
    '</div><div id="sug"></div>' +
    '<section class="sec"><details class="panel"><summary>Como escolhe</summary><ul class="bul" style="margin-top:10px">' +
    ['Parte de um prato base do tipo de refeição (prato principal, pequeno-almoço ou snack), filtrado pela proteína preferida.',
      'Testa todas as combinações com pão ou substituto, um molho e uma sobremesa opcionais, e 1 ou 1½ doses do prato base.',
      'Fica com as que ficam a 12% do alvo de kcal e cumprem a proteína mínima; passar do alvo pesa mais do que ficar abaixo.',
      'Prefere os acompanhamentos que a receita indica em “Combina com” e refeições com menos peças.',
      '“Outra sugestão” percorre as melhores, alternando o prato base para variar.'].map((t) => '<li>' + esc(t) + '</li>').join('') + '</ul></details></section>';
  const save = () => store.set('rf-meal', MS);
  const reset = () => { MS.idx = 0; save(); renderMeal(main); };
  $$('[data-kind]', main).forEach((b) => b.onclick = () => { MS.kind = b.dataset.kind; reset(); });
  $('#mTarget').onchange = (e) => { MS.target = e.target.value; reset(); };
  $('#mMinP').onchange = (e) => { MS.minP = e.target.value; reset(); };
  $('#mPref').onchange = (e) => { MS.pref = e.target.value; reset(); };
  const d = $('#mDessert'); if (d) d.onchange = (e) => { MS.dessert = e.target.checked; reset(); };
  drawSug(main);
}
function drawSug(main) {
  const sug = buildCombos(MS.kind, MS.pref, MS.kind === 'almoco' && MS.dessert, Number(MS.target), Number(MS.minP));
  const box = $('#sug', main);
  if (!sug.pool.length) { box.innerHTML = '<div class="empty" style="margin-top:16px"><h3>Sem combinações</h3><p>Ainda não há receitas suficientes para este tipo de refeição.</p></div>'; return; }
  const combo = sug.pool[MS.idx % sug.pool.length];
  const qtyText = (x) => { const u = x.r.unit || ['dose', 'doses']; return x.qty === 1 ? '1 ' + u[0] : frac(x.qty) + ' ' + u[1]; };
  const minP = Number(MS.minP);
  box.innerHTML = '<div class="sug-head"><h2>Sugestão ' + ((MS.idx % sug.pool.length) + 1) + ' de ' + sug.pool.length + '</h2><button class="btn accent" id="another"' + (sug.pool.length < 2 ? ' disabled' : '') + '>Outra sugestão</button></div>' +
    '<div class="list">' + combo.parts.map((x) => rowHTML(x.r, qtyText(x) + ' · ' + Math.round(x.r.kcal * x.qty) + ' kcal · ' + Math.round(x.r.p * x.qty) + ' g de proteína', x.role)).join('') + '</div>' +
    '<div class="totals">' +
    '<div class="macro"><b>' + Math.round(combo.kcal) + '</b><span>kcal · alvo ' + esc(MS.target) + '</span></div>' +
    '<div class="macro' + (combo.p < minP ? ' warn' : '') + '"><b>' + Math.round(combo.p) + ' g</b><span>proteína' + (minP ? ' · mín. ' + minP : '') + '</span></div>' +
    '<div class="macro"><b>' + Math.round(combo.c) + ' g</b><span>hidratos</span></div>' +
    '<div class="macro"><b>' + Math.round(combo.f) + ' g</b><span>gordura</span></div></div>' +
    '<p class="small" style="margin-top:10px">Entre ' + sug.total + ' combinações testadas. Valores estimados.' +
    (sug.exact ? '' : ' Nenhuma combinação cumpre o alvo e a proteína mínima ao mesmo tempo; estas são as mais próximas.') +
    (sug.prefOk ? '' : ' Ainda não há receitas desta proteína para este tipo de refeição, por isso usei todas.') + '</p>';
  $('#another').onclick = () => { MS.idx++; store.set('rf-meal', MS); drawSug(main); };
}

/* ---------- vista: offline e instalação ---------- */
let installEvt = null;
window.addEventListener('beforeinstallprompt', (e) => { e.preventDefault(); installEvt = e; const b = $('#installBtn'); if (b) b.hidden = false; });
window.addEventListener('appinstalled', () => { installEvt = null; toast('App instalada 🎉'); });
const isStandalone = () => window.matchMedia('(display-mode: standalone)').matches || navigator.standalone === true;
const isIOS = () => /iphone|ipad|ipod/i.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
const mb = (b) => (b / 1048576).toFixed(1).replace('.', ',') + ' MB';
let bulkRunning = false;

async function renderMore(main) {
  await refreshSaved();
  const nSaved = RECIPES.filter(isSaved).length;
  main.innerHTML = '<div class="hero"><h1>Offline e app</h1><p>Usa o livro na cozinha, mesmo sem rede.</p></div>' +
    '<section class="sec"><h2>Instalar no telemóvel</h2><div class="panel">' +
    (isStandalone() ? '<p class="small" style="margin:0">✅ Já estás a usar a app instalada.</p>'
      : '<button class="btn primary full" id="installBtn"' + (installEvt ? '' : ' hidden') + '>' + icon.down + 'Instalar app</button>' +
      '<p class="small" style="margin:' + (installEvt ? '10px' : '0') + ' 0 0">' + (isIOS() ? 'No iPhone: abre no Safari, toca em <b>Partilhar</b> e depois em <b>Adicionar ao ecrã principal</b>.' : 'No Android (Chrome): menu ⋮ → <b>Instalar app</b> ou <b>Adicionar ao ecrã principal</b>.') + '</p>') +
    '</div></section>' +
    '<section class="sec"><h2>Vídeos offline <small id="savedCount">' + nSaved + ' de ' + RECIPES.length + '</small></h2><div class="panel">' +
    '<p class="small" style="margin-top:0">A app e as receitas já ficam guardadas automaticamente. Os vídeos guardam-se quando os vês, ou todos de uma vez aqui.</p>' +
    '<button class="btn primary full" id="saveAll">' + icon.down + 'Guardar todos os vídeos<span id="allSize"></span></button>' +
    '<div class="progress" id="prog" hidden><i></i></div><p class="small" id="progTxt" hidden></p>' +
    '<label class="toggle" style="margin-top:10px">Guardar vídeos que vejo<span class="switch"><input type="checkbox" id="autoSave"' + (autoSave() ? ' checked' : '') + '><span></span></span></label>' +
    '<div id="storage" class="small" style="margin-top:10px"></div>' +
    '<button class="btn full" id="clearVids" style="margin-top:10px"' + (nSaved ? '' : ' disabled') + '>' + icon.trash + 'Apagar vídeos guardados</button>' +
    '</div></section>' +
    '<section class="sec"><h2>Por receita</h2><div class="list">' + RECIPES.map((r) => rowHTML(r, !r.hasVideo ? 'Vídeo a caminho' : isSaved(r) ? '✓ Vídeo offline' : 'Só com internet')).join('') + '</div></section>' +
    '<section class="sec"><h2>Sobre</h2><div class="panel small">' + esc(RECIPES.length + ' receitas. Macros por dose são estimativas a partir de ingredientes crus; variam com as marcas e o tamanho dos ingredientes.') +
    '<div class="kv" style="margin-top:8px"><span>Service worker</span><b id="swState">…</b></div></div></section>';
  const ib = $('#installBtn'); if (ib) ib.onclick = async () => { if (!installEvt) return; installEvt.prompt(); await installEvt.userChoice; installEvt = null; ib.hidden = true; };
  $('#autoSave').onchange = (e) => store.set('rf-autosave', e.target.checked);
  $('#swState').textContent = !('serviceWorker' in navigator) ? 'Não suportado' : navigator.serviceWorker.controller ? 'Ativo' : 'A iniciar';
  if (navigator.storage && navigator.storage.estimate) navigator.storage.estimate().then((s) => { const el = $('#storage'); if (el) el.textContent = 'Espaço usado pela app: ' + mb(s.usage || 0) + '.'; });
  if (navigator.onLine) {
    Promise.all(RECIPES.filter((r) => r.hasVideo && !isSaved(r)).map((r) => fetch(r.videoSrc, { method: 'HEAD' }).then((x) => Number(x.headers.get('content-length')) || 0).catch(() => 0)))
      .then((sizes) => { const t = sizes.reduce((a, b) => a + b, 0); const el = $('#allSize'); if (el && t) el.textContent = ' (' + mb(t) + ')'; });
  }
  $('#saveAll').onclick = async () => {
    if (bulkRunning) return;
    if (!navigator.onLine) { toast('Precisas de internet para guardar.'); return; }
    bulkRunning = true;
    const todo = RECIPES.filter((r) => r.hasVideo && !isSaved(r));
    const prog = $('#prog'), txt = $('#progTxt'); prog.hidden = false; txt.hidden = false; $('#saveAll').disabled = true;
    let done = 0, fail = 0;
    for (const r of todo) {
      txt.textContent = 'A guardar ' + (done + 1) + ' de ' + todo.length + ': ' + (r.short || r.title);
      try { await saveRecipe(r); } catch (e) { fail++; }
      done++; $('i', prog).style.width = (done / todo.length * 100) + '%';
    }
    bulkRunning = false;
    toast(fail ? fail + ' vídeos falharam; tenta outra vez.' : 'Todos os vídeos estão offline ✅');
    if (location.hash === '#/mais') renderMore(main);
  };
  $('#clearVids').onclick = async () => {
    if (!confirm('Apagar todos os vídeos guardados neste dispositivo? As receitas continuam disponíveis.')) return;
    await caches.delete(VIDEO_CACHE); await refreshSaved(); toast('Vídeos apagados'); renderMore(main);
  };
}

/* ---------- router ---------- */
const scrollPos = {};
let currentHash = null, cameFromApp = false;
function route() {
  const main = $('#main');
  const hash = location.hash || '#/';
  if (currentHash != null) scrollPos[currentHash] = main.scrollTop;
  const prevHash = currentHash; currentHash = hash;
  if (prevHash != null) cameFromApp = true;
  const parts = hash.replace(/^#\/?/, '').split('/').map(decodeURIComponent);
  const wasCook = document.body.classList.contains('cook');
  document.body.classList.remove('cook'); main.ontouchstart = main.ontouchend = null;
  let tab = 'home', title = 'Receitas Fit', back = false, docTitle = 'Livro de Receitas Fit';
  if (parts[0] === 'receita' && BY_ID[parts[1]]) {
    const r = BY_ID[parts[1]];
    back = true; title = r.short || r.title; docTitle = r.title + ' · Receitas Fit'; tab = '';
    if (parts[2] === 'cozinha') { renderCook(main, r, Number(parts[3]) || 0); docTitle = 'Modo cozinha · ' + r.title; }
    else { if (wasCook) releaseLock(); renderRecipe(main, r); }
  } else {
    if (wasCook) releaseLock();
    if (parts[0] === 'refeicao') { tab = 'meal'; title = 'Refeição completa'; docTitle = 'Refeição completa · Receitas Fit'; renderMeal(main); }
    else if (parts[0] === 'casa') { tab = 'casa'; title = 'Em casa'; docTitle = 'O que tenho em casa · Receitas Fit'; renderCasa(main); }
    else if (parts[0] === 'favoritas') { const c = colById(parts[1]) || COLS[0]; tab = 'fav'; title = c.name; docTitle = c.name + ' · Receitas Fit'; renderFav(main, c.id); }
    else if (parts[0] === 'mais') { tab = 'more'; title = 'Offline'; docTitle = 'Offline · Receitas Fit'; renderMore(main); }
    else {
      if (parts[0] === 'receita') toast('Receita não encontrada');
      readListHash(parts[0].startsWith('?') ? hash : '');
      renderHome(main);
    }
  }
  if (!document.body.classList.contains('cook') && cookActive) releaseLock();
  document.title = docTitle;
  $('#topTitle').textContent = title;
  $('#backBtn').hidden = !back;
  $('.brand img').hidden = back;
  $$('#tabbar a').forEach((a) => { a.classList.toggle('on', a.dataset.tab === tab); if (a.dataset.tab === tab) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); });
  const firstChild = main.firstElementChild; if (firstChild && !document.body.classList.contains('cook')) firstChild.classList.add('view-enter');
  const isCookStep = parts[2] === 'cozinha' && prevHash && prevHash.indexOf('/cozinha') > 0;
  if (!isCookStep) main.scrollTop = back ? 0 : (scrollPos[hash] || 0);
}
$('#backBtn').addEventListener('click', () => { if (cameFromApp && history.length > 1) history.back(); else location.hash = '#/'; });
document.addEventListener('click', (e) => {
  const b = e.target.closest('[data-fav]');
  if (b) { e.preventDefault(); toggleFav(b.dataset.fav); if (location.hash === '#/favoritas' && !isFav(b.dataset.fav)) setTimeout(route, 250); return; }
  const cb = e.target.closest('[data-cols]');
  if (cb) { e.preventDefault(); colSheet(cb.dataset.cols); return; }
  if (longPressed && e.target.closest('.card')) { e.preventDefault(); longPressed = false; }
});
// toque longo num cartão abre “Guardar em…”
let lpTimer = 0, longPressed = false, lpStart = null;
document.addEventListener('touchstart', (e) => {
  const card = e.target.closest('.card'); if (!card) return;
  longPressed = false; lpStart = [e.touches[0].clientX, e.touches[0].clientY];
  lpTimer = setTimeout(() => { longPressed = true; const w = card.closest('[data-rid]'); if (w) { if (navigator.vibrate) navigator.vibrate(12); colSheet(w.dataset.rid); } }, 520);
}, { passive: true });
document.addEventListener('touchmove', (e) => { if (lpStart && Math.hypot(e.touches[0].clientX - lpStart[0], e.touches[0].clientY - lpStart[1]) > 10) clearTimeout(lpTimer); }, { passive: true });
document.addEventListener('touchend', () => { clearTimeout(lpTimer); lpStart = null; }, { passive: true });
document.addEventListener('contextmenu', (e) => { if (e.target.closest('.card')) e.preventDefault(); });
$('#main').addEventListener('scroll', () => { $('#topbar').classList.toggle('scrolled', $('#main').scrollTop > 4); }, { passive: true });
const net = () => { $('#netBadge').hidden = navigator.onLine; };
window.addEventListener('online', net); window.addEventListener('offline', net);

/* ---------- arranque ---------- */
async function boot() {
  net();
  try {
    const res = await fetch('recipes.json', { cache: 'no-cache' });
    if (!res.ok) throw new Error(res.status);
    prepare(await res.json());
  } catch (e) {
    $('#main').innerHTML = '<div class="empty" style="margin-top:30px"><h3>Não consegui carregar as receitas</h3><p>Verifica a ligação à internet e tenta outra vez.</p><p><button class="btn primary" onclick="location.reload()">Tentar outra vez</button></p></div>';
    return;
  }
  await refreshSaved();
  window.addEventListener('hashchange', route);
  route();
  if ('serviceWorker' in navigator && location.protocol !== 'file:') {
    navigator.serviceWorker.register('sw.js').catch((err) => console.warn('Service worker não registado:', err));
  }
}
window.RF = { buildCombos: (...a) => buildCombos(...a), casaRank: () => casaRank(), get F() { return F; }, get cols() { return COLS; }, get recipes() { return RECIPES; } }; // para testes
boot();
})();
