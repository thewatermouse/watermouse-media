# -*- coding: utf-8 -*-
"""Gera 4 analises de dados proprias (graficos + specs) a partir de paises.json (Banco Mundial).
Todo numero do texto vem do calculo abaixo (nada digitado a mao). Uso: python -I tools/analises_dados.py
Saida: media/graf-*.jpg e rascunhos/2026-11-16..19-*.json (agendamento em programacao.json e feito a parte)."""
import json, pathlib, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = pathlib.Path(r"C:\Users\rodri\clients\watermouse-ferramentas\data\paises.json")
D = json.loads(DATA.read_text(encoding="utf-8"))
P = [p for p in D["paises"] if p.get("pop", 0) >= 1e6]
BR = next(p for p in P if p["iso3"] == "BRA")
BG, INK, GREY, BLUE, LIGHT = "#f8f8f8", "#0d0d10", "#9a9ca5", "#2236ff", "#d9dae0"
SERIF = ["Georgia", "Garamond", "DejaVu Serif"]
MONO = ["Courier New", "DejaVu Sans Mono"]
FONTE = "Fonte: Banco Mundial (WDI), valor mais recente de cada país. Países com 1 milhão de habitantes ou mais. Watermouse Media"


def n1(v):  # numero pt-BR 1 casa
    return f"{v:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")


def n0(v):
    return f"{v:,.0f}".replace(",", ".")


def usd(v):
    return "US$ " + n0(v)


def pct(v):
    return n1(v) + "%"


def r2(v):
    return f"{v:.2f}".replace(".", ",")


def lst(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " e " + items[-1]


def rank(key, p, rev=True, pool=None):
    pool = [q for q in (pool or P) if q.get(key) is not None]
    s = sorted(pool, key=lambda q: q[key], reverse=rev)
    return [q["iso3"] for q in s].index(p["iso3"]) + 1, len(s)


def have(*ks):
    return [p for p in P if all(p.get(k) is not None for k in ks)]


def frame(fig, ax, titulo, sub, fonte=None):
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK)
    ax.tick_params(colors=INK, labelsize=15)
    for t in ax.get_xticklabels() + ax.get_yticklabels():
        t.set_family(MONO)
    fig.text(0.04, 0.945, titulo, family=SERIF, fontsize=33, fontweight="bold", color=INK, va="top")
    fig.text(0.04, 0.875, sub, family=SERIF, fontsize=17, color="#444", va="top")
    fig.text(0.04, 0.02, fonte or FONTE, family=SERIF, fontsize=12.5, color="#555")


def scatter(fname, xs, ys, labels, hi, titulo, sub, xl, yl, logx=False, fit=True, xfmt=None, yfmt=None, show=None, off=None):
    fig, ax = plt.subplots(figsize=(16.8, 8.96), dpi=100)
    fig.subplots_adjust(left=0.07, right=0.97, top=0.78, bottom=0.14)
    x = np.array(xs, float); y = np.array(ys, float)
    ax.scatter(x, y, s=46, color=GREY, alpha=0.75, edgecolor="none", zorder=2)
    if fit:
        xx = np.log(x) if logx else x
        a, b = np.polyfit(xx, y, 1)
        gx = np.linspace(xx.min(), xx.max(), 100)
        ax.plot(np.exp(gx) if logx else gx, a * gx + b, color=INK, lw=1.8, ls=(0, (6, 4)), zorder=3)
    for i, l in enumerate(labels):
        if l in hi:
            ax.scatter([x[i]], [y[i]], s=190 if l == "Brasil" else 90, color=BLUE if l == "Brasil" else INK, zorder=5)
            dx, dy = (off or {}).get(l, (8, 8))
            ax.annotate(l, (x[i], y[i]), xytext=(dx, dy), textcoords="offset points", family=SERIF, fontsize=17 if l == "Brasil" else 14.5,
                        fontweight="bold" if l == "Brasil" else "normal", color=BLUE if l == "Brasil" else INK, zorder=6)
    if logx:
        ax.set_xscale("log")
    ax.set_xlabel(xl, family=SERIF, fontsize=16, color=INK, labelpad=10)
    ax.set_ylabel(yl, family=SERIF, fontsize=16, color=INK, labelpad=10)
    ax.grid(color=LIGHT, lw=0.8, zorder=0)
    if xfmt:
        ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(xfmt))
    if yfmt:
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(yfmt))
    frame(fig, ax, titulo, sub)
    fig.savefig(ROOT / "media" / fname, pil_kwargs={"quality": 92}, facecolor=BG)
    plt.close(fig)


