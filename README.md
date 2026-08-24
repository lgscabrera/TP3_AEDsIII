# Trabalho Prático 3 - Algoritmos de Caminho Mais Curto

**Disciplina:** AEDS 3 (DCE797)  
**Professor:** Iago Augusto de Carvalho  

---

## 📌 Objetivo

Este trabalho tem como objetivo implementar e avaliar **três algoritmos de caminho mais curto** em grafos ponderados, conexos e não orientados. Os algoritmos devem encontrar a menor distância entre um vértice de origem e todos os demais vértices do grafo.

Os algoritmos implementados são:

1. **Dijkstra** (versão clássica com vetor de distâncias)
2. **Duan** (algoritmo inovador de 2025, com heap mínimo)
3. **Bellman-Ford** (terceiro algoritmo escolhido)

Além da implementação, o trabalho inclui:
- Geração de grafos de teste (3 topologias diferentes, 500 a 10000 vértices)
- Análise comparativa de tempo de execução
- Relatório em PDF e apresentação de slides

---

## 🧠 Funcionamento dos Algoritmos

### 1. Algoritmo de Dijkstra

**Complexidade teórica:** O(V²) com matriz de adjacência

**Funcionamento:**
- Mantém um conjunto de vértices visitados e um vetor de distâncias mínimas
- A cada iteração, seleciona o vértice não visitado com menor distância
- Relaxa (atualiza) as distâncias dos vizinhos desse vértice
- Repete até que todos os vértices sejam visitados

**Características:**
- Funciona apenas com pesos não negativos
- Implementação simples com vetor (sem heap)
- Garante a solução ótima

### 2. Algoritmo de Duan (2025)

**Complexidade teórica:** O((V+E) log V) com heap mínimo

**Funcionamento:**
- Similar ao Dijkstra, mas utiliza uma **fila de prioridade (heap mínimo)**
- O heap permite extrair o vértice de menor distância mais eficientemente
- Inserções e extrações são O(log V)
- Reduz a complexidade para grafos esparsos

**Características:**
- Versão otimizada do Dijkstra
- Ideal para grafos com muitas arestas
- Foi proposta em 2025 e ainda não foi caracterizada empiricamente

### 3. Bellman-Ford (Terceiro Algoritmo)

**Complexidade teórica:** O(V × E)

**Funcionamento:**
- Inicializa distâncias como infinito (exceto origem = 0)
- Relaxa todas as arestas (V-1) vezes
- Cada iteração propaga as distâncias mínimas pelo grafo
- Permite detectar ciclos de peso negativo

**Características:**
- **Único** dos três que lida com pesos negativos
- Mais lento que os outros para grafos densos
- Útil quando há restrições de pesos negativos
- Implementado com três loops aninhados

---

## 📊 Comparação Teórica

| Algoritmo | Complexidade | Pesos Negativos | Estrutura | Uso Ideal |
|-----------|--------------|-----------------|-----------|-----------|
| Dijkstra | O(V²) | ❌ Não | Vetor | Grafos densos |
| Duan | O((V+E) log V) | ❌ Não | Heap | Grafos esparsos |
| Bellman-Ford | O(V×E) | ✅ Sim | Vetor | Pesos negativos |

---

## 🛠️ Como Compilar e Executar

### Pré-requisitos

- Compilador GCC
- Make (opcional, mas recomendado)
- Sistema Linux/Unix ou WSL no Windows

### Estrutura do Projeto
```text
TRABALHO_3---AEDS_III/
├── docs/ 
    ├── test_info.txt
    └── results.csv
├── instance/
    ├── generate_graphs.py
    ├── generator.py
    └── requirements.txt
├── scr/
    ├── output/
    ├── algorithms.c
    ├── algorithms.h
    ├── base.c
    ├── Makefile 
    ├── run_test.py
    └── exemplo.dat
├── Trabalho 3 - Informações/
    ├── descricao.pdf
    ├── duan.pdf
    ├── gerador de instancias/
        ├── generator.py
        └── requirements.txt
    └── codigo base/
        ├── algorithms.c
        ├── algorithms.h
        ├── base.c
        ├── Makefile 
        ├── exemplo.dat
        ├── generator.py
        └── requirements.txt
└── README.md

```


### Compilação com Make

```bash
    # Compilar o programa
    make

    # Limpar arquivos objeto e executável
    make clean

    # Criar arquivo de exemplo para teste
    make create-example

    # Executar com o arquivo padrão
    make run

    # Mostrar ajuda
    make help
```

## Compilação Manual (sem Make)

