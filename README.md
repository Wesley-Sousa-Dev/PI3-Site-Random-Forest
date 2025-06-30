# 🌱 Dashboard de Produtividade da Soja no RS

Este é um dashboard interativo desenvolvido em **Python** com **Dash**, que permite visualizar e analisar a produtividade da soja no **Rio Grande do Sul**. O sistema utiliza um modelo de **Random Forest** para prever a produtividade com base em dados históricos de **temperatura**, **precipitação** e **área plantada**.

---

## 📄 Sobre o Projeto

A produção de soja depende fortemente das condições climáticas. Este projeto visa analisar e prever os efeitos de variações mensais de temperatura e precipitação na produtividade da soja no RS, por meio de Machine Learning.

### 🎯 Objetivos
- 📊 Analisar a relação entre clima e produtividade da soja  
- 🤖 Construir um modelo preditivo (Random Forest) robusto  
- 🔍 Identificar as variáveis com maior influência na produtividade  
- 💻 Fornecer uma interface interativa para explorar os dados e as previsões  

---

## 🚀 Funcionalidades

- ✅ **Visão Geral do Modelo**: Métricas como R² e MAPE  
- 📈 **Importância das Variáveis**: Gráfico de barras com impacto de cada variável  
- 🔄 **Análise de Predições**: Dispersão entre valores reais e previstos  
- 📅 **Dados Históricos**: Tabela interativa por ano com temperatura, precipitação, área plantada e rendimento  
- 📱 **Design Responsivo**: Compatível com desktop e mobile  
- 🌗 **Modo Claro/Escuro**: Alternância entre temas visualmente agradáveis  

---

## 🛠️ Tecnologias Utilizadas

- **Python** 🐍
- **Dash** – Web analytics com Python  
- **Dash Bootstrap Components (dbc)** – Layouts modernos e responsivos  
- **Dash Iconify** – Ícones modernos via biblioteca Iconify  
- **Plotly Graph Objects** – Gráficos interativos  
- **Pandas & NumPy** – Manipulação e análise de dados  

---

## ⚙️ Como Executar o Projeto

### 📌 Pré-requisitos
- Python 3.8 ou superior

### 📥 1. Clonar o Repositório
```bash
git clone https://github.com/Wesley-Sousa-Dev/PI3-Site-Random-Forest.git
cd PI3-Site-Random-Forest
```

### 📦 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

Se `requirements.txt` não estiver presente:
```bash
pip install dash dash-bootstrap-components dash-iconify plotly pandas numpy
```

### ▶️ 3. Executar o Aplicativo
```bash
python main.py
```

Acesse em: [http://127.0.0.1:8050](http://127.0.0.1:8050)

---

## 📊 Dados Utilizados

Período: **Jan/2015 a Fev/2025** – Estado: **Rio Grande do Sul**

- 🌡️ **Temperatura Média (°C)** e **Precipitação Média (mm)**:  
  Fonte: [NASA POWER](https://power.larc.nasa.gov/data-access-viewer/)

- 🌾 **Área Plantada (ha)** e **Rendimento Médio (kg/ha)**:  
  Fonte: [IBGE - SIDRA, Tabela 6588](https://sidra.ibge.gov.br/tabela/6588)

Esses dados foram fundamentais para treinar e validar o modelo Random Forest.

---

## 💡 Modelo de Random Forest

Modelo: **Random Forest Regressor**

### 🔢 Métricas de Desempenho
- **R²**: `0.9870` – 98.7% da variância explicada  
- **MAPE**: `2.13%` – Erro médio percentual muito baixo

### 🧩 Parâmetros do Modelo
- `n_estimators`: 800  
- `max_depth`: 10  
- `min_samples_split`: 5  
- `min_samples_leaf`: 3  
- `max_features`: 0.5  
- `random_state`: 42  

### 📌 Importância das Variáveis
| Variável                                     | Importância |
|---------------------------------------------|-------------|
| Área plantada (ha)                          | **41%**     |
| Temperatura × Precipitação (Interação)      | **21%**     |
| Precipitação Média (mm) - últimos 6 meses   | **16%**     |
| Temperatura Média (°C) - últimos 6 meses    | **13%**     |
| Sazonalidade (Seno)                         | **6%**      |
| Sazonalidade (Cosseno)                      | **3%**      |

A **área plantada** e as **condições climáticas combinadas** são os maiores influenciadores da produtividade.
