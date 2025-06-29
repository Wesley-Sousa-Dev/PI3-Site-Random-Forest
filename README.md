# 🌱 Previsão da Produtividade da Soja com Random Forest

Dashboard interativo desenvolvido em Python com **Dash**, aplicando técnicas de **modelagem matemática e computacional** para prever a produtividade da soja no município de Tupanciretã (RS), considerando variáveis climáticas e agrícolas. A aplicação visa orientar estratégias adaptativas frente às mudanças climáticas.

---

## 📋 Funcionalidades Principais

- Visualização da **importância das variáveis** na previsão da produção de soja.
- Comparação entre **valores reais e predições** feitas por modelo Random Forest.
- Filtro interativo por ano para explorar **dados históricos simulados (2018–2025)**.
- Exibição tabular de dados históricos com destaque para **anomalias climáticas** e **altas produtividades**.
- Alternância entre **temas claro e escuro** no painel.

---

## 📊 Variáveis Consideradas

- **Mês**
- **Temperatura Média (°C)**
- **Precipitação (mm)**
- **Área Plantada (ha)**
- **Área Colhida (ha)**
- **Produção (ton)**

---

## ⚙️ Requisitos

- Python 3.x  
- Instale as dependências com:

```bash
pip install -r requirements.txt
```

📄 *Arquivo `requirements.txt` inclui:*  
`dash`, `dash-bootstrap-components`, `dash-iconify`, `plotly`, `pandas`, `numpy`

---

## 🚀 Como Executar

1. Clone este repositório ou baixe os arquivos.
2. No terminal, execute:

```bash
python main.py
```

3. Acesse o dashboard no navegador:

```
http://localhost:8050
```

---

## ✅ Métricas do Modelo

- **Coeficiente de Determinação (R²):** 0.9870
- **Erro Percentual Absoluto Médio (MAPE):** 2.1332%
- **Melhores parâmetros do Random Forest:**
  - `n_estimators`: 800
  - `max_depth`: 10
  - `min_samples_split`: 5
  - `min_samples_leaf`: 3
  - `max_features`: 0.5
  - `random_state`: 42

---

## 🧠 Modelo Utilizado

O modelo de aprendizado de máquina **Random Forest** foi calibrado com dados históricos de clima e produção, realizando predições robustas com alta acurácia. A análise de importância das variáveis permite interpretar **quais fatores mais influenciam a produtividade da soja**.

---

## 📅 Escopo Temporal

- Simulação de dados mensais de **2018 a 2025**
- Baseado em padrões sazonais, ruído estatístico e comportamento climático realista

---

## 🌍 Contribuição ao ODS 13

Este projeto contribui com o **Objetivo de Desenvolvimento Sustentável 13** da ONU (*Ação contra a mudança global do clima*), oferecendo uma solução científica para mitigação de riscos agrícolas decorrentes de alterações climáticas.

---

## 📌 Local de Estudo

**Município de Tupanciretã – Rio Grande do Sul (RS)**  
Foco na análise da produtividade agrícola em nível local com potencial de expansão regional.

---

## 👨‍🔬 Autoria

Projeto acadêmico desenvolvido para análise de dados climáticos e sua correlação com a produção agrícola, com ênfase em aplicações práticas para políticas públicas e planejamento agrícola sustentável.