### Compilar os arquivos objeto
```bash
gcc -Wall -Wextra -O2 -c base.c -o base.o
gcc -Wall -Wextra -O2 -c algorithms.c -o algorithms.o

# Linkar e criar o executável
gcc -Wall -Wextra -O2 -o programa base.o algorithms.o -lm

# Executar
./programa instancia_exemplo.dat
```
## Execução
```bash

# Sintaxe
./programa <arquivo_grafo>

# Exemplo
./programa instancia_exemplo.dat
```
### 📁 Formato dos Arquivos de Grafo

Os arquivos de grafo devem seguir este formato:
```text
<V> <E>
<u1> <v1> <peso1>
<u2> <v2> <peso2>
...
<uE> <vE> <pesoE>
```
Exemplo (instancia_exemplo.dat):
```text
5 6
0 1 4
0 2 2
1 2 1
1 3 5
2 3 8
2 4 10
```
Legenda:

* Primeira linha: número de vértices (V) e número de arestas (E)
* Linhas seguintes: vértice de origem, vértice de destino e peso da aresta
* Vértices são indexados de 0 a V-1
* O grafo é não orientado (a aresta é adicionada nos dois sentidos)

## 📊 Saída do Programa

O programa imprime uma linha para cada algoritmo:
```text

Dijkstra: <custo_total> <tempo_segundos>
Duan: <custo_total> <tempo_segundos>
Outro: <custo_total> <tempo_segundos>
```
Exemplo de saída:
```text

Dijkstra: 31.000000 0.000034
Duan: 31.000000 0.000028
Outro: 31.000000 0.000056
```
* custo_total: Soma das distâncias mínimas da origem (vértice 0) a todos os vértices
* tempo_segundos: Tempo de execução do algoritmo em segundos

## 🛠️ Como utilizar o `generator.py`

O script `generator.py` é uma ferramenta de linha de comando desenvolvida em Python que utiliza a biblioteca NetworkX para gerar diferentes tipos de grafos conexos. Ele atribui posições aleatórias, classes aos nós e pesos (`w1`) às arestas.

## Pré-requisitos

Antes de executar o script, é necessário instalar as dependências listadas no projeto. O arquivo `requirements.txt` exige as bibliotecas `networkx` e `scipy`. Para instalá-las, execute:

```bash
pip install -r requirements.txt
```
Sintaxe Básica

A execução do gerador segue o seguinte padrão via terminal:
```bash

./generator.py <topologia_do_grafo> <numero_de_nos> [argumentos_adicionais...]
```

### Topologias Suportadas e Argumentos

O script suporta diversas topologias de grafos, sendo que o primeiro argumento após o tipo de grafo é sempre o número de nós (n). Alguns modelos exigem parâmetros adicionais específicos:

* complete (Grafo Completo):
    
        Uso: python3 generator.py complete <n>

* erdos (Grafo de Erdős-Rényi):

        Uso: python3 generator.py erdos <n> <p>

        p (float): Probabilidade de criação de aresta.

* watts (Grafo de Watts-Strogatz):

        Uso: python3 generator.py watts <n> <k> <p>

        k (int): Cada nó é unido aos seus k vizinhos mais próximos (topologia em anel).

        p (float): Probabilidade de reconectar cada aresta.

* barabasi (Grafo de Barabási-Albert):

        Uso: python3 generator.py barabasi <n> <m>

        m (int): Número de arestas a serem anexadas de um novo nó aos nós existentes.

* turan (Grafo de Turán):

        Uso: python3 generator.py turan <n> <r>

        r (int): Número de partições.

* powerlaw (Powerlaw Cluster Graph):

        Uso: python3 generator.py powerlaw <n> <m> <p>

        m (int): Número de arestas a anexar a partir de um novo nó.

        p (float): Probabilidade de formar um triângulo após adicionar uma aresta aleatória.

* regular (Grafo Regular Aleatório):

        Uso: python3 generator.py regular <n> <d>

        d (int): Grau de cada nó.

* udg_u (Unit Disk Graph - Disposição Uniforme):

        Uso: python3 generator.py udg_u <n> <radius>

        radius (float): Valor do limite do raio.

* udg_r (Unit Disk Graph - Disposição Aleatória):

        Uso: python3 generator.py udg_r <n> <radius>

        radius (float): Valor do limite do raio.

### Exemplo de Execução

Para gerar um grafo de Erdős-Rényi com 10 nós e uma probabilidade de 0.5 (50%) de criação de arestas, execute:
```Bash
python3 generator.py erdos 10 0.5
```
---
## Explicação Detalhada dos Dados no results.csv
O arquivo results.csv contém 8 colunas com informações sobre os testes realizados nos diferentes tipos de grafos. Abaixo está a explicação detalhada de cada campo:

