# -*- coding: utf-8 -*-
"""Terceira leva de analises de dados proprias (Banco Mundial): CO2 x renda, poder de compra (PPC/nominal),
urbanizacao x fecundidade, desigualdade x renda, emissoes x renovaveis. Reusa helpers de analises_dados.py.
Uso: python -I tools/analises_dados3.py"""
import pathlib, sys
SRC = (pathlib.Path(__file__).resolve().parent / "analises_dados.py").read_text(encoding="utf-8")
exec(compile(SRC.split("# ---------- 1. Renda e vida longa ----------")[0], "analises_dados_helpers", "exec"))
import numpy as np

med = lambda L, k: float(np.median([p[k] for p in L]))
sg = lambda v, un, pl: un if round(abs(v), 1) == 1 else pl

# ---------- A. CO2 por pessoa x renda ----------
pool, a, b, r, res = regress("pibpc", "co2pc", logx=True)
pool = [p for p in pool if p["co2pc"] > 0]
x = np.log([p["pibpc"] for p in pool]); y = np.log([p["co2pc"] for p in pool])
a2, b2 = np.polyfit(x, y, 1); r_ll = float(np.corrcoef(x, y)[0, 1])
resl = {p["iso3"]: float(y[i] - (a2 * x[i] + b2)) for i, p in enumerate(pool)}
exp_br = float(np.exp(a2 * np.log(BR["pibpc"]) + b2))
rk_c, nc = rank("co2pc", BR, pool=pool)
big = sorted([p for p in pool if p["pop"] >= 5e6], key=lambda p: resl[p["iso3"]])
limpos, sujos = big[:3], big[::-1][:3]
hiA = ["Brasil"] + [p["nome"] for p in limpos] + [p["nome"] for p in sujos]
scatter("graf-co2-renda.jpg", [p["pibpc"] for p in pool], [p["co2pc"] for p in pool], [p["nome"] for p in pool], hiA,
        "Quem é rico emite mais, mas nem todo rico emite igual", "PIB por pessoa e emissões de CO2 por pessoa, ambos em escala logarítmica",
        "PIB por pessoa, US$ (escala logarítmica)", "Toneladas de CO2 por pessoa por ano (escala logarítmica)", logx=True, fit=False, xfmt=lambda v, _: n0(v), off={"Brasil": (10, -22)})
import matplotlib.pyplot as plt  # redesenha com eixo y log
fig, ax = plt.subplots(figsize=(16.8, 8.96), dpi=100); fig.subplots_adjust(left=0.07, right=0.97, top=0.78, bottom=0.14)
ax.scatter([p["pibpc"] for p in pool], [p["co2pc"] for p in pool], s=46, color=GREY, alpha=0.75, edgecolor="none", zorder=2)
gx = np.linspace(x.min(), x.max(), 100); ax.plot(np.exp(gx), np.exp(a2 * gx + b2), color=INK, lw=1.8, ls=(0, (6, 4)), zorder=3)
offs = {"Brasil": (10, -22)}
for p in pool:
    if p["nome"] in hiA:
        ax.scatter([p["pibpc"]], [p["co2pc"]], s=190 if p["nome"] == "Brasil" else 90, color=BLUE if p["nome"] == "Brasil" else INK, zorder=5)
        dx, dy = offs.get(p["nome"], (8, 8))
        ax.annotate(p["nome"], (p["pibpc"], p["co2pc"]), xytext=(dx, dy), textcoords="offset points", family=SERIF, fontsize=17 if p["nome"] == "Brasil" else 14.5,
                    fontweight="bold" if p["nome"] == "Brasil" else "normal", color=BLUE if p["nome"] == "Brasil" else INK, zorder=6)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("PIB por pessoa, US$ (escala logarítmica)", family=SERIF, fontsize=16, color=INK, labelpad=10)
