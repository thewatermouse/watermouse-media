# -*- coding: utf-8 -*-
"""Contexto e glossario por materia (conteudo editorial proprio, so fatos bem estabelecidos).

Cada entrada: slug -> (contexto_html, [(termo, definicao), ...]). Usado por tools/enrich.py."""

E = {}

E["artemis-i-cristais-radiacao-lua-2026"] = (
 "<p>A Artemis I foi o primeiro voo de teste do programa Artemis, da NASA, que busca levar pessoas de volta à superfície da Lua. A missão, sem tripulação, decolou em novembro de 2022 e terminou em dezembro do mesmo ano, com a cápsula Orion testando sistemas e o escudo térmico na volta à Terra. Os manequins instrumentados a bordo serviram para estimar o que uma tripulação receberia de radiação numa viagem assim.</p>"
 "<p>Medir essa radiação importa porque, fora da proteção do campo magnético da Terra, o corpo humano fica mais exposto a partículas de alta energia vindas do espaço profundo e do Sol. É um dos limites mais discutidos para missões longas, e qualquer método novo e barato de medir doses ajuda a planejar a proteção das próximas tripulações.</p>",
 [("Radiação cósmica galáctica", "Partículas de alta energia que chegam de fora do Sistema Solar, em todas as direções, e são difíceis de bloquear."),
  ("Cinturões de Van Allen", "Regiões em volta da Terra onde partículas carregadas ficam presas pelo campo magnético. Não existem em volta da Lua."),
  ("Detector passivo", "Dispositivo que guarda o registro da radiação sem precisar de energia elétrica, para ser lido depois no laboratório.")])

E["supernovas-energia-escura-catalogo-2026"] = (
 "<p>A expansão acelerada do Universo foi descoberta em 1998, a partir da observação de supernovas distantes, e rendeu o Nobel de Física de 2011 a Saul Perlmutter, Brian Schmidt e Adam Riess. O nome dado à causa desconhecida dessa aceleração é energia escura. No modelo padrão da cosmologia, ela se comporta como uma constante, com o mesmo valor em qualquer época, e responde por cerca de dois terços do conteúdo de energia do cosmos.</p>"
 "<p>Por isso um resultado que sugira que a energia escura muda com o tempo é tão acompanhado: se for confirmado, o modelo padrão precisará de ajustes. Ao mesmo tempo, esse tipo de indício costuma ficar perto do limite estatístico e depende de como diferentes levantamentos de dados são combinados, o que explica a cautela dos próprios pesquisadores.</p>",
 [("Supernova tipo Ia", "Explosão de uma estrela anã branca cujo brilho é bem conhecido, o que permite usá-la como \"vela padrão\" para medir distâncias."),
  ("Constante cosmológica", "Termo que representa uma energia de valor fixo no espaço, a explicação mais simples para a aceleração do Universo."),
  ("Energia escura", "Nome dado à causa ainda desconhecida da expansão acelerada. Não se sabe do que ela é feita.")])

E["chernobil-particulas-radioativas-estaveis-2026"] = (
 "<p>O acidente de Chernobil, na Ucrânia, aconteceu em 26 de abril de 1986, quando o reator 4 da usina explodiu e liberou material radioativo que se espalhou por boa parte da Europa. Em volta da usina foi criada uma zona de exclusão, que continua restrita até hoje, e uma grande estrutura de contenção cobre os restos do reator.</p>"
 "<p>Entender como o material liberado se comporta décadas depois ajuda a prever por quanto tempo o solo e a água podem carregar contaminação. Isso vale também para decisões sobre onde é seguro viver e produzir alimentos, e para o planejamento de limpezas em outros locais com histórico de contaminação nuclear.</p>",
 [("Meia-vida", "Tempo para que metade dos átomos de um elemento radioativo se transforme. O césio-137, por exemplo, tem meia-vida de cerca de 30 anos."),
  ("Partícula quente", "Fragmento microscópico de combustível ou de material do reator que concentra radioatividade e fica no solo."),
  ("Zona de exclusão", "Área ao redor da usina com acesso e ocupação restritos por causa da contaminação.")])

E["geleiras-suicas-perda-gelo-2026"] = (
 "<p>As geleiras dos Alpes funcionam como reservatórios naturais: guardam água no inverno e a liberam aos poucos no verão, alimentando rios importantes da Europa, como o Reno e o Ródano. Quando elas encolhem, muda a quantidade e o momento em que essa água chega, o que afeta agricultura, geração de energia e abastecimento.</p>"
 "<p>O balanço de massa de uma geleira, ou seja, a diferença entre o gelo que ela ganha em neve e o que perde por derretimento, é medido todos os anos por redes de monitoramento. Para o Brasil, que não tem geleiras, o tema importa por outro motivo: o gelo que derrete nas montanhas e nos polos contribui para a elevação do nível do mar, que afeta cidades costeiras.</p>",
 [("Balanço de massa", "Diferença entre o gelo acumulado (neve) e o gelo perdido (derretimento) por uma geleira em um período."),
  ("Albedo", "Fração da luz solar que uma superfície reflete. Gelo e neve refletem muito, e a perda deles faz a região absorver mais calor."),
  ("Elevação do nível do mar", "Aumento do nível médio dos oceanos, causado pelo derretimento de gelo em terra e pela expansão da água quando esquenta.")])