## Estrutura do CSV
```csv
Quantidade_Vertices;Tipo_Grafo;Custo_Dijkstra;Tempo_Dijkstra(s);Custo_Duan;Tempo_Duan(s);Custo_BellmanFord;Tempo_BellmanFord(s)
```
### 1. Quantidade_Vertices

| Propriedade |	Descrição |
|-----------|--------------|
| O que é | Número de nós (vértices) no grafo| 
| Tipo | Número inteiro |
| Intervalo | Definido pelo usuário (ex: 500 a 10000) |
|Exemplo | 500, 1584, 5011 |

#### Importância:

* Permite analisar como os algoritmos escalam com o aumento do grafo
* Quanto mais vértices, maior a complexidade computacional
* Fundamental para testes de desempenho e complexidade assintótica

### 2. Tipo_Grafo
|Propriedade	|Descrição|
|-----------|--------------|
O que é|	Topologia/estrutura do grafo gerado|
Tipo|	String (texto)|
Valores possíveis|	erdos, watts, barabasi, complete, regular|
Exemplo	|erdos, barabasi|

#### Características de cada tipo:

|Tipo	|Descrição	|Densidade	|Aplicação típica|
|-----------|--------------|--------------|--------------|
erdos|	Erdős-Rényi - arestas com probabilidade p	|Controlada por p	|Redes aleatórias|
watts|	Watts-Strogatz - mundo pequeno	|Moderada|	Redes sociais|
barabasi|	Barabási-Albert - livre de escala	|Baixa a moderada	|Internet, redes biológicas|
complete	|Grafo completo - todos conectados	|Máxima (denso)	|Teste de pior caso|
regular|	Grafo regular - todos mesmo grau	|Constante	|Redes estruturadas|

#### Importância:

* Diferentes topologias afetam o desempenho dos algoritmos
* Permite comparar eficiência em diferentes estruturas de grafo

### 3. Custo_Dijkstra
|Propriedade	|Descrição|
|--------------|--------------|
O que é	|Soma das distâncias mínimas da origem até todos os vértices|
Tipo|	Número decimal (float)|
Unidade	Adimensional |(soma dos pesos das arestas)|
Intervalo típico|	Depende do grafo (ex: 0 a ~1.000.000)|
Exemplo	|12345.678901|

#### Cálculo:
```c
// O algoritmo Dijkstra calcula a menor distância da origem (0) a cada vértice
dist[0] = 0;        // Distância para a origem
dist[1] = 10;       // Menor caminho para vértice 1
dist[2] = 5;        // Menor caminho para vértice 2
dist[3] = 8;        // Menor caminho para vértice 3

// Custo total = soma de todas as distâncias
custo_total = 0 + 10 + 5 + 8 = 23
```
#### Importância:

* Validação: Deve ser IDÊNTICO ao Custo_Duan e Custo_BellmanFord
* Se diferente, indica erro na implementação do algoritmo
* Permite verificar se os caminhos mínimos estão corretos

### 4. Tempo_Dijkstra(s)
|Propriedade	|Descrição|
|--------------|--------------|
O que é	|Tempo de execução do algoritmo de Dijkstra|
Tipo|	Número decimal (float)|
Unidade	|Segundos|
Intervalo típico|	0.000001 a vários segundos|
Exemplo|	0.002345 (2.345 milissegundos)|

#### Complexidade Teórica:
```text
Dijkstra com matriz de adjacência: O(V²)
Onde V = número de vértices
```
Fatores que afetam o tempo:
* Número de vértices (maior impacto)
* Densidade do grafo (matriz cheia vs esparsa)
* Implementação (array simples vs heap)

#### Importância:

* Mede a eficiência da implementação com matriz de adjacência
* Útil para verificar a complexidade O(V²) na prática

#### 5. Custo_Duan
|Propriedade	|Descrição|
|--------------|--------------|
O que é	|Soma das distâncias mínimas (MESMO valor do Dijkstra)
Tipo	|Número decimal (float)
Unidade	|Adimensional
Exemplo	|12345.678901 (deve ser igual ao Dijkstra)

#### Importância:

* Validação cruzada: Deve ser EXATAMENTE igual ao Custo_Dijkstra
* Confirma que o algoritmo de Duan (heap) está correto
* Diferenças indicam bugs na implementação

### 6. Tempo_Duan(s)
|Propriedade|	Descrição|
|--------------|--------------|
O que é	|Tempo de execução do algoritmo de Duan (versão otimizada)
Tipo	|Número decimal (float)
Unidade	|Segundos
Exemplo	|0.001234 (1.234 milissegundos)

