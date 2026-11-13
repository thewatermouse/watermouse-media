# -*- coding: utf-8 -*-
"""Segunda leva de analises de dados proprias (Banco Mundial): mortalidade infantil x renda, indice de miseria,
envelhecimento x gasto em saude, floresta nos paises grandes. Reusa os helpers de analises_dados.py.
Uso: python -I tools/analises_dados2.py"""
import pathlib, sys
SRC = (pathlib.Path(__file__).resolve().parent / "analises_dados.py").read_text(encoding="utf-8")
exec(compile(SRC.split("# ---------- 1. Renda e vida longa ----------")[0], "analises_dados_helpers", "exec"))
import numpy as np

med = lambda L, k: float(np.median([p[k] for p in L]))

# ---------- A. Mortalidade infantil x renda ----------
pool, a, b, r, res = regress("pibpc", "mort", logx=True)
pr = sorted(pool, key=lambda p: res[p["iso3"]])  # menor residuo = melhor que o esperado
big = [p for p in pr if p["pop"] >= 5e6]
melhor, pior = big[:3], big[::-1][:3]
rk_m, nm = rank("mort", BR, rev=False, pool=pool)  # 1 = menor mortalidade
hiA = ["Brasil"] + [p["nome"] for p in melhor] + [p["nome"] for p in pior]
scatter("graf-mortalidade-renda.jpg", [p["pibpc"] for p in pool], [p["mort"] for p in pool], [p["nome"] for p in pool], hiA,
        "Renda protege crianças, mas o caminho varia", "PIB por pessoa (escala logarítmica) e mortalidade infantil (antes de 1 ano) por mil nascidos vivos",
        "PIB por pessoa, US$ (escala logarítmica)", "Mortes de bebês antes de 1 ano por mil nascidos vivos", logx=True, xfmt=lambda v, _: n0(v), off={"Brasil": (10, 10)})
fm = lambda p: f"{p['nome']} ({n1(p['mort'])} por mil, {n1(abs(res[p['iso3']]))} {'abaixo' if res[p['iso3']] < 0 else 'acima'} do previsto)"
body = f"""<p>Entre os indicadores de um país, poucos se relacionam tão bem com a renda quanto a mortalidade de bebês. Cruzamos o PIB por pessoa e a mortalidade infantil (mortes antes de completar 1 ano) de {len(pool)} países com 1 milhão de habitantes ou mais, pelos dados do Banco Mundial. A correlação, entre o logaritmo da renda e a mortalidade, é de {r2(r)}: negativa e forte. Quanto mais rico o país, menos bebês morrem antes de completar 1 ano.</p>

      <!--AD1-->

      <h2>A regra e o Brasil</h2>

      <p>A reta de tendência indica que, a cada vez que a renda por pessoa dobra, a mortalidade infantil cai cerca de {n1(abs(a * np.log(2)))} mortes por mil nascidos vivos, em média. O Brasil registra {n1(BR['mort'])} mortes por mil, o {rk_m}º menor valor entre {nm} países. Para a renda de {usd(BR['pibpc'])} por pessoa, a reta prevê {n1(a * np.log(BR['pibpc']) + b)}, o que deixa o Brasil {n1(abs(res['BRA']))} ponto{'' if round(abs(res['BRA']), 1) == 1 else 's'} {'abaixo' if res['BRA'] < 0 else 'acima'} do esperado.</p>

      <h2>Quem faz mais do que a renda sugere</h2>

      <p>Entre os países com 5 milhões de habitantes ou mais, os que ficam mais abaixo da reta, ou seja, com menos mortes do que a renda indicaria, são {lst(fm(q) for q in melhor)}. Os que ficam mais acima são {lst(fm(q) for q in pior)}.</p>

      <h2>O que o cálculo não diz</h2>

      <p>A renda média não é a causa direta: o que salva bebês são vacinação, saneamento, acesso a pré-natal e parto seguro e nutrição, e esses fatores dependem de políticas públicas e de como a renda se distribui. Países com o mesmo PIB por pessoa podem ter resultados muito diferentes, como mostram os extremos acima. Os dados de mortalidade vêm de estimativas do Grupo Inter-agências da ONU para Estimação da Mortalidade Infantil (UN IGME), e a precisão é menor em países com poucos registros de nascimento.</p>

      {CTX.format(t="A mortalidade infantil mede quantos bebês, em cada mil nascidos vivos, morrem antes de completar 1 ano. É um dos indicadores mais usados para comparar a saúde de países. O PIB por pessoa é em dólares correntes e entra em escala logarítmica no cálculo.")}"""