E["kikai-supervulcao-magma-2026"] = (
 "<p>A caldeira de Kikai fica no sul do Japão, ao largo da ilha de Kyushu, e guarda a marca de uma das maiores erupções dos últimos 10 mil anos, ocorrida há cerca de 7.300 anos. Essa erupção lançou uma enorme quantidade de cinzas sobre a região e é associada a impactos nas comunidades que viviam no sul do arquipélago naquela época.</p>"
 "<p>\"Supervulcão\" é uma expressão popular, não um termo técnico rígido, usada para vulcões capazes de erupções gigantescas. Monitorar se o magma volta a se acumular sob uma caldeira não significa que uma erupção esteja próxima: processos assim podem levar milhares de anos, e o interesse da ciência é entender como o sistema funciona e quais sinais merecem vigilância.</p>",
 [("Caldeira", "Grande depressão formada quando o teto de uma câmara de magma desaba depois de uma erupção volumosa."),
  ("Magma", "Rocha derretida no interior da Terra. Ao chegar à superfície, passa a se chamar lava."),
  ("Índice de Explosividade Vulcânica (VEI)", "Escala de 0 a 8 que mede o tamanho de uma erupção, principalmente pelo volume de material expelido.")])

E["quenia-pequeno-comercio-cidadaos-2026"] = (
 "<p>Reservar o pequeno comércio para cidadãos do próprio país é uma ideia que reaparece em várias economias africanas. Em Gana, por exemplo, a lei de promoção de investimentos reserva o comércio varejista de pequena escala a ganenses, e o debate sobre a aplicação dessa regra a comerciantes estrangeiros é antigo e costuma gerar tensão política.</p>"
 "<p>O pano de fundo é o peso da economia informal: em grande parte da África Subsaariana, a maioria das pessoas trabalha por conta própria, em pequenos negócios. Isso faz da concorrência de estrangeiros um tema sensível, ao mesmo tempo em que o continente tenta integrar seus mercados por meio da Área de Livre Comércio Continental Africana (AfCFTA), em vigor desde 2021, o que cria uma tensão entre proteger o negócio local e abrir o mercado.</p>",
 [("Economia informal", "Atividades econômicas fora do registro formal, como pequenos comércios e serviços por conta própria."),
  ("AfCFTA", "Área de Livre Comércio Continental Africana, acordo para reduzir barreiras ao comércio entre os países da África."),
  ("Setor reservado", "Atividade que a lei limita a cidadãos do país, impedindo a entrada de estrangeiros.")])

E["mocambique-trabalho-domestico-regime-2026"] = (
 "<p>O trabalho doméstico é uma das ocupações mais numerosas e menos protegidas do mundo, e em muitos países ainda fica fora da legislação trabalhista comum. Em 2011, a Organização Internacional do Trabalho (OIT) aprovou a Convenção 189, que pede direitos básicos a essas trabalhadoras e trabalhadores, como jornada definida, descanso semanal e remuneração mínima.</p>"
 "<p>O Brasil passou por um processo parecido: a Emenda Constitucional 72, de 2013, e a Lei Complementar 150, de 2015, ampliaram os direitos do trabalho doméstico, com contrato formal, jornada e FGTS. Por isso a experiência de outros países de língua portuguesa na formalização desse trabalho é relevante para quem acompanha o tema aqui.</p>",
 [("Regime do trabalho doméstico", "Conjunto de regras que define contrato, jornada, salário e proteção social de quem trabalha em residências."),
  ("Convenção 189 da OIT", "Tratado internacional de 2011 sobre trabalho decente para trabalhadoras e trabalhadores domésticos."),
  ("Salário mínimo", "Menor remuneração que a lei permite pagar por um período de trabalho.")])

E["assinatura-mestre-canteiro-seljucida-van-2026"] = (
 "<p>Os seljúcidas foram uma dinastia de origem turca que dominou grandes partes do Oriente Médio e, a partir do fim do século XI, a Anatólia, no território da atual Turquia. Deixaram uma arquitetura marcante, com mesquitas, caravançarais e túmulos de pedra com decoração geométrica e inscrições em árabe.</p>"
 "<p>Saber quem construía esses monumentos é difícil, porque muitas obras medievais não foram assinadas e os registros sobre artesãos são escassos. Quando uma inscrição traz o nome do mestre e uma data, ela permite ligar uma pessoa a uma obra e a um momento, o que ajuda historiadores a reconstruir como funcionavam as oficinas de pedra e como técnicas e estilos circulavam pela região.</p>",
 [("Seljúcidas", "Dinastia turca medieval que governou partes do Oriente Médio e da Anatólia a partir do século XI."),
  ("Mestre canteiro", "Profissional que talha e dirige o trabalho em pedra em uma construção."),
  ("Epigrafia", "Estudo de inscrições gravadas em pedra, metal ou outros materiais duráveis.")])

E["aiib-benin-pipeline-infraestrutura-2026"] = (
 "<p>O Banco Asiático de Investimento em Infraestrutura (AIIB) foi criado em 2016 com sede em Pequim, a partir de uma iniciativa da China, e tem dezenas de países-membros de vários continentes, entre eles o Brasil. A proposta é financiar projetos de energia, transporte, água e telecomunicações, áreas em que as economias em desenvolvimento têm grande carência de investimento.</p>"
 "<p>A África é um dos continentes com maior déficit de infraestrutura, e vários financiadores disputam espaço ali, entre bancos multilaterais tradicionais, bancos de desenvolvimento nacionais e instituições novas. Um acordo plurianual, em vez de um empréstimo isolado, indica a intenção de acompanhar uma carteira de projetos por mais tempo com o mesmo país.</p>",
 [("Banco multilateral", "Instituição financeira controlada por vários países, que empresta para projetos de desenvolvimento."),
  ("Carteira de projetos (pipeline)", "Conjunto de projetos identificados e planejados para receber financiamento ao longo do tempo."),
  ("Déficit de infraestrutura", "Diferença entre a infraestrutura que um país tem e a que precisaria para sustentar seu desenvolvimento.")])