ax.set_ylabel("Toneladas de CO2 por pessoa por ano (escala logarítmica)", family=SERIF, fontsize=16, color=INK, labelpad=10)
ax.grid(color=LIGHT, lw=0.8, zorder=0)
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: n0(v))); ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: n1(v) if v < 10 else n0(v)))
frame(fig, ax, "Quem é rico emite mais, mas nem todo rico emite igual", "PIB por pessoa e emissões de CO2 por pessoa, ambos em escala logarítmica")
fig.savefig(ROOT / "media" / "graf-co2-renda.jpg", pil_kwargs={"quality": 92}, facecolor=BG); plt.close(fig)
fc = lambda p: f"{p['nome']} ({n1(p['co2pc'])} t por pessoa)"
body = f"""<p>As emissões de dióxido de carbono por pessoa crescem com a renda: cruzamos o PIB por pessoa e as emissões de CO2 por habitante de {len(pool)} países com 1 milhão de habitantes ou mais, pelos dados do Banco Mundial, e a correlação (em logaritmos) é de {r2(r_ll)}. Mas a regra tem exceções importantes: países com a mesma renda emitem quantidades muito diferentes.</p>

      <!--AD1-->

      <h2>O Brasil: abaixo da média para a renda que tem</h2>

      <p>O Brasil emite {n1(BR['co2pc'])} toneladas de CO2 por pessoa por ano, o {rk_c}º maior valor entre {nc} países. Para a renda de {usd(BR['pibpc'])} por pessoa, a reta indica cerca de {n1(exp_br)} toneladas, então o Brasil emite {'menos' if BR['co2pc'] < exp_br else 'mais'} do que a renda sugere. A matriz com muita hidrelétrica e biocombustíveis ajuda, mas as emissões do país têm peso grande do desmatamento e da agropecuária, que este indicador de combustíveis fósseis e cimento não mede.</p>

      <h2>Quem emite menos do que a renda indica</h2>

      <p>Entre os países com 5 milhões de habitantes ou mais, os que mais ficam abaixo do esperado são {lst(fc(q) for q in limpos)}. Os que mais ficam acima são {lst(fc(q) for q in sujos)}.</p>

      <h2>Limites do indicador</h2>

      <p>O dado considera as emissões produzidas dentro do território, sem contar o carbono embutido no que o país importa. Países que importam bens de fábricas estrangeiras emitem menos no papel do que consomem de fato. A medida também ignora emissões por mudança no uso da terra, como o desmatamento.</p>

      {CTX.format(t="O indicador de emissões de CO2 do Banco Mundial vem do projeto Global Carbon e mede o dióxido de carbono liberado pela queima de combustíveis fósseis e pela fabricação de cimento, em toneladas por pessoa. O PIB por pessoa é em dólares correntes.")}"""
spec("2026-11-26", "emissoes-de-co2-e-renda-brasil-emite-menos-do-que-a-renda-sugere-banco-mundial-2026",
     f"Emissões de CO2 e renda: o Brasil emite {'menos' if BR['co2pc'] < exp_br else 'mais'} do que a renda sugere, em {len(pool)} países",
     f"O Brasil emite {n1(BR['co2pc'])} toneladas de CO2 por pessoa, o {rk_c}º maior valor entre {nc} países. A correlação entre renda e emissões é de {r2(r_ll)}, mas {limpos[0]['nome']} e {sujos[0]['nome']} mostram que a renda não decide tudo.",
     f"Entre {len(pool)} países, o Brasil emite {n1(BR['co2pc'])} toneladas de CO2 por pessoa, {'abaixo' if BR['co2pc'] < exp_br else 'acima'} do que a renda sugere.",
     f"Análise da Watermouse Media com dados do Banco Mundial: emissões de CO2 por pessoa e PIB por pessoa em {len(pool)} países, com a posição do Brasil.",
     "graf-co2-renda.jpg", "Gráfico de dispersão com PIB por pessoa e emissões de CO2 por pessoa em escala logarítmica, com o Brasil destacado em azul",
     "Gráfico: Watermouse Media, com dados do Banco Mundial (PIB por pessoa e emissões de CO2 por pessoa, valor mais recente).", body,
     attrib("indicadores de emissões de CO2 por habitante e PIB per capita"))

