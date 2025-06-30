# Dashboard de Produtividade da Soja no RS

Este é um dashboard interativo desenvolvido em Python com a biblioteca **Dash** para visualizar e analisar a produtividade da soja no estado do Rio Grande do Sul, Brasil. Ele utiliza um modelo de **Random Forest** para prever a produtividade com base em dados históricos de temperatura, precipitação e área plantada.

---

## 📄 Sobre o Projeto

A produção de soja é altamente suscetível às condições climáticas. Este projeto visa quantificar e prever o impacto das variações mensais de temperatura e precipitação na produtividade da soja no Rio Grande do Sul, utilizando um modelo de Machine Learning (Random Forest). O dashboard oferece uma interface para explorar os dados históricos e os resultados do modelo de forma clara e acessível.

### Objetivos:

* Analisar a relação entre variáveis climáticas e a produtividade da soja.
* Desenvolver um modelo preditivo robusto (Random Forest) para estimar a produtividade da soja.
* Identificar as variáveis de maior influência na produtividade.
* Fornecer uma ferramenta interativa para visualização de dados históricos e desempenho do modelo.

---

## 🚀 Funcionalidades

O dashboard oferece as seguintes funcionalidades:

* **Visão Geral do Modelo**: Exibe métricas chave do modelo Random Forest, como R² e MAPE.
* **Importância das Variáveis**: Um gráfico de barras que mostra a contribuição de cada variável para a previsão da produtividade.
* **Análise de Predições**: Um gráfico de dispersão que compara os valores reais e previstos da produtividade.
* **Dados Históricos Interativos**: Uma tabela filtrável por ano, apresentando dados mensais de temperatura média, precipitação média, área plantada e rendimento médio da produção.
* **Design Responsivo**: Adapta-se a diferentes tamanhos de tela (desktop e mobile).
* **Modo Claro/Escuro**: Opção para alternar entre temas claro e escuro para melhor experiência visual.

---

## 🛠️ Tecnologias Utilizadas

O projeto foi desenvolvido utilizando as seguintes bibliotecas e ferramentas:

* **Python**: Linguagem de programação principal.
* **Dash**: Framework para a construção de aplicações web analíticas.
* **Dash Bootstrap Components (dbc)**: Componentes Bootstrap para um design responsivo e moderno.
* **Dash Iconify**: Biblioteca para fácil integração de ícones.
* **Plotly Graph Objects**: Para criação de gráficos interativos.
* **Pandas**: Manipulação e análise de dados.
* **NumPy**: Suporte para operações numéricas.

---

## ⚙️ Como Executar o Projeto

Para rodar este projeto localmente, siga os passos abaixo:

### Pré-requisitos

Certifique-se de ter o Python 3.8 ou superior instalado.

### 1. Clonar o Repositório

git clone [https://github.com/Wesley-Sousa-Dev/PI3-Site-Random-Forest.git](https://github.com/Wesley-Sousa-Dev/PI3-Site-Random-Forest.git)
cd PI3-Site-Random-Forest

### 2\. Criar e Ativar o Ambiente Virtual (Opcional, mas recomendado)

python -m venv venv
# No Windows
.\venv\Scripts\activate
# No macOS/Linux
source venv/bin/activate

### 3\. Instalar as Dependências

pip install -r requirements.txt

Se o arquivo `requirements.txt` não estiver disponível, você pode criar um com as seguintes dependências:

dash
dash-bootstrap-components
dash-iconify
plotly
pandas
numpy

Ou instale-as manualmente:

pip install dash dash-bootstrap-components dash-iconify plotly pandas numpy

### 4\. Executar o Aplicativo Dash

python main.py

(Assumindo que o arquivo principal da aplicação se chama `app.py`)

Após executar o comando, o dashboard estará disponível em `http://127.0.0.1:8050/` ou na porta especificada pela variável de ambiente `PORT`.

-----

## 📊 Dados Utilizados

Os dados utilizados neste estudo abrangem o período de janeiro de 2015 a fevereiro de 2025 para o estado do Rio Grande do Sul:

  * **Temperatura Média (°C) e Precipitação Média (mm)**: Obtidos da plataforma [NASA POWER](https://power.larc.nasa.gov/data-access-viewer/).
  * **Área Plantada (ha) e Rendimento Médio da Produção (kg/ha)**: Obtidos do [Levantamento Sistemático da Produção Agrícola (LSPA) do IBGE - SIDRA](https://sidra.ibge.gov.br/tabela/6588).

Esses dados foram cruciais para treinar e validar o modelo de Random Forest, permitindo uma análise robusta da influência das condições climáticas na produtividade da soja.

-----

## 💡 Modelo de Random Forest

O modelo preditivo empregado é um **Random Forest Regression**, que apresentou um excelente desempenho na previsão da produtividade da soja.

### Métricas de Desempenho:

  * **R² (Coeficiente de Determinação)**: **0.9870**
      * Indica que aproximadamente 98.7% da variância na produtividade da soja é explicada pelas variáveis de entrada do modelo. Um valor próximo a 1 indica um ajuste quase perfeito.
  * **MAPE (Erro Percentual Absoluto Médio)**: **2.13%**
      * Representa que, em média, as previsões do modelo desviam-se apenas 2.13% dos valores reais, demonstrando alta precisão.

### Parâmetros do Modelo (`best_params`):

  * `n_estimators`: 800 
  * `max_depth`: 10 
  * `min_samples_split`: 5
  * `min_samples_leaf`: 3 
  * `max_features`: 0.5
  * `random_state`: 42 

### Importância das Variáveis:

As variáveis foram ranqueadas pela sua importância no modelo:

1.  **Área plantada (ha)**: 41%
2.  **Temperatura x Precipitação (Interação)**: 21%
3.  **Precipitação Média (mm) - 6 meses**: 16%
4.  **Temperatura Média (°C) - 6 meses**: 13%
5.  **Sazonalidade (Seno)**: 6%
6.  **Sazonalidade (Cosseno)**: 3%

Esses resultados mostram que a **área plantada** é o fator mais influente na produtividade, seguido pelas **interações entre temperatura e precipitação**, e as médias históricas dessas variáveis climáticas.

-----