E["global-grids-accelerator-onu-2026"] = (
 "<p>Energia solar e eólica só chegam ao consumidor se houver rede para transportá-las, e em muitos países a expansão das linhas de transmissão e distribuição não acompanhou a das usinas renováveis. O resultado são filas de espera para conectar novos projetos e, em alguns casos, usinas obrigadas a reduzir a geração porque a rede não comporta tudo o que elas poderiam entregar.</p>"
 "<p>O Brasil conhece o problema de perto: nos últimos anos, parte da geração eólica e solar do Nordeste foi cortada por limites de transmissão, mesmo com a energia disponível. Por isso iniciativas que tentam acelerar a construção e a modernização de redes interessam a quem acompanha a transição energética, e não só a países ricos.</p>",
 [("Rede de transmissão", "Conjunto de linhas e equipamentos que leva a energia das usinas até as regiões de consumo."),
  ("Corte de geração (curtailment)", "Redução forçada da produção de uma usina porque a rede não consegue escoar a energia."),
  ("Fila de conexão", "Lista de projetos que aguardam autorização e capacidade para se ligar à rede.")])

E["bvr19-hidrogenio-solar-oregon-2026"] = (
 "<p>O hidrogênio é visto como um combustível e uma matéria-prima importante para descarbonizar setores difíceis de eletrificar, como a produção de aço, fertilizantes e o transporte pesado. O chamado hidrogênio verde é produzido separando a água em hidrogênio e oxigênio com eletricidade de fonte renovável, num processo chamado eletrólise.</p>"
 "<p>Hoje, os equipamentos que fazem isso dependem de metais caros, como platina e irídio, o que encarece o hidrogênio. Materiais que usem a luz do sol diretamente para quebrar a molécula de água, e que dispensem esses metais, são uma linha de pesquisa para baratear o processo. O Brasil, com muito sol, vento e água, tem uma estratégia nacional de hidrogênio e interesse em produzi-lo a custo competitivo.</p>",
 [("Eletrólise", "Uso de eletricidade para separar a água em hidrogênio e oxigênio."),
  ("Hidrogênio verde", "Hidrogênio produzido a partir de fontes renováveis, sem emitir gases de efeito estufa no processo."),
  ("Fotocatálise", "Uso de luz para acelerar uma reação química com ajuda de um material chamado catalisador.")])

E["escada-energia-quantica-caltech-2026"] = (
 "<p>Na física quântica, a energia de um sistema não varia de forma contínua: só pode assumir certos valores discretos, chamados níveis. Quando esses níveis se organizam em degraus igualmente espaçados, fala-se em uma \"escada\" de energia, um padrão previsto pela teoria para elétrons em condições específicas dentro de materiais.</p>"
 "<p>Observar diretamente fenômenos que a teoria prevê há décadas serve para testar se nossos modelos descrevem a natureza, e costuma abrir caminho para tecnologias, como novos sensores e dispositivos eletrônicos. Os experimentos desse tipo exigem controle muito fino do material, geralmente a temperaturas baixíssimas.</p>",
 [("Nível de energia", "Valor permitido de energia para uma partícula ou um sistema quântico."),
  ("Quantização", "Ideia de que certas grandezas, como a energia, só assumem valores específicos e não qualquer valor."),
  ("Elétron em rede cristalina", "Elétron que se move em um material onde os átomos formam um padrão regular e repetido.")])

E["oficina-cobre-neolitico-cayonu-2026"] = (
 "<p>O Neolítico é o período em que as sociedades humanas passaram da caça e coleta para a agricultura e a vida em assentamentos fixos, no Oriente Próximo, a partir de cerca de 12 mil anos atrás. O cobre foi um dos primeiros metais trabalhados pelas pessoas, inicialmente martelado e aquecido a partir de pedaços encontrados em estado nativo.</p>"
 "<p>A região do sudeste da Anatólia, onde fica a Turquia atual, é uma das mais importantes para entender essa transição, com sítios como Göbekli Tepe, Karahan Tepe e Çayönü. Achar um espaço dedicado à produção de objetos de cobre sugere organização do trabalho e especialização, e não apenas peças isoladas feitas por acaso.</p>",
 [("Neolítico", "Período da pré-história marcado pela agricultura, pela criação de animais e pelos primeiros povoados fixos."),
  ("Cobre nativo", "Cobre que aparece na natureza em estado metálico, sem precisar ser extraído de minério."),
  ("Especialização do trabalho", "Divisão de tarefas em que certas pessoas se dedicam a um ofício específico.")])

E["encelado-oceano-vida-2026"] = (
 "<p>Encélado é uma lua de Saturno, pequena e coberta de gelo, que chamou a atenção da ciência quando a sonda Cassini, da NASA, detectou jatos de vapor e partículas saindo de fraturas perto do polo sul. Esse material vem de um oceano de água líquida sob a crosta de gelo e passa a fazer parte de um dos anéis de Saturno.</p>"
 "<p>Como a água sai para o espaço, uma futura sonda poderia coletar amostras sem precisar perfurar o gelo. Isso faz de Encélado um dos alvos mais estudados na busca por ambientes que poderiam abrigar vida fora da Terra. Ainda assim, nenhum sinal de vida foi detectado até hoje, e o que se discute é como melhor interpretar o que eventualmente for encontrado.</p>",
 [("Lua gelada", "Satélite natural coberto por uma camada de gelo, às vezes com água líquida por baixo."),
  ("Pluma", "Jato de gás e partículas que escapa de uma superfície para o espaço."),
  ("Astrobiologia", "Área da ciência que estuda as condições para a vida e a possibilidade de ela existir fora da Terra.")])

