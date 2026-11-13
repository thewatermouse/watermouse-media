D = {}
WB = "https://data.worldbank.org/indicator/"
D["brasil-gasta-97-por-cento-do-pib-em-saude-e-56-em-educacao-banco-mundial-2026"] = dict(
    why=["Os dois números da manchete medem coisas diferentes, e isso muda a leitura. O 9,7% da saúde é o gasto total, somando o público e o privado. O 5,6% da educação é só o gasto público. Por isso, não dá para dizer que o país prioriza a saúde em relação à educação com base nessa comparação direta.",
         "Posição em ranking de porcentagem do PIB também mistura situações bem distintas. Países pobres podem aparecer no topo por terem uma economia pequena e muito dinheiro de ajuda externa, como mostram o Afeganistão e a Libéria em gasto com saúde. O indicador mais próximo de qualidade é o gasto por pessoa e os resultados, que não entram nesta análise.",
         "Ainda assim, o dado ajuda a situar o Brasil: em saúde, entre os maiores da América Latina, e em educação, acima de países ricos como Estados Unidos, França e Alemanha em fatia do PIB."],
    numeros=["25º entre 156 países em saúde: cerca de 16% do topo da lista (25 ÷ 156). Em educação, 24º entre 158: cerca de 15% do topo.",
             "Estados Unidos, com 16,7% do PIB em saúde, gastam cerca de 1,7 vez a fatia do Brasil (16,7 ÷ 9,7 ≈ 1,72, conta nossa).",
             "Em educação, o Brasil (5,6%) fica 0,3 ponto percentual acima dos Estados Unidos (5,4%) e 0,3 abaixo do Reino Unido (5,9%)."],
    faq=[("As duas medidas são comparáveis?", "Não diretamente: saúde é gasto total (público e privado) e educação é só gasto público."),
         ("Gastar mais significa gastar melhor?", "Não. A porcentagem do PIB mede quanto se gasta, não a qualidade nem o valor por pessoa."),
         ("De onde vêm os dados?", "Do Banco Mundial, nos indicadores de gasto em saúde e de gasto público em educação como porcentagem do PIB.")],
    leia=[("Banco Mundial: gasto atual com saúde (% do PIB)", WB + "SH.XPD.CHEX.GD.ZS"),
          ("Banco Mundial: gasto do governo com educação (% do PIB)", WB + "SE.XPD.TOTL.GD.ZS")])
D["43-paises-menos-da-metade-usa-internet-banco-mundial-2026"] = dict(
    why=["Dados de 'uso de internet' medem a parcela da população que usa, e não a que tem acesso ou o preço da conexão. Um país pode ter cobertura de rede e baixo uso por causa de custo de planos e aparelhos, de energia elétrica instável, de idioma ou de alfabetização. A base não separa essas causas.",
         "Por isso, o número mais útil para ler é a concentração: a maior parte dos países com baixo uso está na África Subsaariana, e alguns dos mais populosos, como Nigéria, Etiópia e República Democrática do Congo, estão no meio do caminho. É neles que a expansão da conexão mais altera o total mundial.",
         "A comparação com o Brasil serve de escala: o uso brasileiro é mais de 12 vezes o do Sudão do Sul, o que mostra a distância entre os extremos."],
    numeros=["43 de 159 países são cerca de 27% da amostra (43 ÷ 159 ≈ 0,27, conta nossa).",
             "34 dos 43 países ficam na África Subsaariana: cerca de 79% do grupo (34 ÷ 43).",
             "1,41 bilhão de pessoas em países com baixo uso equivalem a cerca de 17% de 8,15 bilhões, o total dos 159 países citado em nossa análise de fecundidade (conta nossa).",
             "Nigéria: 41% de 238 milhões de habitantes dá algo como 98 milhões de usuários (238 × 0,41 ≈ 97,6 milhões, conta nossa).",
             "84,5% ÷ 7% ≈ 12,1: o Brasil tem mais de 12 vezes o uso do Sudão do Sul."],
    faq=[("De onde vêm os dados?", "Do Banco Mundial, indicador de indivíduos que usam a internet, em porcentagem da população."),
         ("A média mundial de 72,3% é do Banco Mundial?", "Não: é uma média ponderada pela população dos 159 países da amostra, calculada por nós."),
         ("Por que alguns países têm uso baixo?", "A base não explica as causas. Custo, infraestrutura e outros fatores podem pesar, mas isso não está nos dados.")],
    leia=[("Banco Mundial: indivíduos que usam a internet (% da população)", WB + "IT.NET.USER.ZS")])