# ---------- B. Poder de compra: PPC / nominal ----------
pp = [p for p in have("pibppc", "pibpc") if p["pibpc"] > 0]
for p in pp:
    p["_rz"] = p["pibppc"] / p["pibpc"]
pp_s = sorted(pp, key=lambda p: p["_rz"], reverse=True)
rk_z = [p["iso3"] for p in pp_s].index("BRA") + 1
alto, baixo = pp_s[:3], pp_s[::-1][:3]
mzr = float(np.median([p["_rz"] for p in pp]))
items = [(p["nome"], p["_rz"]) for p in pp_s[:6]] + [("Brasil", BR["pibppc"] / BR["pibpc"])] + [(p["nome"], p["_rz"]) for p in pp_s[::-1][:4][::-1]]
bars("graf-poder-de-compra.jpg", items, ["Brasil"], "Quanto um dólar rende em cada país", "PIB por pessoa em paridade de poder de compra dividido pelo PIB por pessoa em dólares correntes",
     unit="x", fonte="Fonte: Banco Mundial (WDI), valor mais recente. Países com 1 milhão de habitantes ou mais. Cálculo da Watermouse Media")
body = f"""<p>O PIB por pessoa em dólares correntes engana quando o custo de vida é muito diferente de um país para outro. A paridade de poder de compra (PPC) corrige isso, e a razão entre as duas medidas diz quanto mais (ou menos) um dólar rende em cada lugar. Calculamos essa razão para {len(pp)} países com 1 milhão de habitantes ou mais, com dados do Banco Mundial. A mediana é de {n1(mzr)} vezes.</p>

      <!--AD1-->

      <h2>O Brasil: {n1(BR['pibppc'] / BR['pibpc'])} vezes</h2>

      <p>O PIB por pessoa do Brasil é de {usd(BR['pibpc'])} em dólares correntes e de {usd(BR['pibppc'])} em PPC. A razão é de {n1(BR['pibppc'] / BR['pibpc'])} vezes, o {rk_z}º lugar entre {len(pp)} países. Isso significa que, em média, o dinheiro no Brasil compra mais do que a conta em dólares sugere, mas menos do que na mediana dos países ({n1(mzr)} vezes).</p>

      <h2>Onde o dólar rende mais</h2>

      <p>As razões mais altas são as de {lst(f"{p['nome']} ({n1(p['_rz'])} vezes)" for p in alto)}. Nesses países, os preços locais de bens e serviços são mais baixos do que seriam nos Estados Unidos, e o PIB em PPC é bem maior que o nominal. A razão alta também pode refletir desvalorizações recentes da moeda, que reduzem o PIB medido em dólares correntes.</p>

      <h2>Onde o dólar rende menos</h2>

      <p>As razões mais baixas são as de {lst(f"{p['nome']} ({n1(p['_rz'])} vezes)" for p in baixo)}, onde o custo de vida é alto em relação à renda em dólares.</p>

      <h2>Cuidados</h2>

      <p>A PPC compara cestas de bens padronizadas, e a cesta de quem vive em cada lugar pode ser bem diferente. A estimativa vem do Programa de Comparação Internacional, que revê os preços periodicamente, e alguns países têm dados mais antigos ou mais incertos.</p>

      {CTX.format(t="O PIB por pessoa em PPC converte a renda de cada país para uma moeda comum levando em conta quanto custa uma mesma cesta de bens e serviços em cada lugar. O dólar internacional equivale ao que um dólar compraria nos Estados Unidos.")}"""