#### Complexidade Teórica:
```text
Duan com heap mínimo: O((V + E) log V)
Onde:
  V = número de vértices
  E = número de arestas
Comparação com Dijkstra:

Para grafos esparsos (E ≈ V): Duan é MAIS RÁPIDO que Dijkstra O(V²)

Para grafos densos (E ≈ V²): Dijkstra pode ser competitivo
```
#### Importância:

* Avalia a eficiência da implementação com heap
* Deve ser mais rápido que Dijkstra em grafos esparsos
* Testa a melhoria da complexidade de O(V²) para O((V+E) log V)

### 7. Custo_BellmanFord
|Propriedade	|Descrição|
|--------------|--------------|
O que é	|Soma das distâncias mínimas (MESMO valor dos outros)
Tipo	|Número decimal (float)
Unidade	|Adimensional
Exemplo	|12345.678901 (deve ser igual aos outros)

#### Importância:

* Terceira validação: Confirma consistência entre os três algoritmos
* Bellman-Ford é mais geral (aceita pesos negativos)
* Serve como referência para verificar os outros dois

### 8. Tempo_BellmanFord(s)
Propriedade	|Descrição
|--------------|--------------|
O que é	|Tempo de execução do algoritmo de Bellman-Ford
Tipo	|Número decimal (float)
Unidade	|Segundos
Exemplo|	0.123456 (123.456 milissegundos)

#### Complexidade Teórica:
```text
Bellman-Ford: O(V × E)
Onde:
  V = número de vértices
  E = número de arestas
Características:

MAIS LENTO que Dijkstra e Duan para grafos sem pesos negativos

Pode detectar ciclos de peso negativo

Complexidade cúbica em grafos densos: O(V³)
```

#### Importância:

* Serve como baseline para comparar eficiência
* Demonstra na prática porque Dijkstra/Duan são preferíveis
* Útil para entender a diferença de complexidade

---

## Relatório Técnico dos Testes de Algoritmos de Caminho Mínimo
### Visão Geral do Experimento
Foi realizado um teste extensivo em larga escala para avaliar o desempenho de três algoritmos de caminho mínimo (Dijkstra, Duan e Bellman-Ford) em diferentes topologias de grafos. O experimento envolveu a geração e execução de 10.000 instâncias de grafos, totalizando 213.7 GB de dados processados.

### Configuração do Teste
#### Parâmetros do Experimento
* Total de instâncias: 10.000 grafos
* Distribuição: 2.000 grafos de cada tipo (5 tipos)
* Variação de vértices: 500 a 10.000 por grafo
* Tamanho total dos dados: 213.7 GB
* Tempo total de processamento: ~8 horas (6h geração + 2h testes)

#### Tipos de Grafos Testados
Tipo|	Quantidade	|Característica
|--------------|--------------|--------------|
Erdős-Rényi|	2.000	|Grafos aleatórios com probabilidade fixa
Watts-Strogatz	|2.000	|Grafos de "mundo pequeno"
Barabási-Albert	|2.000|	Grafos livres de escala
Completo	|2.000|	Grafos densos (todos conectados)
Regular	|2.000	|Grafos com grau uniforme

#### Hardware Utilizado
 Componente	|Modelo/Especificação	|Impacto nos Testes|
|--------------|--------------|--------------|
Placa Mãe	|B550M Aorus Elite	|Suporte PCIe 4.0, boa largura de banda
CPU|	AMD Ryzen 7 5700X|	8 núcleos / 16 threads @ 4.67 GHz
GPU|	RX 6600 XT (12GB)|	Não utilizada (processamento CPU-bound)
RAM	|64 GB DDR4 @ 3200 MHz	|Essencial para processar grafos grandes
Armazenamento	|1 TB SSD SATA|	Leitura/escrita rápida dos 213.7 GB
Sistema	|Ubuntu 24.04 (kernel 6.17)|	Ambiente otimizado para desenvolvimento

### Análise do Hardware para o Teste
1. CPU Ryzen 7 5700X: Ideal para processamento paralelo (8 núcleos/16 threads). Algoritmos de caminho mínimo são CPU-bound, beneficiando-se da alta frequência (4.67 GHz).
2. 64 GB RAM: Fundamental para manipular múltiplos grafos grandes. Um grafo com 10.000 vértices pode ocupar ~400 MB em memória (matriz de adjacência 10.000×10.000).
3. SSD 1TB: Essencial para ler 213.7 GB de dados em ~2 horas (taxa média de ~30 MB/s por arquivo).