E["celula-tronco-tendao-ligamento-2026"] = (
 "<p>Tendões ligam músculos a ossos, e ligamentos ligam ossos a outros ossos. São tecidos resistentes, mas com pouca irrigação sanguínea, e por isso cicatrizam devagar e muitas vezes de forma incompleta: lesões costumam deixar o tecido mais fraco ou propenso a voltar a se romper. Isso afeta atletas, mas também pessoas comuns e idosas.</p>"
 "<p>Identificar a célula que dá origem a esses tecidos é um passo básico para pensar em terapias de regeneração, porque indica qual população de células seria preciso estimular ou repor. É um resultado de pesquisa básica: até chegar a um tratamento, costumam ser necessários muitos anos de testes em animais e depois em pessoas.</p>",
 [("Célula-tronco", "Célula capaz de se multiplicar e de dar origem a células especializadas de um tecido."),
  ("Tendão", "Tecido fibroso que conecta músculo a osso e transmite a força da contração."),
  ("Ligamento", "Tecido fibroso que conecta ossos entre si e estabiliza as articulações.")])

E["ecowas-moeda-unica-eco-2026"] = (
 "<p>A Comunidade Econômica dos Estados da África Ocidental (CEDEAO, ou ECOWAS em inglês) reúne países com realidades monetárias diferentes. Parte deles, os da união monetária da África Ocidental (UEMOA), usa o franco CFA, ligado ao euro, enquanto outros, como Nigéria e Gana, têm moedas próprias. A ideia de uma moeda comum, chamada ECO, existe há anos, mas foi adiada várias vezes.</p>"
 "<p>Uma moeda única pode baratear o comércio e os pagamentos entre vizinhos, mas exige convergência de inflação, dívida e déficit público, além de um banco central comum. A experiência do euro mostra que os benefícios e os riscos dependem de as economias estarem suficientemente alinhadas, e o tema tem paralelos em debates sul-americanos sobre integração monetária.</p>",
 [("União monetária", "Grupo de países que adota a mesma moeda e a mesma política monetária."),
  ("Franco CFA", "Moeda usada por países da África Ocidental e Central, ligada ao euro por uma paridade fixa."),
  ("Critérios de convergência", "Metas de inflação, dívida e déficit que os países precisam cumprir para entrar em uma moeda única.")])

E["mamografia-sobrediagnostico-2026"] = (
 "<p>A mamografia é um exame de imagem usado para detectar câncer de mama, muitas vezes antes de surgirem sintomas. O rastreamento salva vidas, mas há uma discussão científica antiga sobre o sobrediagnóstico: casos de tumores detectados que talvez nunca crescessem a ponto de causar problemas, e que acabam tratados mesmo assim.</p>"
 "<p>Estimar o tamanho desse efeito é difícil, porque não é possível saber, para uma pessoa específica, o que teria acontecido sem o exame. Por isso os números variam conforme o método de cada estudo. Este texto é jornalismo sobre pesquisa e não substitui orientação médica: quem tem dúvidas sobre quando e com que frequência fazer o exame deve conversar com um profissional de saúde.</p>",
 [("Rastreamento", "Exames feitos em pessoas sem sintomas para detectar uma doença cedo."),
  ("Sobrediagnóstico", "Detecção de uma doença que não causaria sintomas nem risco de vida durante a vida da pessoa."),
  ("Falso positivo", "Resultado alterado em quem, depois de investigação, não tem a doença.")])

E["linear-a-decifracao-ia-2026"] = (
 "<p>O Linear A é um sistema de escrita usado pelos minoicos, civilização da ilha de Creta, na Grécia, por volta de 1800 a 1450 a.C. Ele nunca foi decifrado: sabe-se ler o valor aproximado de muitos sinais por comparação com o Linear B, escrita posterior usada para registrar uma forma antiga do grego, mas isso não revela o significado dos textos, que provavelmente registram outra língua.</p>"
 "<p>Reivindicações de decifração aparecem de tempos em tempos, e a academia costuma examiná-las com cautela, porque uma decifração só é aceita quando produz leituras consistentes e verificáveis em muitos documentos. A pouca quantidade de textos conhecidos é um dos principais obstáculos, e é por isso que o debate sobre o uso de IA nesse campo é acompanhado com atenção e ceticismo.</p>",
 [("Linear A", "Escrita da civilização minoica de Creta, ainda não decifrada."),
  ("Linear B", "Escrita posterior que registra uma forma antiga do grego e foi decifrada em 1952."),
  ("Decifração", "Processo de descobrir a língua e o significado de uma escrita antiga a partir de evidências.")])

E["plastico-sacola-combustivel-oak-ridge-2026"] = (
 "<p>O plástico é feito, em grande parte, de petróleo, e uma fração pequena de todo o que é produzido acaba reciclada. Sacolas e filmes plásticos são difíceis de reciclar de forma tradicional, porque são leves, sujam com facilidade e perdem qualidade a cada ciclo. Por isso há muito interesse em processos químicos que quebrem o plástico em moléculas menores, que podem virar combustíveis ou novos materiais.</p>"
 "<p>Muitos desses processos precisam de calor muito alto, o que gasta energia e pode emitir carbono. Métodos que funcionem a temperaturas mais baixas podem reduzir esse custo, mas ainda precisam provar que funcionam em escala industrial e com plástico misturado e sujo, como o que existe de verdade no lixo.</p>",
 [("Reciclagem química", "Uso de reações para quebrar o plástico em moléculas menores que podem ser reaproveitadas."),
  ("Pirólise", "Decomposição de um material por calor em ambiente sem oxigênio, usada em alguns processos de reciclagem."),
  ("Catalisador", "Substância que acelera uma reação química sem ser consumida por ela.")])