spec("2026-11-27", "poder-de-compra-quanto-um-dolar-rende-em-cada-pais-brasil-ppc-banco-mundial-2026",
     f"Poder de compra: o Brasil tem razão de {n1(BR['pibppc'] / BR['pibpc'])} entre PIB em PPC e PIB nominal, o {rk_z}º entre {len(pp)} países",
     f"Dividindo o PIB por pessoa em PPC pelo nominal, a mediana mundial é de {n1(mzr)} vezes e o Brasil fica em {n1(BR['pibppc'] / BR['pibpc'])}. A razão mostra onde o dólar rende mais ou menos.",
     f"Um dólar rende {n1(BR['pibppc'] / BR['pibpc'])} vezes mais no Brasil do que o câmbio sugere, o {rk_z}º lugar entre {len(pp)} países.",
     f"Análise da Watermouse Media com dados do Banco Mundial: razão entre PIB por pessoa em PPC e em dólares correntes de {len(pp)} países, com a posição do Brasil.",
     "graf-poder-de-compra.jpg", "Gráfico de barras horizontais com a razão entre PIB em PPC e PIB nominal por pessoa, com o Brasil destacado em azul",
     "Gráfico: Watermouse Media, com dados do Banco Mundial (PIB per capita em PPC e em dólares correntes).", body,
     attrib("indicadores de PIB per capita em PPC (dólares internacionais correntes) e PIB per capita em US$ correntes"))

# ---------- C. Urbanizacao x fecundidade ----------
pu = have("urb", "fert")
pool, a, b, r, res = regress("urb", "fert")
rk_f, nf = rank("fert", BR, rev=False, pool=pu)
altas = sorted([p for p in pu if p["pop"] >= 5e6], key=lambda p: p["fert"], reverse=True)[:3]
baixas = sorted([p for p in pu if p["pop"] >= 5e6], key=lambda p: p["fert"])[:3]
abaixo_rep = [p for p in pu if p["fert"] < 2.1]
rural = [p for p in pu if p["urb"] < 40]; urbano = [p for p in pu if p["urb"] >= 80]
hiC = ["Brasil"] + [p["nome"] for p in altas[:2]] + [p["nome"] for p in baixas[:2]]
scatter("graf-urbanizacao-fecundidade.jpg", [p["urb"] for p in pu], [p["fert"] for p in pu], [p["nome"] for p in pu], hiC,
        "Quanto mais urbano o país, menos filhos por mulher", "População urbana (%) e filhos por mulher, 159 países",
        "População urbana, % do total", "Filhos por mulher", off={"Brasil": (10, 10)})
body = f"""<p>Vida na cidade e tamanho da família andam em direções opostas. Cruzamos a parcela de população urbana e a taxa de fecundidade (filhos por mulher) de {len(pu)} países com 1 milhão de habitantes ou mais, com dados do Banco Mundial, e a correlação é de {r2(r)}: quanto mais urbano o país, menos filhos por mulher, em média.</p>

      <!--AD1-->

      <h2>O Brasil</h2>

      <p>O Brasil tem {pct(BR['urb'])} da população em áreas urbanas e {n1(BR['fert'])} filhos por mulher, o {rk_f}º menor valor entre {nf} países. A taxa está abaixo do nível de reposição, em torno de 2,1 filhos por mulher, que mantém a população estável sem migração. Para a parcela urbana que tem, a reta prevê {n1(a * BR['urb'] + b)} filhos por mulher.</p>

      <h2>Dois mundos</h2>

      <p>Nos {len(rural)} países com menos de 40% de população urbana, a mediana é de {n1(med(rural, 'fert'))} filhos por mulher. Nos {len(urbano)} países com 80% ou mais, é de {n1(med(urbano, 'fert'))}. Dos {len(pu)} países da amostra, {len(abaixo_rep)} estão abaixo do nível de reposição.</p>

      <h2>Extremos</h2>

      <p>Entre os países com 5 milhões de habitantes ou mais, as maiores taxas são as de {lst(f"{p['nome']} ({n1(p['fert'])})" for p in altas)}, e as menores, as de {lst(f"{p['nome']} ({n1(p['fert'])})" for p in baixas)}.</p>

      <h2>O que a relação não prova</h2>

      <p>Cidade não reduz filhos por si só: urbanização anda junto com escolaridade das mulheres, renda, acesso a contracepção e custo de moradia, e todos esses fatores afetam a decisão. Há também países urbanos com fecundidade alta, o que mostra que o padrão tem exceções.</p>

      {CTX.format(t="A taxa de fecundidade total é o número médio de filhos que uma mulher teria ao longo da vida se vivesse conforme as taxas de fecundidade de cada idade observadas naquele ano. A população urbana segue a definição de cada país, compilada pela ONU.")}"""