spec("2026-11-22", "mortalidade-infantil-e-renda-onde-o-brasil-fica-em-relacao-ao-previsto-banco-mundial-2026",
     f"Mortalidade infantil e renda: o Brasil fica {n1(abs(res['BRA']))} ponto{'' if round(abs(res['BRA']), 1) == 1 else 's'} {'abaixo' if res['BRA'] < 0 else 'acima'} do previsto entre {len(pool)} países",
     f"A correlação entre renda e mortalidade infantil é de {r2(r)}. O Brasil tem {n1(BR['mort'])} mortes por mil e é o {rk_m}º menor valor entre {nm} países; {melhor[0]['nome']} e {pior[0]['nome']} estão nos extremos entre os países maiores.",
     f"Cruzamos renda e mortalidade infantil em {len(pool)} países: o Brasil tem {n1(BR['mort'])} mortes por mil nascidos vivos.",
     f"Análise da Watermouse Media com dados do Banco Mundial: PIB por pessoa e mortalidade infantil em {len(pool)} países, com a posição do Brasil.",
     "graf-mortalidade-renda.jpg", "Gráfico de dispersão com PIB por pessoa em escala logarítmica e mortalidade infantil de 157 países, com o Brasil destacado em azul",
     "Gráfico: Watermouse Media, com dados do Banco Mundial (PIB por pessoa e mortalidade infantil, valor mais recente).", body,
     attrib("indicadores de PIB per capita (US$ correntes) e taxa de mortalidade infantil (por mil nascidos vivos)"))

# ---------- B. Indice de miseria ----------
pm = have("inflacao", "desemp")
for p in pm:
    p["_mis"] = p["inflacao"] + p["desemp"]
pm_s = sorted(pm, key=lambda p: p["_mis"], reverse=True)
rk_mis = [p["iso3"] for p in pm_s].index("BRA") + 1
rinf = float(np.corrcoef([p["inflacao"] for p in pm], [p["desemp"] for p in pm])[0, 1])
top = pm_s[:8]
bars_items = [(p["nome"], p["_mis"]) for p in pm_s[:11]]
if "Brasil" not in [i[0] for i in bars_items]:
    bars_items = bars_items[:11] + [("Brasil", BR["inflacao"] + BR["desemp"])]
bars("graf-indice-miseria.jpg", bars_items, [p["nome"] for p in pm_s[:3]],
     "O índice de miséria: inflação mais desemprego", "Inflação anual somada à taxa de desemprego (pontos percentuais), os 11 países mais altos e o Brasil", unit=" pp",
     fonte="Fonte: Banco Mundial (WDI), valor mais recente de cada país. Países com 1 milhão de habitantes ou mais. Cálculo da Watermouse Media")
