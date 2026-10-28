/* Watermouse Media · Ferramentas: utilitarios compartilhados (formatacao pt-BR, RNG com semente, eventos, cartao de compartilhamento). */
(function(){
  var wm = window.wm = window.wm || {};
  var nf = {};
  wm.nf = function(dec){ dec = dec|0; return nf[dec] || (nf[dec] = new Intl.NumberFormat('pt-BR',{minimumFractionDigits:dec,maximumFractionDigits:dec})); };
  wm.fmt = function(v, dec){ return wm.nf(dec).format(v); };
  /* numeros grandes por extenso: 212,8 milhões; 2,28 trilhões */
  wm.big = function(v, unit){
    var a = Math.abs(v), s;
    if (a >= 1e12) s = wm.fmt(v/1e12, a>=1e13?1:2) + (v/1e12>=2?' trilhões':' trilhão');
    else if (a >= 1e9) s = wm.fmt(v/1e9, a>=1e10?1:2) + (v/1e9>=2?' bilhões':' bilhão');
    else if (a >= 1e6) s = wm.fmt(v/1e6, a>=1e7?1:2) + (v/1e6>=2?' milhões':' milhão');
    else if (a >= 1e4) s = wm.fmt(v/1e3, 0) + ' mil';
    else s = wm.fmt(v, a>=100?0:1);
    return unit ? s + ' ' + unit : s;
  };
  wm.esc = function(s){ return String(s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); };

  /* semente: mesmo desafio para todo mundo no mesmo dia (fuso de Sao Paulo) */
  wm.today = function(){
    var p = new Intl.DateTimeFormat('en-CA',{timeZone:'America/Sao_Paulo',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
    return p; /* AAAA-MM-DD */
  };
  wm.hash = function(str){ var h = 2166136261>>>0; for (var i=0;i<str.length;i++){ h ^= str.charCodeAt(i); h = Math.imul(h,16777619); } return h>>>0; };
  wm.rng = function(seed){ var a = seed>>>0; return function(){ a = (a + 0x6D2B79F5)>>>0; var t = a; t = Math.imul(t ^ (t>>>15), t|1); t ^= t + Math.imul(t ^ (t>>>7), t|61); return ((t ^ (t>>>14))>>>0)/4294967296; }; };

  wm.track = function(name, data){ try{ var o = {event:name}; for (var k in data||{}) o[k]=data[k]; (window.dataLayer = window.dataLayer||[]).push(o); }catch(e){} };
  wm.store = {
    get:function(k, d){ try{ var v = localStorage.getItem('wm_'+k); return v==null ? d : JSON.parse(v); }catch(e){ return d; } },
    set:function(k, v){ try{ localStorage.setItem('wm_'+k, JSON.stringify(v)); }catch(e){} }
  };
  wm.toast = function(msg){
    var t = document.getElementById('toast'); if (!t){ t = document.createElement('div'); t.id='toast'; t.className='toast'; t.setAttribute('role','status'); document.body.appendChild(t); }
    t.textContent = msg; t.classList.add('on'); clearTimeout(wm._tt); wm._tt = setTimeout(function(){ t.classList.remove('on'); }, 2200);
  };
  wm.copy = function(text){
    if (navigator.clipboard && navigator.clipboard.writeText) return navigator.clipboard.writeText(text).then(function(){ wm.toast('Copiado.'); });
    var ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select(); try{ document.execCommand('copy'); wm.toast('Copiado.'); }catch(e){} ta.remove(); return Promise.resolve();
  };

  /* cartao 1080x1350 para compartilhar (desenhado em canvas). draw(ctx, W, H, helpers) */
  wm.fontsReady = function(){
    if (!document.fonts || !document.fonts.load) return Promise.resolve();
    return Promise.all([document.fonts.load('64px "DM Serif Display"'), document.fonts.load('italic 36px "Instrument Serif"'), document.fonts.load('26px "IBM Plex Mono"'), document.fonts.load('32px "Newsreader"')]).catch(function(){});
  };
  wm.wrap = function(ctx, text, x, y, maxW, lh, maxLines){
    var words = String(text).split(' '), line = '', lines = [];
    words.forEach(function(w){ var t = line ? line+' '+w : w; if (ctx.measureText(t).width > maxW && line){ lines.push(line); line = w; } else line = t; });
    if (line) lines.push(line);
    if (maxLines && lines.length > maxLines){ lines = lines.slice(0,maxLines); lines[maxLines-1] = lines[maxLines-1].replace(/\s*\S*$/,'') + '…'; }
    lines.forEach(function(l,i){ ctx.fillText(l, x, y + i*lh); });
    return y + lines.length*lh;
  };
  wm.card = function(draw){
    return wm.fontsReady().then(function(){
      var c = document.createElement('canvas'); c.width = 1080; c.height = 1350; var ctx = c.getContext('2d');
      ctx.fillStyle = '#F8F8F9'; ctx.fillRect(0,0,1080,1350);
      ctx.fillStyle = '#0D0D0F'; ctx.fillRect(0,0,1080,14);
      draw(ctx, 1080, 1350);
      ctx.fillStyle = '#0D0D0F'; ctx.fillRect(0,1282,1080,68);
      ctx.fillStyle = '#F8F8F9'; ctx.font = '500 24px "IBM Plex Mono", monospace'; ctx.textAlign = 'left'; ctx.fillText('Watermouse Media', 56, 1325);
      ctx.textAlign = 'right'; ctx.fillText(location.host + location.pathname.replace(/\/$/,''), 1024, 1325); ctx.textAlign = 'left';
      return new Promise(function(res){ c.toBlob(function(b){ res({canvas:c, blob:b, url:URL.createObjectURL(b)}); }, 'image/png'); });
    });
  };
  wm.download = function(blob, name){ var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click(); a.remove(); };
  /* compartilhar: usa a folha nativa (com imagem, se o aparelho deixar) ou cai para copiar link */
  wm.share = function(o){ /* {text, url, blob, name, origem} */
    var data = {text:o.text, url:o.url};
    if (o.blob && navigator.canShare){ try{ var f = new File([o.blob], o.name||'watermouse.png', {type:'image/png'}); if (navigator.canShare({files:[f]})) data.files = [f]; }catch(e){} }
    if (navigator.share){ return navigator.share(data).then(function(){ wm.track('ferramenta_share',{metodo:'nativo',ferramenta:o.ferramenta}); }).catch(function(){}); }
    return wm.copy(o.text + ' ' + o.url).then(function(){ wm.track('ferramenta_share',{metodo:'copiar',ferramenta:o.ferramenta}); });
  };
  wm.wa = function(text, url, ferr){ wm.track('ferramenta_share',{metodo:'whatsapp',ferramenta:ferr}); window.open('https://wa.me/?text='+encodeURIComponent(text+' '+url),'_blank','noopener'); };
  wm.xp = function(text, url, ferr){ wm.track('ferramenta_share',{metodo:'x',ferramenta:ferr}); window.open('https://twitter.com/intent/tweet?text='+encodeURIComponent(text)+'&url='+encodeURIComponent(url),'_blank','noopener'); };
})();

/* ===== contagens anonimas (Cloudflare Worker + KV): wm.hist(k) le, wm.hit(k,b) soma 1 ao balde b ===== */
(function(){
  var wm = window.wm; wm.API = 'https://wm-stats.rodrigokato.workers.dev/v1/h';
  wm.hist = function(k){ return fetch(wm.API+'?k='+encodeURIComponent(k)).then(function(r){ return r.ok ? r.json() : null; }).catch(function(){ return null; }); };
  wm.hit = function(k, b){ return fetch(wm.API, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({k:k, b:String(b)}), keepalive:true}).then(function(r){ return r.ok ? r.json() : null; }).catch(function(){ return null; }); };
  /* porcentagem de jogadores com pontuacao menor (e metade dos empatados) */
  wm.below = function(h, score){ if (!h || !h.t) return null; var lt = 0, eq = 0; Object.keys(h.b).forEach(function(k){ var v = +k; if (v < score) lt += h.b[k]; else if (v === score) eq += h.b[k]; }); return Math.round((lt + eq/2) * 100 / h.t); };
  wm.once = function(key){ var s = wm.store.get('sent', {}); if (s[key]) return false; s[key] = 1; var ks = Object.keys(s); if (ks.length > 300) delete s[ks[0]]; wm.store.set('sent', s); return true; };

  /* enquete: <div class="poll" data-id="..." data-q="Pergunta" data-opts="a|Rotulo A;b|Rotulo B"> */
  wm.poll = function(el){
    var id = el.dataset.id, key = 'poll:' + id, opts = el.dataset.opts.split(';').map(function(s){ var p = s.split('|'); return {k:p[0], l:p[1]}; });
    function showRes(h){
      var t = (h && h.t) || 0, out = '<div class="pq">'+wm.esc(el.dataset.q)+'</div>';
      opts.forEach(function(o){ var n = h && h.b[o.k] || 0, pc = t ? Math.round(n*100/t) : 0; out += '<div class="pr"><span class="pl">'+wm.esc(o.l)+'</span><span class="pb"><i style="width:'+pc+'%"></i></span><span class="pp num">'+pc+'%</span></div>'; });
      out += '<div class="pn label">'+t+' voto'+(t===1?'':'s')+' · anônimo</div>'; el.innerHTML = out;
    }
    function ask(){
      var out = '<div class="pq">'+wm.esc(el.dataset.q)+'</div><div class="po">';
      opts.forEach(function(o){ out += '<button type="button" class="btn ghost small" data-o="'+o.k+'">'+wm.esc(o.l)+'</button>'; });
      el.innerHTML = out + '</div><div class="pn label">Voto anônimo, sem cadastro</div>';
      el.querySelectorAll('[data-o]').forEach(function(b){ b.addEventListener('click', function(){ wm.store.set('poll_'+id, b.dataset.o); wm.track('enquete_voto',{enquete:id,opcao:b.dataset.o}); wm.hit(key, b.dataset.o).then(function(h){ showRes(h); }); }); });
    }
    if (wm.store.get('poll_'+id, null)) wm.hist(key).then(showRes); else ask();
  };
})();
