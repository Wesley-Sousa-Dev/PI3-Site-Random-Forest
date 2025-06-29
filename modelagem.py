import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_absolute_percentage_error
from scipy.stats import zscore
import seaborn as sns
import joblib

# Criando um DataFrame com dados mensais de temperatura, precipitação, área plantada e rendimento (2015-2025)
data = {
    'mes': list(range(1, 123)), # Índice do mês (de 1 a 122)
    # Temperatura média (°C):
    'temp_media': [23.63, 23.43, 22.27, 19.20, 16.26, 13.59, 13.39, 17.44, 15.73, 17.59, 19.47, 22.60, 23.92, 24.52, 20.63, 20.40, 13.27, 10.24, 12.57, 14.34, 14.40, 17.89, 19.55, 22.81, 23.84, 24.25, 21.36, 18.24, 16.66, 13.93, 14.02, 15.29, 18.52, 18.30, 19.04, 23.33, 23.98, 23.15, 22.10, 21.85, 16.56, 11.76, 12.73, 12.21, 17.56, 18.31, 21.19, 22.74, 24.82, 23.02, 21.35, 20.20, 17.12, 16.19, 11.97, 13.04, 15.52, 19.54, 21.40, 23.07, 24.40, 23.89, 24.30, 18.94, 15.11, 14.35, 11.63, 14.36, 16.23, 18.69, 21.00, 23.50, 24.50, 23.06, 22.63, 19.70, 14.08, 12.55, 11.80, 15.15, 17.14, 18.11, 21.49, 24.06, 27.08, 25.11, 21.53, 18.30, 13.61, 11.29, 15.20, 12.96, 14.29, 17.30, 19.83, 23.91, 26.26, 24.76, 24.79, 19.27, 16.66, 14.56, 13.73, 15.13, 17.62, 18.05, 20.75, 23.28, 23.59, 25.32, 23.37, 20.71, 14.91, 15.52, 11.85, 13.99, 17.41, 19.29, 21.83, 21.47, 24.97, 26.88],
    # Precipitação média (mm):
    'precip_media': [201.91, 90.50, 62.05, 75.15, 126.29, 110.86, 158.67, 82.94, 136.49, 267.48, 156.21, 305.49, 101.91, 114.10, 201.94, 215.71, 79.38, 30.80, 118.08, 119.46, 61.66, 233.78, 127.50, 153.64, 163.43, 150.90, 166.79, 183.33, 284.47, 106.05, 26.83, 166.39, 139.54, 207.34, 102.86, 88.56, 146.15, 69.67,	140.22, 79.41, 95.58, 106.66, 131.27, 130.67, 175.34, 138.34, 152.75, 116.76, 225.22, 92.60, 101.23, 142.88, 194.92, 54.89, 116.54, 80.51, 71.02, 269.97, 130.29, 51.87, 122.75, 62.85,	30.97, 43.30, 143.60, 177.14, 144.13, 65.02, 125.90, 69.37, 59.36, 98.97, 166.06, 91.24, 102.07, 40.71, 126.48, 143.66, 44.12, 73.58, 188.76, 95.42, 67.85, 41.92, 91.87, 92.82, 151.34, 193.13, 160.87, 138.41, 140.68, 106.70, 68.54, 109.66, 48.62, 68.14, 57.89, 79.51, 93.33, 34.16, 133.03, 102.83, 135.74, 69.50, 322.29, 230.83, 260.05, 141.12, 110.53, 83.44, 122.13, 239.37, 293.33, 153.65, 50.20, 94.24, 139.63, 122.33, 85.14, 97.31, 57.37, 109.49],
    # Área plantada (ha):
    'area_plantada': [5200279, 5219684, 5230879, 5230879, 5241776, 5241776, 5263899, 5263899, 5263899, 5263899, 5263899, 5263899, 5471680, 5475537, 5472388, 5472388, 5477005, 5477005, 5474084, 5474084, 5474084, 5474084, 5474084, 5464084, 5463281, 5499742, 5496062, 5496062, 5528233, 5528233, 5541860, 5541860, 5541860, 5541860, 5541860, 5541860, 5674433, 5674433, 5674433, 5679427, 5679427, 5679427, 5679427, 5758133, 5758133, 5709034, 5709034, 5709034, 5805001, 5806922, 5828790, 5828790, 5848766, 5848766, 5843714, 5843714, 5843513, 5843533, 5843533, 5843533, 5930249, 5930249, 5976049, 5976049, 5980832, 5980832, 5981671, 5981671, 5981671, 5980671, 5980671, 5980671, 6075058, 6087229, 6091873, 6091873, 6095677, 6095677, 6107270, 6107270, 6107270, 6107320, 6107320, 6107620, 6362434, 6362588, 6381617, 6381617, 6387985, 6387985, 6387670, 6387670, 6387670, 6387670, 6387670, 6387670, 6628647, 6638744, 6637125, 6637125, 6658472, 6658472, 6651731, 6651731, 6641731, 6640385, 6640385, 6642290, 6716122, 6692798, 6700006, 6700006, 6707273, 6707273, 6708247, 6708247, 6707247, 6707747, 6707747, 6707747, 6817844, 6786139],
    # Rendimento médio da produção (kg/ha):
    'rendimento': [2817, 2850, 2890, 2890, 2976, 2976, 2983, 2983, 2983, 2983, 2983, 2983, 2967, 2942, 2921, 2921, 2985, 2985, 2972, 2972, 2972, 2972, 2972, 2981, 2998, 3031, 3141, 3141, 3361, 3361, 3385, 3385, 3385, 3385, 3385, 3385, 3140, 3140, 3140, 3093, 3093, 3093, 3093, 3104, 3103, 3104, 3104, 3104, 3206, 3209, 3233, 3233, 3194, 3194, 3177, 3177, 3178, 3178, 3178, 3178, 3249, 3249, 2280, 2280, 1883, 1883, 1883, 1883, 1882, 1894, 1894, 1895, 3197, 3206, 3226, 3226, 3324, 3324, 3341, 3341, 3344, 3344, 3344, 3344, 3312, 2069, 1512, 1512, 1472, 1472, 1500, 1500, 1503, 1503, 1503, 1503, 3207, 2758, 2227, 2227, 1949, 1949, 1912, 1912, 1912, 1912, 1912, 1912, 3193, 3247, 3244, 3244, 3045, 3045, 2809, 2809, 2811, 2809, 2809, 2809, 3245, 2792]
}
df = pd.DataFrame(data)