E["gana-economia-24-horas-2026"] = (
 "<p>Gana é uma das economias mais estáveis da África Ocidental e grande produtora de ouro e cacau. Como muitos países que dependem de matérias-primas, busca agregar valor ao que produz, com indústrias de transformação, em vez de apenas exportar o produto bruto.</p>"
 "<p>A ideia de uma economia 24 horas, em que fábricas, serviços e portos funcionam em vários turnos, busca usar melhor a capacidade instalada, criar empregos e aumentar as exportações. O desafio é ter energia confiável, transporte e mão de obra para sustentar a operação contínua, além de regras trabalhistas e de segurança adequadas, pontos que também aparecem em discussões sobre jornadas e turnos no Brasil.</p>",
 [("Economia 24 horas", "Modelo em que setores produtivos operam em turnos contínuos, de dia e de noite."),
  ("Agregação de valor", "Transformar matéria-prima em produtos de maior preço antes de vendê-los."),
  ("Polo de produção", "Região que concentra fábricas e cadeias de fornecedores de determinada atividade.")])

E["simulador-quantico-materia-energia-2026"] = (
 "<p>Um computador quântico usa bits quânticos, os qubits, que podem estar em combinações de estados e, por isso, permitem simular sistemas da própria física quântica que são difíceis de calcular em computadores comuns. Um dos usos mais promissores é justamente a simulação: reproduzir em laboratório o comportamento de partículas e campos que não se consegue observar diretamente.</p>"
 "<p>Íons presos em armadilhas eletromagnéticas são uma das tecnologias para construir esses sistemas. Experimentos com poucos íons, como o descrito aqui, são provas de conceito: mostram que um fenômeno pode ser reproduzido, mas ainda estão distantes de máquinas capazes de resolver problemas práticos que superem os computadores atuais.</p>",
 [("Qubit", "Unidade básica de informação quântica, que pode estar em combinações de 0 e 1."),
  ("Íon aprisionado", "Átomo com carga elétrica mantido no lugar por campos eletromagnéticos, usado como qubit."),
  ("Simulação quântica", "Uso de um sistema quântico controlado para reproduzir o comportamento de outro sistema quântico.")])

E["sono-rem-energia-cerebro-2026"] = (
 "<p>O sono é dividido em fases, e uma delas é o sono REM (sigla em inglês para movimentos rápidos dos olhos), quando ocorre boa parte dos sonhos mais vívidos. Nessa fase a atividade do cérebro lembra a da vigília, ainda que o corpo fique praticamente paralisado, e por isso há interesse em saber quanta energia ela consome.</p>"
 "<p>O cérebro humano é um órgão caro em termos de energia: representa uma pequena parte do peso do corpo, mas usa uma fração bem maior da energia disponível. Estudar o equilíbrio entre gasto e reposição durante o sono ajuda a entender por que dormir é necessário, uma pergunta que a ciência ainda não respondeu por completo.</p>",
 [("Sono REM", "Fase do sono com atividade cerebral intensa, movimentos rápidos dos olhos e sonhos mais vívidos."),
  ("Metabolismo cerebral", "Conjunto de processos pelos quais o cérebro produz e consome energia."),
  ("Vigília", "Estado em que a pessoa está acordada e consciente.")])

E["estrelas-massivas-galaxias-webb-2026"] = (
 "<p>O Telescópio Espacial James Webb, lançado no fim de 2021, observa o Universo em luz infravermelha e consegue ver galáxias muito distantes, ou seja, como elas eram há bilhões de anos. Desde as primeiras imagens, ele encontrou galáxias antigas mais brilhantes, ou com mais massa, do que muitos modelos esperavam para uma fase tão cedo da história cósmica.</p>"
 "<p>Esses achados levaram a debates sobre se as teorias sobre a formação de galáxias estão incompletas ou se há outras explicações, como estrelas muito massivas e diferentes das atuais, as primeiras que se formaram. Cada hipótese precisa ser testada com mais observações, e nenhuma delas está confirmada.</p>",
 [("Infravermelho", "Luz de comprimento de onda maior que o da luz visível, ideal para ver objetos muito distantes e antigos."),
  ("Primeiras estrelas", "Estrelas formadas logo depois do Big Bang, compostas quase só de hidrogênio e hélio."),
  ("Desvio para o vermelho", "Alongamento da luz de objetos distantes por causa da expansão do Universo, usado para estimar distâncias.")])

E["bateria-sodio-hyundai-2026"] = (
 "<p>As baterias de íons de lítio dominam os carros elétricos e os celulares, mas dependem de lítio, cobalto e níquel, materiais com cadeias de suprimento concentradas e preços voláteis. O sódio, presente no sal de cozinha, é muito mais abundante e barato, o que explica o interesse em baterias de íons de sódio.</p>"
 "<p>Em geral, essas baterias armazenam menos energia por quilo do que as de lítio, o que limita a autonomia, mas podem ser mais baratas e ter bom desempenho em temperaturas baixas. Passar em testes de segurança é uma etapa necessária antes da produção em escala, que depende ainda de custo, durabilidade e de uma cadeia industrial.</p>",
 [("Densidade de energia", "Quantidade de energia que uma bateria armazena por quilo ou por litro."),
  ("Íons de sódio", "Tecnologia de bateria que usa sódio, em vez de lítio, para transportar carga entre os eletrodos."),
  ("Fuga térmica", "Aquecimento descontrolado de uma bateria, que pode levar a incêndio. Testes de segurança procuram evitá-la.")])