D["30-paises-tem-mais-de-20-por-cento-de-idosos-brasil-banco-mundial-2026"] = dict(
    why=["O envelhecimento é uma pressão sobre previdência, saúde e mercado de trabalho, mas o ritmo varia muito. O Brasil, com 11,5% de população de 65 anos ou mais, está em faixa intermediária, mas a parcela cresce a cada ano, e o que o torna relevante é a velocidade: países como o Japão chegaram aos 30% depois de décadas de envelhecimento.",
         "O ranking também mostra efeitos de composição: no Golfo, as proporções baixas de idosos refletem muitos trabalhadores estrangeiros jovens, e não só fecundidade alta. Quem lê o número sem esse contexto pode tirar conclusões erradas sobre o país.",
         "A idade de 65 anos é um corte convencional. Países com expectativa de vida diferente têm 'idosos' em situações bem distintas, e o indicador não mede dependência ou saúde."],
    numeros=["30 de 159 países com mais de 20% de idosos: cerca de 19% da amostra (30 ÷ 159). Já 63 países, cerca de 40%, têm menos de 5%.",
             "Japão (30,0%) tem cerca de 2,6 vezes a parcela do Brasil (11,5%): 30 ÷ 11,5 ≈ 2,6 (conta nossa).",
             "O Brasil fica cerca de 1,1 ponto percentual acima da média mundial ponderada de 10,4% (conta nossa, 11,5 − 10,4)."],
    faq=[("De onde vêm os dados?", "Do Banco Mundial, indicador de população com 65 anos ou mais, em porcentagem do total, com dados para 2025 na matéria."),
         ("Por que a matéria cita expectativa de vida?", "Porque ela se liga ao envelhecimento: o ranking de expectativa de vida do portal complementa esta leitura."),
         ("O Brasil envelhece mais devagar que o Japão?", "Hoje tem uma parcela bem menor, mas a matéria diz que ela aumenta a cada ano.")],
    leia=[("Banco Mundial: população com 65 anos ou mais (% do total)", WB + "SP.POP.65UP.TO.ZS")])
D["57-paises-tem-menos-filhos-por-mulher-que-o-brasil-banco-mundial-2026"] = dict(
    why=["A taxa de fecundidade abaixo do nível de reposição, cerca de 2,1 filhos por mulher, não significa que a população cai imediatamente: há inércia demográfica, e migração e longevidade também pesam. O que a taxa indica é a tendência de longo prazo, e o Brasil, com 1,61, está em um grupo grande, não isolado.",
         "O mundo está dividido quase ao meio pela linha da reposição: 80 países abaixo e 79 acima. Mas os dois lados têm perfis muito diferentes, de Coreia do Sul, com menos de um filho por mulher, a Nigéria, com mais de quatro.",
         "A matéria avisa que a taxa mede o comportamento de um ano e não é previsão. Fecundidade pode subir ou cair com políticas, economia e mudanças culturais."],
    numeros=["57 de 159 países estão abaixo do Brasil: cerca de 36% (57 ÷ 159). Eles reúnem 2,7 bilhões de pessoas, cerca de 33% dos 8,15 bilhões (2,7 ÷ 8,15, conta nossa).",
             "1,61 está cerca de 23% abaixo da reposição de 2,1 (1 − 1,61 ÷ 2,1 ≈ 0,23, conta nossa).",
             "A Coreia do Sul (0,75) tem menos da metade da taxa brasileira (0,75 ÷ 1,61 ≈ 0,47), e a Nigéria (4,38) tem cerca de 2,7 vezes (4,38 ÷ 1,61).",
             "80 abaixo de 2,1 mais 79 acima somam os 159 países."],
    faq=[("O que é nível de reposição?", "Cerca de 2,1 filhos por mulher, taxa em que cada geração se substitui, sem considerar migração."),
         ("A população do Brasil vai diminuir?", "A matéria diz que, sem migração, a tendência é parar de crescer e envelhecer mais rápido, mas ressalta que o número não é uma previsão."),
         ("De onde vêm os dados?", "Do Banco Mundial, indicador de taxa de fecundidade total (nascimentos por mulher).")],
    leia=[("Banco Mundial: taxa de fecundidade total", WB + "SP.DYN.TFRT.IN")])