low = pm_s[::-1][:3]
body = f"""<p>O índice de miséria é uma conta simples, criada pelo economista Arthur Okun nos anos 1960: soma-se a inflação anual à taxa de desemprego. Quanto maior o número, pior a situação do bolso do cidadão. Calculamos o índice para {len(pm)} países com 1 milhão de habitantes ou mais, com dados do Banco Mundial, e o resultado traz uma surpresa: inflação e desemprego quase não andam juntos entre países, com correlação de {r2(rinf)}.</p>

      <!--AD1-->

      <h2>O Brasil no ranking</h2>

      <p>O Brasil tem inflação de {pct(BR['inflacao'])} ao ano e desemprego de {pct(BR['desemp'])}, o que dá um índice de {n1(BR['inflacao'] + BR['desemp'])} pontos. É o {rk_mis}º mais alto entre {len(pm)} países, ou seja, fica {'na metade mais baixa' if rk_mis > len(pm) / 2 else 'na metade mais alta'} do ranking. A mediana mundial é de {n1(float(np.median([p['_mis'] for p in pm])))} pontos.</p>

      <h2>Quem lidera o índice</h2>

      <p>Os países com os maiores índices são {lst(f"{p['nome']} ({n1(p['_mis'])}: inflação de {pct(p['inflacao'])} e desemprego de {pct(p['desemp'])})" for p in top[:3])}. Nessas listas, a inflação alta costuma pesar mais do que o desemprego, porque as variações de preços podem passar de 100% ao ano, enquanto o desemprego raramente supera 35%.</p>

      <h2>Quem fica no fim da lista</h2>

      <p>Os menores valores são os de {lst(f"{p['nome']} ({n1(p['_mis'])})" for p in low)}. Um índice baixo pode esconder situações bem diferentes: economias com muito emprego formal, ou países onde o desemprego medido é baixo porque quase todos trabalham na informalidade por falta de alternativa.</p>

      <h2>Limites da conta</h2>

      <p>O índice trata um ponto de inflação e um ponto de desemprego como se pesassem igual, o que é uma simplificação. A inflação de um ano isolado oscila bastante, e o desemprego depende da metodologia de cada país. Use o número como um retrato do ano de referência, não como diagnóstico da economia.</p>

      {CTX.format(t="O índice de miséria foi proposto por Arthur Okun, conselheiro econômico do presidente Lyndon Johnson, como medida rápida do desconforto econômico. A inflação é a variação anual do índice de preços ao consumidor, e o desemprego é a estimativa da Organização Internacional do Trabalho para a parcela da força de trabalho sem emprego.")}"""
spec("2026-11-23", "indice-de-miseria-inflacao-mais-desemprego-brasil-ocupa-posicao-banco-mundial-2026",
     f"Índice de miséria: o Brasil é o {rk_mis}º entre {len(pm)} países ao somar inflação e desemprego",
     f"Somando inflação anual e taxa de desemprego, o Brasil chega a {n1(BR['inflacao'] + BR['desemp'])} pontos. O dado curioso: entre países, as duas variáveis têm correlação de apenas {r2(rinf)}.",
     f"Inflação mais desemprego dá {n1(BR['inflacao'] + BR['desemp'])} pontos para o Brasil, o {rk_mis}º lugar entre {len(pm)} países.",
     f"Análise da Watermouse Media com dados do Banco Mundial: índice de miséria (inflação mais desemprego) de {len(pm)} países, com a posição do Brasil.",
     "graf-indice-miseria.jpg", "Gráfico de barras horizontais com o índice de miséria (inflação mais desemprego) dos países mais altos e do Brasil em azul",
     "Gráfico: Watermouse Media, com dados do Banco Mundial (inflação anual e taxa de desemprego, valor mais recente).", body,
     attrib("indicadores de inflação (índice de preços ao consumidor, variação anual) e desemprego total (% da força de trabalho)"))

# ---------- C. Envelhecimento x gasto em saude ----------
pc = have("idosos", "saude")
pool, a, b, r, res = regress("idosos", "saude")
rk_id, nid = rank("idosos", BR, pool=pc)
jap = next((p for p in pc if p["iso3"] == "JPN"), None)
usa = next(p for p in pc if p["iso3"] == "USA")
mais_idosos = sorted(pc, key=lambda p: p["idosos"], reverse=True)[:5]
hiC = ["Brasil", "Estados Unidos"] + [p["nome"] for p in mais_idosos[:3]]
scatter("graf-idosos-saude.jpg", [p["idosos"] for p in pc], [p["saude"] for p in pc], [p["nome"] for p in pc], hiC,
        "Países mais velhos gastam mais com saúde", "Parcela de idosos (65 anos ou mais, %) e gasto total com saúde (% do PIB), 156 países",
        "População com 65 anos ou mais, %", "Gasto total com saúde, % do PIB", off={"Brasil": (10, -22), "Estados Unidos": (-110, -22)})