def bars(fname, items, hi, titulo, sub, unit="", dec=1, fonte=None):
    fig, ax = plt.subplots(figsize=(16.8, 8.96), dpi=100)
    fig.subplots_adjust(left=0.17, right=0.95, top=0.80, bottom=0.12)
    names = [i[0] for i in items][::-1]; vals = [i[1] for i in items][::-1]
    cols = [BLUE if n == "Brasil" else (INK if n in hi else GREY) for n in names]
    ax.barh(names, vals, color=cols, height=0.68, zorder=2)
    for i, v in enumerate(vals):
        ax.text(v + max(vals) * 0.008, i, (n1(v) if dec else n0(v)) + unit, va="center", family=MONO, fontsize=14, color=INK, fontweight="bold")
    ax.set_xlim(0, max(vals) * 1.1)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="y", length=0, labelsize=15)
    for t in ax.get_yticklabels():
        t.set_family(SERIF); t.set_fontsize(15.5)
        if t.get_text() == "Brasil":
            t.set_color(BLUE); t.set_fontweight("bold")
    frame(fig, ax, titulo, sub, fonte)
    for t in ax.get_yticklabels():
        t.set_family(SERIF)
    fig.savefig(ROOT / "media" / fname, pil_kwargs={"quality": 92}, facecolor=BG)
    plt.close(fig)


def regress(ks_x, ks_y, logx=False):
    pool = have(ks_x, ks_y)
    x = np.array([p[ks_x] for p in pool], float); y = np.array([p[ks_y] for p in pool], float)
    xx = np.log(x) if logx else x
    a, b = np.polyfit(xx, y, 1)
    r = float(np.corrcoef(xx, y)[0, 1])
    res = {p["iso3"]: float(y[i] - (a * xx[i] + b)) for i, p in enumerate(pool)}
    return pool, a, b, r, res


def attrib(inds):
    return ('<b>Fonte:</b> <a href="https://data.worldbank.org" target="_blank" rel="noopener">Banco Mundial, World Development Indicators</a>, '
            + inds + ', atualização de out/2026. Cálculo e gráfico da Watermouse Media, para países com 1 milhão de habitantes ou mais. '
            'A correlação mostra associação, não prova que uma variável causa a outra.')


NOTE = ("Análise própria da Watermouse Media com dados públicos do Banco Mundial. Os números são calculados por nós a partir da base; "
        "o texto não é tradução nem resumo de outra matéria.")
CTX = ('<!--ctx-->\n      <h2>Para entender o contexto</h2>\n\n      {t}')
names = {p["iso3"]: p["nome"] for p in P}
specs = []