### Tempos de Processamento
#### Geração das Instâncias: ~6 horas
```text
Processo de geração:
├── Criar 2.000 grafos/tipo × 5 tipos = 10.000 arquivos
├── Para cada grafo: gerar topologia, arestas e pesos
├── Salvar 10.000 arquivos totalizando 213.7 GB
└── Velocidade média: ~35.6 GB/hora ou ~10 MB/s
Fatores que influenciaram a geração:

Complexidade de geração de cada topologia

Garantia de conectividade dos grafos

Escrita no SSD de arquivos grandes
```

#### Execução dos Testes: ~2 horas
```text
Processamento dos algoritmos:
├── 10.000 execuções completas (3 algoritmos por execução)
├── Leitura de 213.7 GB de dados
├── Processamento de ~30.000 algoritmos (10k × 3)
└── Velocidade média: ~106.8 GB/hora (~30 MB/s)
Tempo por operação:

Leitura do grafo do disco

Execução Dijkstra: O(V²)

Execução Duan: O((V+E) log V)

Execução Bellman-Ford: O(V×E)

Escrita dos resultados
```

### Análise de Performance por Algoritmo
#### Complexidades Teóricas vs. Práticas
|Algoritmo	|Complexidade	|Tempo esperado (V=10.000) | Comportamento observado|
|--------------|--------------|--------------|--------------|
Dijkstra 	|O(V²)	|~100 milhões de operações|	Melhor em grafos densos
Duan (Heap)	|O((V+E) log V)	|~200 mil operações (esparso)|	Melhor em grafos esparsos
Bellman-Ford	|O(V×E)	|~1 bilhão de operações (denso)	|Mais lento, usado como validação

### Distribuição de Tempo por Tipo de Grafo
Espera-se que o desempenho varie significativamente por tipo:

```text
Grafos Completos (densos):
├── Dijkstra: Mais rápido (operações previsíveis)
├── Duan: Penalizado pelo heap (overhead)
└── Bellman-Ford: Extremamente lento (O(V³))

Grafos Erdős-Rényi (esparsos, p baixo):
├── Dijkstra: Penalizado por O(V²)
├── Duan: Muito mais rápido (O(E log V))
└── Bellman-Ford: Lento, mas menos que completos

Grafos Watts-Strogatz (mundo pequeno):
├── Balanceado: densidade média
├── Duan geralmente melhor que Dijkstra
└── Bellman-Ford: significativamente mais lento

Grafos Barabási-Albert (livres de escala):
├── Estrutura hierárquica
├── Duan se destaca pela esparsidade
└── Bellman-Ford: tempo proporcional a V × E

Grafos Regulares:
├── Grau constante: E = (n × d)/2
├── Comportamento linear com o número de vértices
└── Duan: melhor desempenho geral
```

### Métricas Importantes Obtidas
#### Capacidade de Processamento
* Grafos por segundo: ~1.39 grafos/segundo (10.000/7200s)
* Dados processados por segundo: ~30.4 MB/s
* Operações de CPU: Bilhões de operações de relaxamento

#### Eficiência do Hardware
* Uso de CPU: 100% durante processamento (multi-thread)
* Uso de RAM: Pico de ~32-48 GB
* Uso de SSD: Leitura constante ~200-300 MB/s

---

# 🛠️Execução dos Automática dos Testes
```Bash
python3 generate_graphs.py -n 5 -min 500 -max 10000
```
O que esse comando faz?

Esse comando executa o script generate_graphs.py, responsável por criar automaticamente arquivos de grafos para os testes dos algoritmos.

Parâmetros utilizados
* python3

 Executa o interpretador Python 3
* generate_graphs.py

 Script responsável pela geração automática dos grafos
* -n 5

 Define a quantidade de grafos que serão gerados

Resultado

O script cria automaticamente instâncias de grafos com diferentes tamanhos e topologias para serem utilizadas nos testes de desempenho dos algoritmos de caminho mínimo.

# 🛠️Executar os Testes
```Bash
python3 run_test.py
```
O que esse comando faz?

Esse comando executa o script run_test.py, responsável por automatizar os testes dos algoritmos implementados.

Funcionamento

O script:

* Lê os grafos gerados anteriormente

* Executa os algoritmos:
  * Dijkstra
  * Duan
  * Bellman-Ford

* Mede o tempo de execução de cada algoritmo

* Calcula os custos mínimos encontrados

* Salva os resultados para análise comparativa

---

# 👥 Grupo

Integrantes:

* Joaquim Pedro do Nascimento Moreira de Jesus
* Victória Almeida Tambasco
* Murilo Antonio da Silva
* Luiz Gabriel da Silva Cabrera
* Luiz Fernando Ferreira Cabral

Trabalho desenvolvido em grupo conforme as diretrizes da disciplina.

---