dobra = 5.0
body = f"""<p>Populações mais velhas precisam de mais cuidados de saúde, e o gasto dos países reflete isso. Cruzamos a parcela de pessoas com 65 anos ou mais e o gasto total com saúde, em porcentagem do PIB, de {len(pc)} países, com dados do Banco Mundial. A correlação é de {r2(r)}, positiva e moderada: países com mais idosos tendem a gastar uma fatia maior da economia com saúde.</p>

      <!--AD1-->

      <h2>A regra: cada ponto de idosos vale quanto de PIB</h2>

      <p>A reta de tendência indica que, a cada 1 ponto percentual a mais de idosos na população, o gasto com saúde sobe cerca de {n1(a)} ponto percentual do PIB, em média. Com {n1(dobra)} pontos percentuais a mais de idosos, o gasto sobe cerca de {n1(a * dobra)} ponto do PIB.</p>

      <h2>O Brasil: jovem para o gasto que tem</h2>

      <p>O Brasil tem {pct(BR['idosos'])} de população com 65 anos ou mais, o {rk_id}º lugar entre {nid} países, e gasta {pct(BR['saude'])} do PIB com saúde. Para a parcela de idosos que tem, a reta prevê um gasto de {n1(a * BR['idosos'] + b)}% do PIB, então o Brasil gasta {n1(abs(res['BRA']))} ponto{'' if round(abs(res['BRA']), 1) == 1 else 's'} {'acima' if res['BRA'] > 0 else 'abaixo'} do esperado só pela idade da população.</p>

      <h2>Os mais velhos e o caso dos Estados Unidos</h2>

      <p>Os países com mais idosos na amostra são {lst(f"{p['nome']} ({pct(p['idosos'])} com 65 anos ou mais, gasto de {pct(p['saude'])} do PIB)" for p in mais_idosos[:3])}. Os Estados Unidos, com {pct(usa['idosos'])} de idosos, gastam {pct(usa['saude'])} do PIB, mais do que a reta prevê ({n1(a * usa['idosos'] + b)}%): a idade da população não explica sozinha o gasto americano.</p>

      <h2>O que o cálculo não faz</h2>

      <p>Associação não é causa, e o gasto em porcentagem do PIB mistura recursos públicos, privados e de ajuda externa. Países com muitos idosos também são, em geral, países de renda alta, e a renda explica parte do gasto. Este cálculo não separa os dois efeitos.</p>

      {CTX.format(t="A parcela de população com 65 anos ou mais vem das projeções populacionais da ONU, e o gasto corrente com saúde é o indicador da Organização Mundial da Saúde, repassado pelo Banco Mundial. Ambos usam o ano mais recente disponível de cada país.")}"""
spec("2026-11-24", "populacao-idosa-e-gasto-com-saude-brasil-gasta-o-esperado-pela-idade-banco-mundial-2026",
     f"População idosa e gasto com saúde: o Brasil gasta {n1(abs(res['BRA']))} ponto{'' if round(abs(res['BRA']), 1) == 1 else 's'} do PIB {'a mais' if res['BRA'] > 0 else 'a menos'} do que a idade da população sugere",
     f"A correlação entre a parcela de idosos e o gasto com saúde é de {r2(r)} em {len(pc)} países. O Brasil tem {pct(BR['idosos'])} de idosos e gasta {pct(BR['saude'])} do PIB.",
     f"Países com mais idosos gastam mais com saúde, mas a regra tem exceções. O Brasil tem {pct(BR['idosos'])} de idosos e gasta {pct(BR['saude'])} do PIB.",
     f"Análise da Watermouse Media com dados do Banco Mundial: parcela de idosos e gasto com saúde em {len(pc)} países, com Brasil e Estados Unidos em destaque.",
     "graf-idosos-saude.jpg", "Gráfico de dispersão com a parcela de idosos e o gasto com saúde em porcentagem do PIB de 156 países, com o Brasil em azul",
     "Gráfico: Watermouse Media, com dados do Banco Mundial (população com 65 anos ou mais e gasto total com saúde, valor mais recente).", body,
     attrib("indicadores de população com 65 anos ou mais (% do total) e gasto corrente com saúde (% do PIB)"))

# ---------- D. Floresta nos paises grandes ----------
pf = [p for p in have("mata", "area") if p["area"] >= 1e6]
pf_s = sorted(pf, key=lambda p: p["mata"], reverse=True)
rkf = [p["iso3"] for p in pf_s].index("BRA") + 1
bars("graf-floresta-paises-grandes.jpg", [(p["nome"], p["mata"]) for p in pf_s[:14]], ["Brasil"],
     "Quanto do território é floresta nos países gigantes", "Área de floresta em % do território, países com mais de 1 milhão de km²", unit="%",
     fonte="Fonte: Banco Mundial (WDI), área florestal, valor mais recente de cada país. Países com 1 milhão de km² ou mais. Watermouse Media")