# Criando a coluna de ano com base no mês
df['ano'] = 2015 + (df['mes'] - 1) // 12

# Calculando a média anual do rendimento
df['media_anual'] = df.groupby('ano')['rendimento'].transform('mean')

# Criando a variável de rendimento relativo (rendimento dividido pela média anual)
df['rendimento_relativo'] = df['rendimento'] / df['media_anual']

# Criando variáveis defasadas (lag) para capturar tendências temporais
df['lag_rendimento'] = df['rendimento'].shift(1)
df['lag_rendimento_rel'] = df['lag_rendimento'] / df['media_anual']

# Aplicando o Z-score para remover outliers
cols_zscore = ['rendimento_relativo', 'lag_rendimento_rel']
df_z = df[cols_zscore].dropna()
z = np.abs(zscore(df_z))
df_clean = df.loc[df_z.index][(z < 3).all(axis=1)].copy()

# Feature Engineering: Suavização Temporal (Médias Móveis)
# Criando médias móveis para temperatura e precipitação (janela de 6 meses)
df_clean['temp_movel'] = df_clean['temp_media'].rolling(window=6).mean().fillna(df_clean['temp_media'])
df_clean['precip_movel'] = df_clean['precip_media'].rolling(window=6).mean().fillna(df_clean['precip_media'])

