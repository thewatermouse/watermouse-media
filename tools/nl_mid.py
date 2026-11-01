"""Faixa de newsletter no meio da materia (leva ao formulario do fim da pagina). Idempotente.
add_mid_cta(html): depois do anuncio in-article-1, insere a faixa apos o 2o </p> seguinte; sem anuncio/paragrafos suficientes, nao faz nada."""
import re

STRIP = ('<aside class="nl-mid"><span>☕ <b>Gostando?</b> Receba as histórias da semana por e-mail, em 3 minutos.</span>'
         '<a href="#newsletter">Assinar grátis →</a></aside>')


def add_mid_cta(s):
    if 'class="nl-mid"' in s:
        return s
    m = re.search(r'data-ad="in-article-1".*?</script>\s*</div>', s, re.S)
    if not m:
        return s
    pos = m.end()
    for _ in range(2):
        j = s.find('</p>', pos)
        if j < 0:
            return s
        pos = j + 4
    return s[:pos] + '\n      ' + STRIP + s[pos:]