rich = [p for p in pf if p["pibpc"] >= 20000]
abs_for = lambda p: p["mata"] / 100 * p["area"]
maior_flor = sorted(pf, key=abs_for, reverse=True)[:4]
body = f"""<p>Floresta é riqueza natural, mas não é incompatível com renda alta, e os dados do Banco Mundial mostram isso. Olhamos os {len(pf)} países com mais de 1 milhão de quilômetros quadrados de território e quanto de cada um é coberto por floresta. O Brasil, com {pct(BR['mata'])} do território coberto, ocupa o {rkf}º lugar entre eles.</p>

      <!--AD1-->

      <h2>O Brasil entre os gigantes</h2>

      <p>Entre os países gigantes, os de maior proporção de floresta são {lst(f"{p['nome']} ({pct(p['mata'])})" for p in pf_s[:3])}. O Brasil fica atrás de {', '.join(p['nome'] for p in pf_s[:rkf - 1]) if rkf > 1 else 'nenhum deles'}, e à frente de países como {lst(p['nome'] for p in pf_s[rkf:rkf + 3])}.</p>

      <h2>Em tamanho absoluto</h2>

      <p>Em quilômetros quadrados de floresta, os maiores são {lst(f"{p['nome']} (cerca de {n0(abs_for(p) / 1000)} mil km²)" for p in maior_flor)}. A proporção mede quanto do país é floresta; o tamanho absoluto mostra o peso da floresta para o planeta. Os dois rankings contam histórias diferentes.</p>

      <h2>Renda e floresta</h2>

      <p>Entre os {len(pf)} países gigantes, {len(rich)} têm PIB por pessoa acima de US$ 20.000. A correlação entre renda e cobertura florestal em todos os países com dado é de apenas {r2(float(np.corrcoef(np.log([p['pibpc'] for p in have('mata', 'pibpc')]), [p['mata'] for p in have('mata', 'pibpc')])[0, 1]))}, praticamente nula: país rico não é sinônimo de país sem floresta, nem país pobre de país florestado.</p>

      <h2>O que a medida inclui</h2>

      <p>A área florestal do Banco Mundial vem da FAO e considera terra com árvores de pelo menos 5 metros de altura e cobertura mínima de 10% do solo, o que inclui florestas plantadas. O indicador mede cobertura, não qualidade: uma floresta nativa preservada e uma plantação de eucalipto contam do mesmo jeito.</p>

      {CTX.format(t="A Organização das Nações Unidas para a Alimentação e a Agricultura (FAO) faz a avaliação global dos recursos florestais e é a fonte do indicador. O território de cada país inclui áreas de águas interiores, e o ano de referência pode variar de um país para outro.")}"""
spec("2026-11-25", "floresta-nos-paises-gigantes-brasil-fica-em-posicao-entre-os-maiores-territorios-banco-mundial-2026",
     f"Floresta nos países gigantes: o Brasil, com {pct(BR['mata'])} do território, é o {rkf}º entre {len(pf)} países de mais de 1 milhão de km²",
     f"O Brasil tem {pct(BR['mata'])} do território coberto por floresta, o {rkf}º lugar entre os {len(pf)} países gigantes. Renda e floresta quase não se relacionam entre países.",
     f"Entre os {len(pf)} países com mais de 1 milhão de km², o Brasil é o {rkf}º em proporção de floresta, com {pct(BR['mata'])}.",
     f"Análise da Watermouse Media com dados do Banco Mundial: proporção de floresta nos {len(pf)} países com mais de 1 milhão de km², com a posição do Brasil.",
     "graf-floresta-paises-grandes.jpg", "Gráfico de barras horizontais com a proporção de floresta nos países de mais de 1 milhão de km², com o Brasil em azul",
     "Gráfico: Watermouse Media, com dados do Banco Mundial (área florestal, % do território, valor mais recente).", body,
     attrib("indicadores de área florestal (% do território), área do país e PIB per capita"))

print("ok", specs)