spec("2026-11-28", "urbanizacao-e-fecundidade-quanto-mais-urbano-menos-filhos-brasil-banco-mundial-2026",
     f"Urbanização e fecundidade: com {pct(BR['urb'])} de população urbana, o Brasil tem {n1(BR['fert'])} filhos por mulher, abaixo da reposição",
     f"Entre {len(pu)} países, a correlação entre população urbana e filhos por mulher é de {r2(r)}. O Brasil é o {rk_f}º com menor fecundidade, e {len(abaixo_rep)} países estão abaixo da reposição.",
     f"Países mais urbanos têm menos filhos por mulher. O Brasil tem {pct(BR['urb'])} de população urbana e {n1(BR['fert'])} filhos por mulher.",
     f"Análise da Watermouse Media com dados do Banco Mundial: população urbana e taxa de fecundidade em {len(pu)} países, com a posição do Brasil.",
     "graf-urbanizacao-fecundidade.jpg", "Gráfico de dispersão com população urbana e filhos por mulher de 159 países, com o Brasil destacado em azul",
     "Gráfico: Watermouse Media, com dados do Banco Mundial (população urbana, % do total, e taxa de fecundidade total).", body,
     attrib("indicadores de população urbana (% do total) e taxa de fecundidade total (nascimentos por mulher)"))

# ---------- D. Desigualdade x renda ----------
pg = have("gini", "pibpc")
pool, a, b, r, res = regress("pibpc", "gini", logx=True)
rk_g, ng = rank("gini", BR, pool=pg)
ricos = [p for p in pg if p["pibpc"] >= 30000]
desig_r = sorted(ricos, key=lambda p: p["gini"], reverse=True)[:3]
iguais_pobres = sorted([p for p in pg if p["pibpc"] < 5000], key=lambda p: p["gini"])[:3]
hiD = ["Brasil"] + [p["nome"] for p in desig_r[:2]] + [p["nome"] for p in iguais_pobres[:2]]
scatter("graf-gini-renda.jpg", [p["pibpc"] for p in pg], [p["gini"] for p in pg], [p["nome"] for p in pg], hiD,
        "Países ricos são mais iguais, mas só em parte", "PIB por pessoa (escala logarítmica) e índice de Gini, 145 países",
        "PIB por pessoa, US$ (escala logarítmica)", "Índice de Gini (0 = igualdade, 100 = máxima desigualdade)", logx=True, xfmt=lambda v, _: n0(v), off={"Brasil": (10, 10)})