E["musculos-envelhecimento-nervos-2026"] = (
 "<p>Com a idade, a maioria das pessoas perde massa e força muscular, um processo chamado sarcopenia. Ele aumenta o risco de quedas e reduz a autonomia, e costuma ser atribuído a vários fatores, entre eles a alimentação, a inatividade física e mudanças hormonais.</p>"
 "<p>Cada músculo recebe comandos de neurônios por meio de pontos de contato chamados junções neuromusculares. Se essa conexão se deteriora com o envelhecimento, a perda de força pode ter origem no nervo e não apenas no músculo. Entender a causa ajuda a pensar em tratamentos, mas a recomendação geral de atividade física regular, com treino de força, continua valendo.</p>",
 [("Sarcopenia", "Perda de massa e de força dos músculos associada ao envelhecimento."),
  ("Junção neuromuscular", "Ponto onde o nervo se conecta ao músculo e transmite o comando para contrair."),
  ("Unidade motora", "Um neurônio motor e o conjunto de fibras musculares que ele controla.")])

E["pacto-defesa-turquia-paquistao-arabia-2026"] = (
 "<p>Pactos de defesa mútua, como o da OTAN, funcionam pelo princípio de que um ataque a um dos membros é tratado como um ataque a todos. Esse tipo de compromisso muda o cálculo de quem pensa em atacar, e por isso é acompanhado de perto por governos e analistas.</p>"
 "<p>Os três países citados têm perfis militares e diplomáticos diferentes: a Turquia integra a OTAN, o Paquistão tem armas nucleares e a Arábia Saudita é grande potência energética e financeira. Os efeitos práticos de um acordo desse tipo dependem do texto, de como a obrigação de ajuda é definida e de como os governos o aplicarão, o que costuma levar tempo para ficar claro.</p>",
 [("Defesa mútua", "Compromisso em que os países se obrigam a ajudar um ao outro se algum for atacado."),
  ("Artigo 5 da OTAN", "Cláusula da aliança atlântica que trata o ataque a um membro como ataque a todos."),
  ("Dissuasão", "Estratégia de evitar um ataque deixando claro que a resposta teria custo muito alto.")])

E["cerebro-dois-orgaos-evolucao-2026"] = (
 "<p>O cérebro dos vertebrados evoluiu por camadas ao longo de centenas de milhões de anos. Estruturas mais antigas, ligadas a funções básicas como o controle do corpo e do olfato, convivem com regiões mais recentes, especialmente o neocórtex, muito desenvolvido em mamíferos e, nos humanos, ligado ao raciocínio e à linguagem.</p>"
 "<p>Propostas que reinterpretam como essas partes se combinaram ajudam a organizar o debate sobre a origem da inteligência, mas são hipóteses científicas e precisam ser testadas com dados de anatomia, genética e comparação entre espécies. Nenhum modelo único explica sozinho a complexidade do cérebro humano.</p>",
 [("Neocórtex", "Camada mais externa e recente do cérebro de mamíferos, ligada a funções como raciocínio, percepção e linguagem."),
  ("Evolução convergente", "Surgimento de características parecidas em linhagens diferentes, por pressões semelhantes."),
  ("Homologia", "Semelhança entre estruturas de espécies diferentes que vem de um ancestral comum.")])

E["long-covid-dopamina-2026"] = (
 "<p>A COVID longa é o nome dado a sintomas que persistem por semanas ou meses depois da infecção pelo coronavírus, como cansaço intenso, dificuldade de concentração e problemas de memória, às vezes chamados de névoa mental. Os sintomas variam muito, e não há ainda uma explicação única para todos os casos.</p>"
 "<p>A dopamina é uma substância que os neurônios usam para se comunicar e que participa da motivação, do movimento e da atenção. Estudos de imagem do cérebro que mostrem alterações nesse sistema ajudam a procurar mecanismos biológicos para os sintomas, o que pode orientar pesquisas de tratamento. Esse tipo de achado ainda não se traduz em terapia disponível, e quem tem sintomas persistentes deve procurar avaliação médica.</p>",
 [("COVID longa", "Conjunto de sintomas que continuam ou surgem depois da fase aguda da COVID-19."),
  ("Dopamina", "Neurotransmissor envolvido em motivação, atenção e controle do movimento."),
  ("Neuroimagem", "Técnicas para ver a estrutura e a atividade do cérebro, como a tomografia e a ressonância.")])

E["ue-greenwashing-alegacoes-verdes-2026"] = (
 "<p>Greenwashing é o nome dado a propagandas que passam uma imagem ambiental melhor do que a realidade, com termos vagos como \"verde\", \"eco\" ou \"amigo da natureza\". A União Europeia aprovou regras para limitar esse tipo de alegação, exigindo que as empresas possam comprová-las e restringindo afirmações genéricas e as ligadas a compensações de emissões.</p>"
 "<p>As regras valem para o mercado europeu, mas afetam quem vende para lá, incluindo exportadores brasileiros. Também servem de referência para outros países: no Brasil, o Código de Defesa do Consumidor e as normas de autorregulamentação publicitária já proíbem propaganda enganosa, e o debate sobre alegações ambientais ganha força.</p>",
 [("Greenwashing", "Prática de apresentar uma empresa ou produto como mais sustentável do que de fato é."),
  ("Alegação ambiental genérica", "Afirmação vaga, como \"eco\" ou \"verde\", sem explicar o que, de fato, é melhor para o meio ambiente."),
  ("Compensação de carbono", "Mecanismo em que uma empresa financia reduções de emissão em outro lugar para \"neutralizar\" as suas.")])

