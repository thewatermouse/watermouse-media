"""Troca o CTA 'Assinar a newsletter' (so um link) por formulario inline nas materias e guias.
Idempotente: pode rodar de novo. Uso: python tools/add_signup.py [--dry]"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DRY = '--dry' in sys.argv

CSS = """
  /* newsletter inline (add_signup.py) */
  .news form{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;}
  .news input[type=email]{background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.16);border-radius:2px;padding:12px 16px;font:inherit;font-size:14px;color:#fff;min-width:220px;outline:none;}
  .news input[type=email]::placeholder{color:rgba(248,248,249,0.4);}
  .news input[type=email]:focus{border-color:#B8C0FF;}
  .news button{background:var(--sage);color:#fff;border:none;border-radius:2px;padding:12px 24px;font:inherit;font-size:14px;font-weight:500;cursor:pointer;}
  .news .nl-ok{font-size:14px;color:#B8C0FF;}
  .news .nl-leg{font-size:11.5px;line-height:1.5;margin:12px auto 0;opacity:.6;max-width:46ch;}
  .news .nl-leg a{display:inline;background:none;padding:0;border-radius:0;color:#B8C0FF;text-decoration:underline;font-size:inherit;font-weight:inherit;}
  .nl-hp{position:absolute;left:-9999px;}
"""

HTML = """<section class="news" id="newsletter">
      <h2 class="serif">Gostou? Receba as próximas.</h2>
      <p>As histórias que não chegam em português, uma vez por semana, em 3 minutos de leitura. Sem spam.</p>
      <div class="nl-ok" role="alert" hidden></div>
      <form class="nl-form" novalidate>
        <input type="email" name="email" placeholder="voce@email.com" required autocomplete="email" aria-label="Seu e-mail">
        <button type="submit">Assinar</button>
        <span class="nl-hp" aria-hidden="true"><label>Não preencha<input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></span>
      </form>
      <p class="nl-leg">Ao assinar, você concorda em receber a newsletter (com confirmação e link para sair em todo envio) e, conforme a <a href="https://thewatermouse.com/privacidade/">política de privacidade</a>, com o uso dos seus dados para medição e anúncios.</p>
    </section>"""

JS = """<script>
(function(){
  var EP="https://script.google.com/macros/s/AKfycbwPrnZ0gmFK3_t8PXvk4XVsJq5jE1KRtB67aejkP8SA6E9RfsBHocwH47GV1RLcpfA/exec";
  var box=document.getElementById('newsletter'); if(!box) return;
  var f=box.querySelector('.nl-form'), s=box.querySelector('.nl-ok'); if(!f) return;
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var inp=f.querySelector('[name="email"]'), email=inp.value.trim(), btn=f.querySelector('button');
    if(!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)){inp.focus();return;}
    if(f.querySelector('[name="_honey"]').value){return;}
    btn.disabled=true; btn.textContent="Enviando...";
    fetch(EP,{method:"POST",headers:{"Content-Type":"text/plain;charset=utf-8"},body:JSON.stringify({email:email,origem:"media-materia"})})
      .then(function(r){if(!r.ok){throw new Error("http");}return r.json();})
      .then(function(d){if(!d||String(d.success)!=="true"){throw new Error("rejected");}window.dataLayer=window.dataLayer||[];window.dataLayer.push({event:'newsletter_signup',origem:'media-materia'});f.hidden=true;s.hidden=false;s.textContent="Quase lá! Enviamos um e-mail para você confirmar a inscrição. Olhe também a caixa de spam. 📨";})
      .catch(function(){window.location.href="mailto:digo@thewatermouse.com?subject="+encodeURIComponent("Assinatura Watermouse Media")+"&body="+encodeURIComponent("E-mail: "+email);})
      .finally(function(){btn.disabled=false;btn.textContent="Assinar";});
  });
})();
</script>
"""

OLD = re.compile(r'<section class="news">\s*<h2 class="serif">Gostou\? Receba as próximas\.</h2>.*?</section>', re.S)

changed = skipped = 0
for p in sorted(ROOT.glob('*.html')):
    t = p.read_text(encoding='utf-8')
    if 'class="nl-form"' in t:
        skipped += 1
        continue
    if not OLD.search(t):
        continue
    t = OLD.sub(lambda m: HTML, t, count=1)
    # CSS logo antes do </style> que contem .news
    i = t.find('.news a{')
    j = t.find('</style>', i)
    t = t[:j] + CSS + t[j:]
    # JS antes do </body>
    t = t.replace('</body>', JS + '</body>', 1)
    changed += 1
    if not DRY:
        p.write_text(t, encoding='utf-8')
print('alteradas', changed, 'ja_tinham', skipped, '(dry)' if DRY else '')