body = f"""<p>Renda alta garante distribuição mais igual? Os dados dizem que não. Cruzamos o PIB por pessoa e o índice de Gini de {len(pg)} países, com dados do Banco Mundial, e a correlação (em logaritmos da renda) é de apenas {r2(r)}: negativa, mas fraca. Países mais ricos tendem a ser um pouco mais igualitários, com muitas exceções.</p>

      <!--AD1-->

      <h2>O Brasil</h2>

      <p>O Brasil tem Gini de {n1(BR['gini'])}, o {rk_g}º mais alto entre {ng} países, para uma renda de {usd(BR['pibpc'])} por pessoa. A reta de tendência indica Gini de {n1(a * np.log(BR['pibpc']) + b)} para essa renda, então a desigualdade brasileira fica {n1(abs(res['BRA']))} pontos {'acima' if res['BRA'] > 0 else 'abaixo'} do esperado.</p>

      <h2>Ricos desiguais, pobres mais iguais</h2>

      <p>Entre os {len(ricos)} países com PIB por pessoa acima de US$ 30.000, os mais desiguais são {lst(f"{p['nome']} (Gini {n1(p['gini'])})" for p in desig_r)}. Entre os países com renda abaixo de US$ 5.000, os mais igualitários são {lst(f"{p['nome']} (Gini {n1(p['gini'])})" for p in iguais_pobres)}.</p>

      <h2>O que isso mostra</h2>

      <p>Renda média e distribuição são coisas diferentes: crescer não reduz a desigualdade automaticamente, e países de renda parecida chegam a patamares bem distintos de Gini, como resultado de impostos, transferências, educação e mercado de trabalho. Também é bom lembrar que o Gini vem de pesquisas domiciliares de anos diferentes e mede a distribuição de renda ou de consumo, conforme o país.</p>

      {CTX.format(t="O índice de Gini vai de 0, em que todos teriam a mesma renda, a 100, em que uma pessoa ficaria com tudo. Os dados do Banco Mundial vêm de pesquisas domiciliares e cada país tem um ano de referência próprio.")}"""
spec("2026-11-29", "desigualdade-e-renda-paises-ricos-sao-mais-iguais-so-em-parte-brasil-banco-mundial-2026",
     f"Desigualdade e renda: com Gini de {n1(BR['gini'])}, o Brasil é o {rk_g}º mais desigual entre {ng} países, {n1(abs(res['BRA']))} pontos {'acima' if res['BRA'] > 0 else 'abaixo'} do previsto para a renda",
     f"A correlação entre renda e Gini é de apenas {r2(r)} em {len(pg)} países. Países ricos como {desig_r[0]['nome']} são desiguais, e países pobres como {iguais_pobres[0]['nome']} são mais iguais.",
     f"Renda alta não garante igualdade: a correlação com o Gini é de {r2(r)}. O Brasil tem Gini de {n1(BR['gini'])}.",
     f"Análise da Watermouse Media com dados do Banco Mundial: PIB por pessoa e índice de Gini em {len(pg)} países, com a posição do Brasil.",
     "graf-gini-renda.jpg", "Gráfico de dispersão com PIB por pessoa em escala logarítmica e índice de Gini de 145 países, com o Brasil destacado em azul",
     "Gráfico: Watermouse Media, com dados do Banco Mundial (PIB por pessoa e índice de Gini, valor mais recente).", body,
     attrib("indicadores de índice de Gini e PIB per capita"))

# ---------- E. Emissoes x renovaveis ----------
pe = have("co2pc", "renov")
pool, a, b, r, res = regress("renov", "co2pc")
rk_e, ne = rank("co2pc", BR, pool=pe)
alta_ren_baixa_emis = sorted([p for p in pe if p["renov"] >= 50 and p["pop"] >= 5e6], key=lambda p: p["co2pc"])[:3]
baixa_ren_alta_emis = sorted([p for p in pe if p["renov"] < 15 and p["pop"] >= 5e6], key=lambda p: p["co2pc"], reverse=True)[:3]
quase = [p for p in pe if p["renov"] >= 50 and p["co2pc"] > 5]
hiE = ["Brasil"] + [p["nome"] for p in alta_ren_baixa_emis[:2]] + [p["nome"] for p in baixa_ren_alta_emis[:2]]
scatter("graf-renovaveis-emissoes.jpg", [p["renov"] for p in pe], [p["co2pc"] for p in pe], [p["nome"] for p in pe], hiE,
        "Mais energia renovável, menos CO2 por pessoa, em geral", "Parcela de renováveis no consumo de energia (%) e emissões de CO2 por pessoa, 155 países",
        "Energia renovável, % do consumo final", "Toneladas de CO2 por pessoa por ano", off={"Brasil": (10, 10)})