E["lingua-sidetica-alfabeto-2026"] = (
 "<p>O sidético é uma língua da Antiguidade falada na cidade de Side, na costa sul da atual Turquia, e conhecida por poucas inscrições, a maioria em pedra. Ele pertence ao conjunto de línguas da Anatólia, região onde também se falavam o hitita e o luvita, que formam um ramo antigo da família indo-europeia.</p>"
 "<p>Decifrar uma escrita pouco documentada é um trabalho lento, que depende de achar textos bilíngues ou de comparar sinais com línguas parentes. Cada letra identificada reduz a incerteza sobre como ler as inscrições, mas \"se aproximar de decifrar\" ainda não é o mesmo que ler todos os textos com segurança.</p>",
 [("Língua da Anatólia", "Grupo de línguas antigas da região da atual Turquia, muitas hoje extintas."),
  ("Texto bilíngue", "Inscrição que traz o mesmo conteúdo em duas línguas ou escritas, útil para decifrar uma delas."),
  ("Indo-europeu", "Família de línguas que inclui o português, o grego, o latim, o hindi e o inglês.")])

E["india-deep-tech-espacial-2026"] = (
 "<p>\"Deep tech\" é o nome dado a empresas baseadas em avanços científicos e de engenharia difíceis de copiar, como espaço, biotecnologia, semicondutores e inteligência artificial. Elas costumam exigir mais tempo e capital até gerar receita do que um aplicativo comum.</p>"
 "<p>A Índia tem um programa espacial público, a ISRO, conhecido por missões de baixo custo, como a que levou uma sonda a Marte em 2014 e o pouso próximo ao polo sul da Lua em 2023. Nos últimos anos o país abriu o setor espacial à iniciativa privada, o que ajuda a explicar o surgimento de startups e o fluxo de investimento citado na reportagem.</p>",
 [("Deep tech", "Empresas baseadas em ciência e engenharia avançadas, com ciclos longos de desenvolvimento."),
  ("ISRO", "Organização Indiana de Pesquisa Espacial, a agência espacial do país."),
  ("Capital de risco", "Investimento em empresas jovens com alto potencial e alto risco.")])

E["ue-eolica-solar-fosseis-2026"] = (
 "<p>A União Europeia vem ampliando a geração solar e eólica há anos, impulsionada por metas climáticas e pela busca de reduzir a dependência de gás importado, tema que ganhou urgência depois de 2022. Quando se diz que essas fontes \"superam os fósseis\", a comparação costuma ser da eletricidade gerada em um período, não de toda a energia consumida, que inclui transporte e aquecimento.</p>"
 "<p>Para o Brasil, que já tem uma matriz elétrica majoritariamente renovável, graças às hidrelétricas, a experiência europeia mostra desafios que também aparecem aqui, como a necessidade de redes, de armazenamento e de gerenciar a variação da geração solar e eólica ao longo do dia e do ano.</p>",
 [("Matriz elétrica", "Conjunto de fontes usadas para gerar a eletricidade de um país."),
  ("Intermitência", "Variação da geração conforme o sol e o vento, que não são constantes."),
  ("Armazenamento", "Sistemas, como baterias, que guardam energia para usar quando a geração é menor.")])

E["china-seguro-cuidados-idosos-2026"] = (
 "<p>A China está envelhecendo rápido: a população em idade de trabalho diminui e o número de idosos cresce, resultado, em parte, de décadas de política do filho único e da queda da natalidade. Isso aumenta a demanda por cuidados de longo prazo, que tradicionalmente eram assumidos pelas famílias.</p>"
 "<p>O sistema de seguridade social chinês já inclui seguros de aposentadoria, saúde, desemprego, acidente de trabalho e maternidade, os cinco tradicionais. Um seguro específico para cuidados de longo prazo é uma resposta a esse envelhecimento. O Brasil também está envelhecendo, em ritmo acelerado, e discute quem paga e organiza o cuidado de pessoas idosas dependentes.</p>",
 [("Cuidados de longo prazo", "Apoio contínuo a pessoas que precisam de ajuda nas atividades diárias, como idosos dependentes."),
  ("Seguridade social", "Conjunto de políticas de proteção, como aposentadoria, saúde e seguros de risco."),
  ("Envelhecimento populacional", "Aumento da proporção de idosos em relação ao total da população.")])

E["coracao-regenera-infarto-2026"] = (
 "<p>O infarto acontece quando uma artéria que leva sangue ao coração é bloqueada, e parte do músculo cardíaco morre. Por muito tempo se acreditou que o coração adulto humano quase não se regenera, e que o músculo perdido é substituído por cicatriz, o que reduz a capacidade de bombear sangue e pode levar à insuficiência cardíaca.</p>"
 "<p>Mostrar que há regeneração de músculo depois do infarto, ainda que limitada, abre caminhos para pensar em tratamentos que estimulem esse processo. Resultados desse tipo vêm de pesquisa básica e precisam ser confirmados e transformados em terapias seguras antes de chegar aos pacientes, o que costuma levar anos.</p>",
 [("Infarto do miocárdio", "Morte de parte do músculo do coração por falta de sangue."),
  ("Cardiomiócito", "Célula muscular do coração, responsável por contrair e bombear o sangue."),
  ("Insuficiência cardíaca", "Condição em que o coração não consegue bombear sangue de forma suficiente para o corpo.")])