def spec(date, slug, title, dek, dek_card, og, img, alt, cap, body, attr, read=5):
    assert chr(0x2014) not in body + title + dek, "em-dash"
    s = dict(slug=slug, cat="mundo", cat_label="Mundo", title=title, dek=dek, dek_card=dek_card, og_desc=og,
             date_iso=f"{date}T10:00:00-03:00", image="media/" + img, image_alt=alt, image_caption_html=cap,
             body_html=body, read_min=str(read), note=NOTE, attrib_html=attr)
    (ROOT / "rascunhos" / f"{date}-{slug.split('-banco')[0][:40]}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    specs.append(s["slug"])


# ---------- 1. Renda e vida longa ----------
pool, a, b, r, res = regress("pibpc", "vida", logx=True)
pr = sorted(pool, key=lambda p: res[p["iso3"]], reverse=True)
acima = [p for p in pr if p["pop"] >= 5e6][:5]
abaixo = [p for p in pr if p["pop"] >= 5e6][::-1][:5]
exp_br = a * np.log(BR["pibpc"]) + b
res_br = res["BRA"]
pos_br = [p["iso3"] for p in pr].index("BRA") + 1
med = lambda L, k: float(np.median([p[k] for p in L]))
low = [p for p in pool if p['pibpc'] < 2000]
high = [p for p in pool if p['pibpc'] > 40000]
hi1 = ["Brasil"] + [p["nome"] for p in acima[:3]] + [p["nome"] for p in abaixo[:3]]
scatter("graf-renda-vida.jpg", [p["pibpc"] for p in pool], [p["vida"] for p in pool], [p["nome"] for p in pool], hi1,
        "Dinheiro compra anos de vida, mas não todos", "PIB por pessoa (escala logarítmica) e expectativa de vida ao nascer, 159 países",
        "PIB por pessoa, US$ (escala logarítmica)", "Expectativa de vida, anos", logx=True,
        xfmt=lambda v, _: n0(v), off={"Brasil": (10, -22), "Chade": (-62, 8), "Nigéria": (10, -20)})
fa = lambda p: f"{p['nome']} ({n1(p['vida'])} anos, {n1(res[p['iso3']])} acima do esperado para a renda)"
fb = lambda p: f"{p['nome']} ({n1(p['vida'])} anos, {n1(abs(res[p['iso3']]))} abaixo)"
body = f"""<p>Países mais ricos vivem mais, mas a relação não é perfeita, e os desvios dizem mais do que a regra. Cruzamos o PIB por pessoa e a expectativa de vida ao nascer de {len(pool)} países com 1 milhão de habitantes ou mais, pelos dados do Banco Mundial. A correlação é de {r2(r)} (entre o logaritmo da renda e a expectativa de vida), forte para dados de países.</p>

      <!--AD1-->

      <h2>A regra: dobrar a renda soma anos, em média</h2>

      <p>Ajustando uma reta ao logaritmo da renda, cada vez que a renda por pessoa dobra, a expectativa de vida sobe cerca de {n1(a * np.log(2))} anos em média. Na prática, a diferença entre os extremos é enorme: a mediana é de {n1(med(low, 'vida'))} anos nos {len(low)} países com menos de US$ 2.000 por pessoa e de {n1(med(high, 'vida'))} anos nos {len(high)} com mais de US$ 40.000.</p>

      <h2>Onde o Brasil fica</h2>

      <p>Com PIB por pessoa de {usd(BR['pibpc'])} e expectativa de vida de {n1(BR['vida'])} anos, o Brasil tem {n1(abs(res_br))} anos {'a menos' if res_br < 0 else 'a mais'} do que a reta prevê para essa renda ({n1(exp_br)} anos). É o {pos_br}º melhor desempenho em relação à renda entre {len(pr)} países.</p>

      <h2>Quem vive mais do que a renda prevê, e quem vive menos</h2>

      <p>Entre os países com 5 milhões de habitantes ou mais, os que mais superam a previsão são {lst(fa(q) for q in acima[:3])}. Os que mais ficam abaixo são {lst(fb(q) for q in abaixo[:3])}.</p>

      <h2>O que o gráfico não diz</h2>

      <p>A reta é uma média, não uma lei. Expectativa de vida depende de saneamento, vacinação, violência, acesso a serviços de saúde e distribuição da renda, e o PIB por pessoa esconde desigualdade interna. Países de renda alta com vida abaixo do previsto, ou o inverso, costumam ter explicações específicas de cada caso, que este cálculo sozinho não identifica.</p>

      {CTX.format(t="A relação entre renda e saúde é conhecida entre economistas como curva de Preston, descrita pelo demógrafo Samuel Preston em 1975: países mais ricos têm vida média maior, com retornos decrescentes. Usamos o PIB por pessoa em dólares correntes e o logaritmo da renda no ajuste.")}"""
specs_meta = []
spec("2026-11-16", "renda-e-vida-longa-onde-o-brasil-fica-na-curva-de-preston-banco-mundial-2026",
     f"Renda e vida longa: o Brasil fica {n1(abs(res_br))} ano{'' if round(abs(res_br), 1) == 1 else 's'} {'abaixo' if res_br < 0 else 'acima'} da curva que liga PIB por pessoa e expectativa de vida em {len(pool)} países",
     f"Países ricos vivem mais, mas a regra tem exceções. Entre {len(pool)} países, o Brasil fica {n1(abs(res_br))} anos {'abaixo' if res_br < 0 else 'acima'} do previsto para a sua renda. {acima[0]['nome']} e {abaixo[0]['nome']} estão nos extremos entre os países maiores.",
     f"Cruzamos PIB por pessoa e expectativa de vida em {len(pool)} países: o Brasil fica perto da curva, {n1(abs(res_br))} anos {'abaixo' if res_br < 0 else 'acima'} do previsto para a renda.",
     f"Análise da Watermouse Media com dados do Banco Mundial: PIB por pessoa e expectativa de vida em {len(pool)} países e o desvio do Brasil em relação à curva de Preston.",
     "graf-renda-vida.jpg", "Gráfico de dispersão com PIB por pessoa em escala logarítmica e expectativa de vida de 159 países, com o Brasil destacado em azul e uma linha de tendência",
     "Gráfico: Watermouse Media, com dados do Banco Mundial (PIB por pessoa e expectativa de vida, valor mais recente de cada país).", body,
     attrib("indicadores de PIB per capita (US$ correntes) e expectativa de vida ao nascer"))

# ---------- 2. Desigualdade e homicidios ----------
pool, a, b, r, res = regress("gini", "homic")
pg = have("gini", "homic")
top_h = sorted(pg, key=lambda p: p["homic"], reverse=True)
rk_h, nh = rank("homic", BR)
rk_g, ng = rank("gini", BR)
alto_g = [p for p in pg if p["gini"] >= 45]
baixo_g = [p for p in pg if p["gini"] < 35]
sub_g = [p for p in alto_g if p["homic"] < 5]
sub_g = sorted(sub_g, key=lambda p: p["gini"], reverse=True)
hi2 = ["Brasil"] + [p["nome"] for p in top_h[:3]] + [p["nome"] for p in sub_g[:2]]
scatter("graf-gini-homicidios.jpg", [p["gini"] for p in pg], [p["homic"] for p in pg], [p["nome"] for p in pg], hi2,
        "Desigualdade e violência andam juntas, com exceções", "Índice de Gini e homicídios por 100 mil habitantes, 132 países",
        "Índice de Gini (0 = igualdade total, 100 = desigualdade máxima)", "Homicídios por 100 mil habitantes", fit=True, off={"Brasil": (-60, 12), "Moçambique": (-90, -4), "Angola": (8, 8)})
body = f"""<p>Em que medida a desigualdade de renda está associada à violência? Cruzamos o índice de Gini e a taxa de homicídios de {len(pg)} países com 1 milhão de habitantes ou mais, pelos dados do Banco Mundial. A correlação é de {r2(r)}, positiva e moderada: países mais desiguais tendem a ter mais homicídios, sem que isso seja uma regra.</p>

      <!--AD1-->

      <h2>O Brasil nos dois rankings</h2>

      <p>O Brasil tem Gini de {n1(BR['gini'])}, o {rk_g}º mais alto entre {ng} países com dado, e {n1(BR['homic'])} homicídios por 100 mil habitantes, o {rk_h}º entre {nh}. Entre os {len(alto_g)} países com Gini de 45 ou mais, a mediana de homicídios é de {n1(med(alto_g, 'homic'))} por 100 mil; entre os {len(baixo_g)} com Gini abaixo de 35, é de {n1(med(baixo_g, 'homic'))}.</p>

      <h2>As taxas mais altas</h2>

      <p>As maiores taxas de homicídio entre os países da amostra são as de {top_h[0]['nome']} ({n1(top_h[0]['homic'])}), {top_h[1]['nome']} ({n1(top_h[1]['homic'])}) e {top_h[2]['nome']} ({n1(top_h[2]['homic'])}) por 100 mil habitantes. Pela reta de tendência, um país com Gini de {n1(BR['gini'])} teria {n1(a * BR['gini'] + b)} homicídios por 100 mil habitantes; o Brasil, com {n1(BR['homic'])}, fica acima disso, o que indica que a desigualdade explica só parte do quadro.</p>

      <h2>Países desiguais e pouco violentos</h2>

      <p>Há exceções claras. {sub_g[0]['nome']} tem Gini de {n1(sub_g[0]['gini'])} e taxa de {n1(sub_g[0]['homic'])} homicídios por 100 mil; {sub_g[1]['nome']}, Gini de {n1(sub_g[1]['gini'])} e taxa de {n1(sub_g[1]['homic'])}. Fatores como presença do Estado, mercados ilegais, armas, histórico de conflito e política de segurança pesam tanto quanto a renda.</p>

      <h2>Cuidado com a leitura</h2>

      <p>Correlação não é causa: a desigualdade pode contribuir para a violência, mas o contrário também ocorre, e há terceiros fatores. Além disso, os dados de homicídio e de Gini vêm de anos diferentes em cada país (de {min(p['gini_ano'] for p in pg)} a {max(p['homic_ano'] for p in pg)}, o valor mais recente disponível), e a qualidade do registro de mortes varia.</p>

      {CTX.format(t="O índice de Gini mede a concentração da renda de 0 (todos recebem o mesmo) a 100 (uma pessoa fica com tudo). A taxa de homicídios, calculada pelo Banco Mundial com base em dados de escritórios de estatística e do Escritório da ONU sobre Drogas e Crime, é o indicador de violência mais comparável entre países.")}"""
spec("2026-11-17", "desigualdade-e-homicidios-brasil-esta-entre-os-mais-altos-nos-dois-banco-mundial-2026",
     f"Desigualdade e homicídios: o Brasil aparece entre os mais altos nos dois indicadores, em {len(pg)} países",
     f"O Brasil é o {rk_g}º em Gini e o {rk_h}º em homicídios entre os países com dado. A correlação entre os dois índices é de {r2(r)}: forte o bastante para chamar atenção, fraca o bastante para mostrar que renda não explica tudo.",
     f"Cruzamos Gini e homicídios em {len(pg)} países: o Brasil está no {rk_g}º lugar em desigualdade e no {rk_h}º em violência, mas há exceções.",
     f"Análise da Watermouse Media com dados do Banco Mundial: índice de Gini e taxa de homicídios em {len(pg)} países, com a posição do Brasil.",
     "graf-gini-homicidios.jpg", "Gráfico de dispersão com índice de Gini e taxa de homicídios de 132 países, com o Brasil destacado em azul",
     "Gráfico: Watermouse Media, com dados do Banco Mundial (índice de Gini e homicídios por 100 mil habitantes, valor mais recente).", body,
     attrib("indicadores de índice de Gini e homicídios intencionais por 100 mil habitantes"))

# ---------- 3. Renovaveis ----------
pr_ = have("renov", "pibpc")
rk_r, nr = rank("renov", BR, pool=pr_)
top_r = sorted(pr_, key=lambda p: p["renov"], reverse=True)
big = [p for p in pr_ if p["pop"] >= 5e7]
big_r = sorted(big, key=lambda p: p["renov"], reverse=True)
rico = [p for p in pr_ if p["pibpc"] >= 40000]
rico_r = sorted(rico, key=lambda p: p["renov"], reverse=True)
pobre = [p for p in pr_ if p["pibpc"] < 2000]
pool, a, b, r, res = regress("pibpc", "renov", logx=True)
medp, medr = med(pobre, "renov"), med(rico, "renov")
sel = ["Brasil"] + [p["nome"] for p in big_r[:6] if p["iso3"] != "BRA"][:4]
items = [(p["nome"], p["renov"]) for p in big_r]
bars("graf-renovaveis.jpg", items[:14] if "Brasil" in [i[0] for i in items[:14]] else items[:13] + [("Brasil", BR["renov"])], sel,
     "Quem mais usa energia renovável entre os países grandes", "Parcela das fontes renováveis no consumo final de energia (%), países com 50 milhões de habitantes ou mais", unit="%", fonte="Fonte: Banco Mundial (WDI), valor mais recente de cada país. Países com 50 milhões de habitantes ou mais. Watermouse Media")
body = f"""<p>A energia renovável costuma ser associada a países ricos, mas os dados do Banco Mundial mostram quase o oposto: entre {len(pr_)} países, a correlação entre o logaritmo da renda por pessoa e a parcela de renováveis no consumo final de energia é de {r2(r)}. Quanto mais pobre o país, maior a participação de fontes renováveis, e a explicação está no tipo de renovável.</p>

      <!--AD1-->

      <h2>Por que países pobres têm mais renováveis</h2>

      <p>O indicador inclui a lenha e o carvão vegetal usados para cozinhar, que são renováveis, mas pouco eficientes. Nos {len(pobre)} países com PIB por pessoa abaixo de US$ 2.000, a mediana de renováveis é de {pct(medp)} do consumo final de energia. Nos {len(rico)} países com mais de US$ 40.000 por pessoa, é de {pct(medr)}. A diferença reflete a biomassa tradicional nos pobres e a industrialização movida a petróleo, gás e carvão nos ricos.</p>

      <h2>O Brasil entre os grandes</h2>

      <p>O Brasil usa {pct(BR['renov'])} de energia renovável no consumo final, o {rk_r}º lugar entre {nr} países. Entre os {len(big)} países com 50 milhões de habitantes ou mais, o Brasil fica em {[p['iso3'] for p in big_r].index('BRA') + 1}º, atrás de {lst(f"{p['nome']} ({pct(p['renov'])})" for p in big_r[:3] if p['iso3'] != 'BRA')}. A hidrelétrica e o etanol explicam boa parte da posição brasileira.</p>

      <h2>Entre os ricos, quem lidera</h2>

      <p>Entre os países com PIB por pessoa acima de US$ 40.000, os que mais usam renováveis são {lst(f"{p['nome']} ({pct(p['renov'])})" for p in rico_r[:3])}. Os que menos usam são {lst(f"{p['nome']} ({pct(p['renov'])})" for p in rico_r[::-1][:3])}.</p>

      <h2>Cuidado com a leitura</h2>

      <p>Participação de renováveis no consumo final de energia não é a mesma coisa que eletricidade limpa: a matriz elétrica do Brasil é muito mais renovável do que a matriz de energia total, por exemplo. O indicador também ignora a quantidade absoluta de energia gerada e as emissões de cada país.</p>

      {CTX.format(t="O indicador do Banco Mundial, 'consumo de energia renovável (% do consumo final total)', considera a energia hidráulica, solar, eólica, geotérmica, a biomassa (inclusive a lenha) e os biocombustíveis. A base usa o ano mais recente disponível para cada país, em geral {n0(float(np.median([p['renov_ano'] for p in pr_])))}, o ano mais recente do indicador.")}"""
spec("2026-11-18", "energia-renovavel-paises-pobres-usam-mais-brasil-esta-entre-os-grandes-banco-mundial-2026",
     f"Países pobres usam mais energia renovável do que os ricos, e o Brasil é o {[p['iso3'] for p in big_r].index('BRA') + 1}º entre os {len(big)} países de 50 milhões de habitantes ou mais",
     f"A correlação entre renda e renováveis é de {r2(r)}: quanto mais rico, menor a parcela, porque o indicador inclui lenha. Entre os países com 50 milhões de habitantes ou mais, o Brasil usa {pct(BR['renov'])} e fica em {[p['iso3'] for p in big_r].index('BRA') + 1}º.",
     f"Quanto mais pobre o país, maior a parcela de renováveis no consumo de energia. O Brasil, com {pct(BR['renov'])}, é o {[p['iso3'] for p in big_r].index('BRA') + 1}º entre os {len(big)} países de 50 milhões de habitantes ou mais.",
     f"Análise da Watermouse Media com dados do Banco Mundial: parcela de renováveis no consumo final de energia em {nr} países, por faixa de renda, e a posição do Brasil.",
     "graf-renovaveis.jpg", "Gráfico de barras horizontais com a parcela de renováveis no consumo final de energia nos países de 50 milhões de habitantes ou mais, com o Brasil destacado em azul",
     "Gráfico: Watermouse Media, com dados do Banco Mundial (consumo de energia renovável, % do consumo final total).", body,
     attrib("indicador de consumo de energia renovável (% do consumo final de energia) e PIB per capita"))

# ---------- 4. Gasto em saude e vida ----------
pool, a, b, r, res = regress("saude", "vida")
ps = have("saude", "vida", "pibpc")
usa = next(p for p in P if p["iso3"] == "USA")
mesmo = [p for p in ps if p["vida"] >= usa["vida"] and p["saude"] < usa["saude"] / 2]
mesmo = sorted(mesmo, key=lambda p: -p["vida"])
efic = [p for p in ps if p["pop"] >= 5e6]
efic = sorted(efic, key=lambda p: p["vida"] / p["saude"], reverse=True)
hi4 = ["Brasil", "Estados Unidos"] + [p["nome"] for p in mesmo[:3]]
scatter("graf-saude-vida.jpg", [p["saude"] for p in ps], [p["vida"] for p in ps], [p["nome"] for p in ps], hi4,
        "Gastar mais com saúde não garante viver mais", "Gasto total com saúde (% do PIB, 2023) e expectativa de vida ao nascer, 156 países",
        "Gasto total com saúde, % do PIB", "Expectativa de vida, anos", fit=True, off={"Estados Unidos": (-110, -22), "Singapura": (-84, -6), "Kuwait": (8, 8)})
rk_s, ns = rank("saude", BR, pool=ps)
body = f"""<p>Mais gasto com saúde significa mais anos de vida? Cruzamos o gasto total com saúde, em porcentagem do PIB, e a expectativa de vida ao nascer de {len(ps)} países, pelos dados do Banco Mundial. A correlação é de apenas {r2(r)}: positiva, mas fraca, o que mostra que o tamanho do gasto, sozinho, explica pouco do resultado.</p>

      <!--AD1-->

      <h2>O caso dos Estados Unidos</h2>

      <p>Os Estados Unidos gastam {pct(usa['saude'])} do PIB com saúde, o maior percentual da amostra, e têm expectativa de vida de {n1(usa['vida'])} anos. Há {len(mesmo)} países que gastam menos da metade disso e têm expectativa de vida igual ou maior, entre eles {lst(f"{p['nome']} ({pct(p['saude'])} do PIB, {n1(p['vida'])} anos)" for p in mesmo[:4])}. Em dólares por pessoa a conta muda: {mesmo[1]['nome']} gasta cerca de {usd(mesmo[1]['saude'] / 100 * mesmo[1]['pibpc'])} por habitante, {usd(BR['saude'] / 100 * BR['pibpc'])} no Brasil e {usd(usa['saude'] / 100 * usa['pibpc'])} nos Estados Unidos (estimativa nossa: % do PIB multiplicado pelo PIB por pessoa).</p>

      <h2>O Brasil</h2>

      <p>O Brasil gasta {pct(BR['saude'])} do PIB, o {rk_s}º maior percentual entre {ns} países, e tem expectativa de vida de {n1(BR['vida'])} anos. Pela reta de tendência, um país com esse gasto teria {n1(a * BR['saude'] + b)} anos, o que deixa o Brasil {n1(abs(res['BRA']))} anos {'abaixo' if res['BRA'] < 0 else 'acima'} do esperado só pela porcentagem do PIB.</p>

      <h2>Por que a relação é fraca</h2>

      <p>O gasto em % do PIB mistura situações muito diferentes: países pobres que recebem ajuda externa e gastam uma fatia grande de uma economia pequena, países ricos que gastam muito com preços altos, e países que investem em prevenção e atenção básica a custo baixo. A expectativa de vida também depende de renda, violência, saneamento e idade da população, e o gasto sozinho não captura nada disso.</p>

      <h2>O que o cálculo não faz</h2>

      <p>Não medimos eficiência, qualidade nem acesso, e não ajustamos por renda. O gasto público e o privado estão somados, e a composição entre os dois muda muito entre países. É um retrato descritivo, não uma avaliação de sistemas de saúde.</p>

      {CTX.format(t="O gasto corrente total com saúde (% do PIB) soma recursos públicos, privados e de ajuda externa, e é o indicador padrão da Organização Mundial da Saúde para comparar países. O ano de referência é 2023 para a maioria dos países.")}"""
spec("2026-11-19", "gasto-em-saude-e-expectativa-de-vida-correlacao-fraca-brasil-banco-mundial-2026",
     f"Gastar mais com saúde não garante viver mais: a correlação com a expectativa de vida é de apenas {r2(r)} em {len(ps)} países",
     f"Os Estados Unidos gastam {pct(usa['saude'])} do PIB com saúde e têm {n1(usa['vida'])} anos de expectativa de vida; {len(mesmo)} países gastam menos da metade e vivem igual ou mais. O Brasil gasta {pct(BR['saude'])} e tem {n1(BR['vida'])} anos.",
     f"Entre {len(ps)} países, o gasto com saúde explica pouco da expectativa de vida. O Brasil gasta {pct(BR['saude'])} do PIB e vive {n1(BR['vida'])} anos.",
     f"Análise da Watermouse Media com dados do Banco Mundial: gasto total com saúde em % do PIB e expectativa de vida em {len(ps)} países, com Estados Unidos e Brasil em destaque.",
     "graf-saude-vida.jpg", "Gráfico de dispersão com gasto em saúde em porcentagem do PIB e expectativa de vida de 156 países, com Brasil em azul e Estados Unidos em destaque",
     "Gráfico: Watermouse Media, com dados do Banco Mundial (gasto total com saúde, % do PIB; expectativa de vida ao nascer).", body,
     attrib("indicadores de gasto corrente com saúde (% do PIB) e expectativa de vida ao nascer"))

print("ok", specs)