body = f"""<p>Energia renovável deveria andar junto com menos emissões, e em média anda: cruzamos a parcela de renováveis no consumo final de energia e as emissões de CO2 por pessoa de {len(pe)} países, pelos dados do Banco Mundial, e a correlação é de {r2(r)}. Mas ela é moderada, porque outros fatores, como a renda e a indústria, pesam mais.</p>

      <!--AD1-->

      <h2>O Brasil</h2>

      <p>O Brasil usa {pct(BR['renov'])} de energia renovável e emite {n1(BR['co2pc'])} toneladas de CO2 por pessoa, o {rk_e}º maior valor entre {ne} países. Para a parcela de renováveis que tem, a reta prevê {n1(a * BR['renov'] + b)} toneladas, então o Brasil emite {n1(abs(res['BRA']))} t por pessoa {'a menos' if res['BRA'] < 0 else 'a mais'} do que o esperado para uma parcela de renováveis como a dele.</p>

      <h2>Quem combina bem os dois</h2>

      <p>Entre os países com 5 milhões de habitantes ou mais e pelo menos metade da energia renovável, os que menos emitem por pessoa são {lst(f"{p['nome']} ({pct(p['renov'])} de renováveis, {n1(p['co2pc'])} t por pessoa)" for p in alta_ren_baixa_emis)}. Em vários deles, boa parte da renovável é lenha e carvão vegetal usados para cozinhar, e as emissões são baixas também porque o consumo de energia é pequeno.</p>

      <h2>E quem emite muito mesmo com pouca renovável</h2>

      <p>Os países com menos de 15% de renováveis e as maiores emissões por pessoa são {lst(f"{p['nome']} ({pct(p['renov'])}, {n1(p['co2pc'])} t por pessoa)" for p in baixa_ren_alta_emis)}. Há também {len(quase)} países com 50% ou mais de renováveis e emissões acima de 5 toneladas por pessoa, o que mostra que alta participação de renováveis não elimina as emissões de um país industrializado.</p>

      <h2>Limites</h2>

      <p>A parcela de renováveis mede o consumo final de energia, não a eletricidade, e as emissões do indicador vêm de combustíveis fósseis e cimento. Os dois indicadores têm anos de referência diferentes, o que pode distorcer países que mudaram a matriz recentemente.</p>

      {CTX.format(t="O consumo de energia renovável (% do consumo final) inclui hidrelétrica, solar, eólica, geotérmica, biomassa e biocombustíveis. As emissões de CO2 por pessoa são em toneladas e vêm do projeto Global Carbon.")}"""
spec("2026-11-30", "energia-renovavel-e-emissoes-de-co2-por-pessoa-brasil-emite-menos-do-que-o-esperado-banco-mundial-2026",
     f"Renováveis e emissões: o Brasil emite {n1(abs(res['BRA']))} t por pessoa {'a menos' if res['BRA'] < 0 else 'a mais'} do que o esperado, em {len(pe)} países",
     f"A correlação entre parcela de renováveis e CO2 por pessoa é de {r2(r)}. {len(quase)} países têm mais da metade de renováveis e emissões acima de 5 t por pessoa.",
     f"Mais renováveis costuma significar menos CO2 por pessoa. O Brasil usa {pct(BR['renov'])} de renováveis e emite {n1(BR['co2pc'])} t por pessoa.",
     f"Análise da Watermouse Media com dados do Banco Mundial: parcela de energia renovável e emissões de CO2 por pessoa em {len(pe)} países, com a posição do Brasil.",
     "graf-renovaveis-emissoes.jpg", "Gráfico de dispersão com parcela de energia renovável e emissões de CO2 por pessoa de 155 países, com o Brasil destacado em azul",
     "Gráfico: Watermouse Media, com dados do Banco Mundial (consumo de energia renovável, % do consumo final, e emissões de CO2 por pessoa).", body,
     attrib("indicadores de consumo de energia renovável (% do consumo final) e emissões de CO2 por habitante"))

print("ok", specs)