E["karahantepe-estatua-leopardo-2026"] = (
 "<p>Karahan Tepe é um sítio arqueológico no sudeste da Turquia, vizinho de Göbekli Tepe, onde há estruturas de pedra com pilares esculpidos feitas por comunidades de caçadores-coletores, por volta de 11 mil anos atrás, antes da agricultura. Esses locais mudaram a ideia de que construções monumentais só apareceriam depois do surgimento da agricultura.</p>"
 "<p>Representações de animais, como leopardos, serpentes e raposas, são comuns nesses sítios e sugerem um repertório simbólico e talvez rituais compartilhados. Interpretar o significado de uma imagem tão antiga, sem textos para guiar, é sempre uma hipótese, e os arqueólogos distinguem o que foi encontrado do que é interpretação.</p>",
 [("Caçadores-coletores", "Povos que viviam da caça e da coleta, sem agricultura nem criação de animais."),
  ("Pilar em T", "Monólito de pedra em formato de T, típico dos sítios do sudeste da Anatólia nesse período."),
  ("Iconografia", "Estudo das imagens e símbolos usados por uma cultura.")])

E["china-russia-asia-central-2026"] = (
 "<p>A Ásia Central, formada por Cazaquistão, Quirguistão, Tadjiquistão, Turcomenistão e Uzbequistão, foi parte da União Soviética até 1991, e a Rússia manteve ali grande peso econômico e político. Nas últimas décadas, a China aumentou investimentos, empréstimos e obras de infraestrutura na região, em parte pela Iniciativa do Cinturão e Rota.</p>"
 "<p>Ser a maior parceira comercial significa que o comércio com a China, em valor, supera o de cada outro país, o que não quer dizer controle da região. Os governos locais costumam buscar equilíbrio entre vários parceiros, incluindo Rússia, China, União Europeia, Turquia e Estados Unidos, e a posição relativa dos países muda com sanções, preços de commodities e novos corredores de transporte.</p>",
 [("Ásia Central", "Região de cinco países de maioria muçulmana que foram repúblicas soviéticas."),
  ("Iniciativa do Cinturão e Rota", "Programa chinês de investimentos em infraestrutura que liga a China a outras regiões do mundo."),
  ("Parceiro comercial", "País com o qual se movimenta o maior valor de exportações e importações.")])

E["antidepressivos-rios-peixes-2026"] = (
 "<p>Medicamentos tomados por pessoas passam pelo organismo e são eliminados na urina, chegando às estações de tratamento de esgoto, que nem sempre removem esses compostos por completo. Resíduos de remédios acabam em rios e lagos, em concentrações muito baixas, e a ciência estuda se isso afeta os animais aquáticos que vivem ali.</p>"
 "<p>Antidepressivos agem em sistemas químicos do cérebro que existem também em peixes, o que explica o interesse em verificar efeitos no comportamento e na reprodução desses animais. Estudos de laboratório mostram efeitos em certas condições, e a discussão é se as concentrações encontradas no ambiente são suficientes para provocá-los. No Brasil, o tratamento de esgoto ainda não alcança toda a população, o que torna o tema relevante também por aqui.</p>",
 [("Contaminante emergente", "Substância, como remédios e produtos de higiene, que aparece na água em baixas concentrações e cujo risco ainda é estudado."),
  ("Tratamento de esgoto", "Processo que remove sujeira e parte dos poluentes da água antes de devolvê-la ao ambiente."),
  ("Bioacumulação", "Acúmulo de uma substância no organismo de um ser vivo ao longo do tempo.")])

E["computacao-quantica-mil-vezes-2026"] = (
 "<p>Computadores quânticos usam qubits, que são frágeis: qualquer interferência do ambiente pode apagar a informação em instantes. Por isso dois problemas centrais são fazer operações rápidas e corrigir erros, e quanto mais rápida for uma operação em relação ao tempo em que o qubit mantém a informação, mais cálculos cabem antes de ele perdê-la.</p>"
 "<p>Operações mais rápidas ajudam, mas sozinhas não bastam para construir máquinas úteis: é preciso ter muitos qubits, baixas taxas de erro e sistemas de correção. Resultados de laboratório como este mostram progresso em uma das peças do quebra-cabeça, sem indicar que computadores quânticos práticos estejam prontos.</p>",
 [("Coerência", "Tempo durante o qual um qubit mantém sua informação quântica antes de ser perturbado."),
  ("Porta quântica", "Operação básica aplicada a qubits, equivalente a uma instrução de um computador comum."),
  ("Correção de erros", "Técnicas para detectar e corrigir falhas nos qubits durante um cálculo.")])

E["everything-to-grid-2026"] = (
 "<p>Carros elétricos têm baterias grandes, e a maior parte do tempo ficam parados. A ideia do \"everything-to-grid\" é aproveitar essa capacidade: veículos, casas com baterias e painéis solares podem devolver energia à rede quando ela está mais cara ou mais necessária, em vez de apenas consumir.</p>"
 "<p>Isso pede carregadores bidirecionais, regras do setor elétrico que permitam vender a energia e tarifas que premiem a flexibilidade. Para quem usa o carro, há ainda dúvidas sobre o desgaste da bateria e sobre como se garante que o veículo esteja carregado quando for preciso. No Brasil, a geração distribuída solar já é comum, e o debate sobre armazenamento e flexibilidade da rede está avançando.</p>",
 [("Carregador bidirecional", "Carregador que, além de carregar o carro, permite que a energia da bateria volte para a casa ou para a rede."),
  ("Geração distribuída", "Produção de energia perto de onde é consumida, como painéis solares em telhados."),
  ("Resposta da demanda", "Ajuste do consumo de energia conforme as condições da rede, geralmente com incentivo financeiro.")])
