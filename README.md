# Wumpus World

**Disciplina:** Introdução à Inteligência Artificial  
**Semestre:** 2025.2  
**Professor:** André Luis Fonseca Faustino  
**Turma:** T04

## Integrantes do Grupo
* Clóvis Luan Medeiros de Araújo (20240015041)
* Daniel Vítor de Oliveira Bezerra (20240005377)

## Descrição do Projeto
Este projeto implementa uma simulação interativa do clássico problema de Inteligência Artificial: o **Mundo do Wumpus**. O objetivo é desenvolver um Agente Inteligente capaz de explorar um ambiente parcialmente observável, inferir conhecimentos sobre perigos (Poços e Wumpus) baseados em percepções sensoriais (Brisa e Fedor) e traçar rotas seguras para encontrar o Ouro e retornar à saída.

O projeto foi desenvolvido em **Python** utilizando a biblioteca **Pygame** para a interface gráfica. O agente possui uma Base de Conhecimento (KB) dinâmica e permite ao usuário selecionar entre diferentes algoritmos de busca para a tomada de decisão:
* **BFS (Busca em Largura)**
* **DFS (Busca em Profundidade)**
* **A* (A-Star Search)**

## Guia de Instalação e Execução

Siga os passos abaixo para rodar o projeto em sua máquina local.

### 1. Instalação das Dependências
Certifique-se de ter o **Python 3.x** instalado. Clone o repositório e instale as bibliotecas necessárias:

```bash
# Clone o repositório
git clone [INSIRA O LINK DO SEU REPOSITÓRIO AQUI]

# Entre na pasta do projeto
cd wumpus-world

# Instale as dependências (neste projeto, a principal é o pygame)
pip install -r requirements.txt
````

### 2. Como Executar

Execute o comando abaixo no terminal para iniciar o servidor local:

```bash
# Exemplo para Streamlit
streamlit run src/app.py
```

Se necessário, especifique a porta ou url de acesso, ex: http://localhost:8501

## Estrutura dos Arquivos

[Descreva brevemente a organização das pastas]

  * `src/`: Código-fonte da aplicação ou scripts de processamento.
  * `notebooks/`: Análises exploratórias, testes e prototipagem.
  * `data/`: Datasets utilizados (se o tamanho permitir o upload).
  * `assets/`: Imagens, logos ou gráficos de resultados.

## Resultados e Demonstração

[Adicione prints da aplicação em execução ou gráficos com os resultados do modelo/agente. Se for uma aplicação Web, coloque um print da interface.]

## Referências

  * [Link para o Dataset original]
  * [Artigo, Documentação ou Tutorial utilizado como base]