# Feature Engineering: Criação de Features Interativas
# Criando uma variável de interação entre temperatura e precipitação
df_clean['clima_interacao'] = df_clean['temp_movel'] * df_clean['precip_movel']

# Feature Engineering: Codificação Cíclica (Sazonalidade)
# Criando variáveis sazonais usando seno e cosseno para representar o ciclo anual
df_clean['mes_sin'] = np.sin(2 * np.pi * df_clean['mes'] / 12)
df_clean['mes_cos'] = np.cos(2 * np.pi * df_clean['mes'] / 12)

# Definição das variáveis independentes (X) e dependente (y)
X = df_clean[['mes_cos', 'mes_sin', 'temp_movel', 'precip_movel', 'clima_interacao', 'area_plantada']].dropna()
y = df_clean.loc[X.index, 'rendimento_relativo']
media_ano = df_clean.loc[X.index, 'media_anual']

# Divisão dos dados em treino e teste (80% treino, 20% teste)
X_train, X_test, y_train, y_test, media_train, media_test = train_test_split(
    X, y, media_ano, test_size=0.2, random_state=42
)

np.save('indices_teste.npy', X_test.index)  
media_test.to_csv('media_test.csv')

# Criando um pipeline com normalização dos dados e Random Forest Regressor
pipeline = Pipeline([
    ('scaler', StandardScaler()), # Normalização dos dados
    ('rf', RandomForestRegressor( # Modelo de aprendizado de máquina
        n_estimators=800,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=3,
        max_features=0.5,
        random_state=42
    ))
])

# Treinamento do modelo
pipeline.fit(X_train, y_train)

# Previsões relativas → conversão para escala original
y_pred_rel = pipeline.predict(X_test)
y_pred_real = y_pred_rel * media_test
y_test_real = y_test * media_test

# Avaliação do modelo
r2_final = r2_score(y_test_real, y_pred_real)
mape_final = mean_absolute_percentage_error(y_test_real, y_pred_real) * 100

# Exibição dos resultados
print(f"R²: {r2_final:.4f}")
print(f"MAPE: {mape_final:.4f}%")

# Rótulos legíveis para as variáveis explicativas — mais fáceis de entender no gráfico
variaveis_legiveis = [
    'Sazonalidade (Cosseno)',
    'Sazonalidade (Seno)',
    'Temperatura Média (°C)\n(6 meses)',
    'Precipitação Média (mm)\n(6 meses)',
    'Temperatura x Precipitação\n(Interação)',
    'Área Plantada (ha)'
]

# Importância das variáveis no modelo
importancias = pipeline.named_steps['rf'].feature_importances_
variaveis = X.columns

# Gráfico de importância das variáveis
plt.figure(figsize=(8, 5))
sns.barplot(x=importancias, y=variaveis_legiveis, color="#00F020")
plt.title('Importância das Variáveis', fontsize=14)
plt.xlabel('Importância')
plt.ylabel('Variável')
plt.tight_layout()
plt.savefig('grafico_importancia_variaveis.png', dpi=300) # Salvar o gráfico 
plt.show()

# Gráfico de dispersão entre valores reais e previstos
plt.figure(figsize=(6, 6))
sns.scatterplot(x=y_test_real, y=y_pred_real, color="#28a745", s=60, edgecolor='k', alpha=0.7)
plt.plot([y_test_real.min(), y_test_real.max()],
         [y_test_real.min(), y_test_real.max()],
          color="#ff0000", linestyle='--', linewidth=2)
plt.xlabel('Valor Real')
plt.ylabel('Valor Previsto')
plt.title('Dispersão: Valor Real vs Previsto (Teste)')
plt.grid(True)
plt.tight_layout()
plt.savefig('grafico_dispersao_teste.png', dpi=300) # Salvar o gráfico
plt.show()

# Salvar pipeline completo (modelo + scaler)
joblib.dump(pipeline, 'modelo_produtividade_soja.pkl')

# R²: 0.9870
# MAPE: 2.1332%