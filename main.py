import dash
from dash import dcc, html, dash_table, Input, Output, callback, State
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os

# --- DADOS REAIS (do script de modelagem) ---
data = {
    "mes": list(range(1, 123)),
    "temp_media": [
        23.63,
        23.43,
        22.27,
        19.20,
        16.26,
        13.59,
        13.39,
        17.44,
        15.73,
        17.59,
        19.47,
        22.60,
        23.92,
        24.52,
        20.63,
        20.40,
        13.27,
        10.24,
        12.57,
        14.34,
        14.40,
        17.89,
        19.55,
        22.81,
        23.84,
        24.25,
        21.36,
        18.24,
        16.66,
        13.93,
        14.02,
        15.29,
        18.52,
        18.30,
        19.04,
        23.33,
        23.98,
        23.15,
        22.10,
        21.85,
        16.56,
        11.76,
        12.73,
        12.21,
        17.56,
        18.31,
        21.19,
        22.74,
        24.82,
        23.02,
        21.35,
        20.20,
        17.12,
        16.19,
        11.97,
        13.04,
        15.52,
        19.54,
        21.40,
        23.07,
        24.40,
        23.89,
        24.30,
        18.94,
        15.11,
        14.35,
        11.63,
        14.36,
        16.23,
        18.69,
        21.00,
        23.50,
        24.50,
        23.06,
        22.63,
        19.70,
        14.08,
        12.55,
        11.80,
        15.15,
        17.14,
        18.11,
        21.49,
        24.06,
        27.08,
        25.11,
        21.53,
        18.30,
        13.61,
        11.29,
        15.20,
        12.96,
        14.29,
        17.30,
        19.83,
        23.91,
        26.26,
        24.76,
        24.79,
        19.27,
        16.66,
        14.56,
        13.73,
        15.13,
        17.62,
        18.05,
        20.75,
        23.28,
        23.59,
        25.32,
        23.37,
        20.71,
        14.91,
        15.52,
        11.85,
        13.99,
        17.41,
        19.29,
        21.83,
        21.47,
        24.97,
        26.88,
    ],
    "precip_media": [
        201.91,
        90.50,
        62.05,
        75.15,
        126.29,
        110.86,
        158.67,
        82.94,
        136.49,
        267.48,
        156.21,
        305.49,
        101.91,
        114.10,
        201.94,
        215.71,
        79.38,
        30.80,
        118.08,
        119.46,
        61.66,
        233.78,
        127.50,
        153.64,
        163.43,
        150.90,
        166.79,
        183.33,
        284.47,
        106.05,
        26.83,
        166.39,
        139.54,
        207.34,
        102.86,
        88.56,
        146.15,
        69.67,
        140.22,
        79.41,
        95.58,
        106.66,
        131.27,
        130.67,
        175.34,
        138.34,
        152.75,
        116.76,
        225.22,
        92.60,
        101.23,
        142.88,
        194.92,
        54.89,
        116.54,
        80.51,
        71.02,
        269.97,
        130.29,
        51.87,
        122.75,
        62.85,
        30.97,
        43.30,
        143.60,
        177.14,
        144.13,
        65.02,
        125.90,
        69.37,
        59.36,
        98.97,
        166.06,
        91.24,
        102.07,
        40.71,
        126.48,
        143.66,
        44.12,
        73.58,
        188.76,
        95.42,
        67.85,
        41.92,
        91.87,
        92.82,
        151.34,
        193.13,
        160.87,
        138.41,
        140.68,
        106.70,
        68.54,
        109.66,
        48.62,
        68.14,
        57.89,
        79.51,
        93.33,
        34.16,
        133.03,
        102.83,
        135.74,
        69.50,
        322.29,
        230.83,
        260.05,
        141.12,
        110.53,
        83.44,
        122.13,
        239.37,
        293.33,
        153.65,
        50.20,
        94.24,
        139.63,
        122.33,
        85.14,
        97.31,
        57.37,
        109.49,
    ],
    "area_plantada": [
        5200279,
        5219684,
        5230879,
        5230879,
        5241776,
        5241776,
        5263899,
        5263899,
        5263899,
        5263899,
        5263899,
        5263899,
        5471680,
        5475537,
        5472388,
        5472388,
        5477005,
        5477005,
        5474084,
        5474084,
        5474084,
        5474084,
        5474084,
        5464084,
        5463281,
        5499742,
        5496062,
        5496062,
        5528233,
        5528233,
        5541860,
        5541860,
        5541860,
        5541860,
        5541860,
        5541860,
        5674433,
        5674433,
        5674433,
        5679427,
        5679427,
        5679427,
        5679427,
        5758133,
        5758133,
        5709034,
        5709034,
        5709034,
        5805001,
        5806922,
        5828790,
        5828790,
        5848766,
        5848766,
        5843714,
        5843714,
        5843513,
        5843533,
        5843533,
        5843533,
        5930249,
        5930249,
        5976049,
        5976049,
        5980832,
        5980832,
        5981671,
        5981671,
        5981671,
        5980671,
        5980671,
        5980671,
        6075058,
        6087229,
        6091873,
        6091873,
        6095677,
        6095677,
        6107270,
        6107270,
        6107270,
        6107320,
        6107320,
        6107620,
        6362434,
        6362588,
        6381617,
        6381617,
        6387985,
        6387985,
        6387670,
        6387670,
        6387670,
        6387670,
        6387670,
        6387670,
        6628647,
        6638744,
        6637125,
        6637125,
        6658472,
        6658472,
        6651731,
        6651731,
        6641731,
        6640385,
        6640385,
        6642290,
        6716122,
        6692798,
        6700006,
        6700006,
        6707273,
        6707273,
        6708247,
        6708247,
        6707247,
        6707747,
        6707747,
        6707747,
        6817844,
        6786139,
    ],
    "rendimento": [
        2817,
        2850,
        2890,
        2890,
        2976,
        2976,
        2983,
        2983,
        2983,
        2983,
        2983,
        2983,
        2967,
        2942,
        2921,
        2921,
        2985,
        2985,
        2972,
        2972,
        2972,
        2972,
        2972,
        2981,
        2998,
        3031,
        3141,
        3141,
        3361,
        3361,
        3385,
        3385,
        3385,
        3385,
        3385,
        3385,
        3140,
        3140,
        3140,
        3093,
        3093,
        3093,
        3093,
        3104,
        3103,
        3104,
        3104,
        3104,
        3206,
        3209,
        3233,
        3233,
        3194,
        3194,
        3177,
        3177,
        3178,
        3178,
        3178,
        3178,
        3249,
        3249,
        2280,
        2280,
        1883,
        1883,
        1883,
        1883,
        1882,
        1894,
        1894,
        1895,
        3197,
        3206,
        3226,
        3226,
        3324,
        3324,
        3341,
        3341,
        3344,
        3344,
        3344,
        3344,
        3312,
        2069,
        1512,
        1512,
        1472,
        1472,
        1500,
        1500,
        1503,
        1503,
        1503,
        1503,
        3207,
        2758,
        2227,
        2227,
        1949,
        1949,
        1912,
        1912,
        1912,
        1912,
        1912,
        1912,
        3193,
        3247,
        3244,
        3244,
        3045,
        3045,
        2809,
        2809,
        2811,
        2809,
        2809,
        2809,
        3245,
        2792,
    ],
}

# Criar DataFrame real
df = pd.DataFrame(data)


# Adicionar colunas de ano e mês
df["ano"] = 2015 + (df["mes"] - 1) // 12
df["mes_num"] = ((df["mes"] - 1) % 12) + 1
meses_nome = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]
df["mes_nome"] = df["mes_num"].apply(lambda x: meses_nome[x - 1])

# Preparar DataFrame para a tabela do dashboard
df_historico = df.rename(
    columns={
        "ano": "Ano",
        "mes_nome": "Mês",
        "temp_media": "Temperatura",
        "precip_media": "Precipitação",
        "area_plantada": "Área Plantada",
        "rendimento": "Produção",
    }
)[["Ano", "Mês", "Temperatura", "Precipitação", "Área Plantada", "Produção"]]

# Adicionar coluna Área Colhida (assumindo 95% da área plantada como exemplo)
df_historico["Área Colhida"] = (df_historico["Área Plantada"] * 0.95).astype(int)

# Reordenar colunas
df_historico = df_historico[
    [
        "Ano",
        "Mês",
        "Temperatura",
        "Precipitação",
        "Área Plantada",
        "Área Colhida",
        "Produção",
    ]
]

# Lista de anos disponíveis
anos = sorted(df_historico["Ano"].unique())

dark_theme_bg = "linear-gradient(135deg, #1a1d24 0%, #2a2e3a 100%)"
light_theme_bg = "linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)"

# --- DADOS DO MODELO (ATUALIZADOS COM DADOS REAIS DO TESTE) ---
model_data = {
    "r2": 0.9870,
    "mape": 2.1332,
    "best_params": {
        "n_estimators": 800,
        "max_depth": 10,
        "min_samples_split": 5,
        "min_samples_leaf": 3,
        "max_features": 0.5,
        "random_state": 42,
    },
    "feature_names": [
        "Sazonalidade (Cosseno)",
        "Sazonalidade (Seno)",
        "Temperatura Média (°C) (6 meses)",
        "Precipitação Média (mm) (6 meses)",
        "Temperatura x Precipitação (Interação)",
        "Área Plantada (ha)",
    ],
    "feature_importances": np.array([0.03, 0.06, 0.13, 0.16, 0.21, 0.41]),
    "y_test_real": np.array(
        [
            1472,
            2976,
            3104,
            3093,
            2983,
            3206,
            2811,
            3140,
            3206,
            2967,
            3104,
            3141,
            1949,
            3177,
            2972,
            2850,
            3178,
            1500,
            2809,
            1912,
            2227,
            1503,
            1894,
            2942,
        ]
    ),
    "y_pred_real": np.array(
        [
            1576.7,
            2970.68,
            3104.65,
            3118.74,
            2935.95,
            3193.74,
            2816.04,
            3112.79,
            3238.87,
            2929.00,
            3112.30,
            3245.58,
            2178.71,
            3200.44,
            2967.98,
            2907.51,
            3195.27,
            1538.74,
            2822.85,
            2007.44,
            2193.69,
            1552.73,
            2006.69,
            2944.96,
        ]
    ),
}


# --- PREPARAÇÃO DOS DADOS ---
sorted_indices = np.argsort(model_data["feature_importances"])
sorted_feature_names = [model_data["feature_names"][i] for i in sorted_indices]
sorted_feature_importances = model_data["feature_importances"][sorted_indices]

# --- INICIALIZAÇÃO DA APLICAÇÃO ---
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no",
        },
        {
            "name": "description",
            "content": "Dashboard de Produtividade da Soja no RS usando Random Forest",
        },
        {"name": "theme-color", "content": "#28a745"},
    ],
)
app.title = "Random Forest ML Dashboard"

cor_detalhes = "#28a745"


# --- FUNÇÃO PARA DETECTAR DISPOSITIVO MÓVEL ---
def get_responsive_config():
    return {
        "displayModeBar": False,
        "responsive": True,
        "toImageButtonOptions": {
            "format": "png",
            "filename": "grafico",
            "height": 500,
            "width": 700,
            "scale": 1,
        },
    }


# --- FUNÇÕES PARA CRIAR GRÁFICOS ---
def create_feature_importance_graph(theme="light", is_mobile=False):
    if theme == "dark":
        bg_color = "#1a1d24"
        text_color = "#e0e0e0"
        bar_color = "#00F020"
    else:
        bg_color = "rgba(0,0,0,0)"
        text_color = "#2d5016"
        bar_color = "#00F020"

    feature_names = np.array(model_data["feature_names"])
    feature_importances = np.array(model_data["feature_importances"])
    order = np.argsort(feature_importances)
    feature_names = feature_names[order][::-1]
    feature_importances = feature_importances[order][::-1]

    fig = go.Figure(
        go.Bar(
            x=feature_importances,
            y=feature_names,
            orientation="h",
            marker=dict(color=bar_color, line=dict(color="#000000", width=1)),
            hovertemplate="<b>%{y}</b><br>Importância: %{x:.1%}<extra></extra>",
        )
    )

    height = 300 if is_mobile else 400
    margin_left = 100 if is_mobile else 120
    title_size = 16 if is_mobile else 20

    fig.update_layout(
        title={
            "text": "Importância das Variáveis",
            "x": 0.5,
            "xanchor": "center",
            "font": {
                "size": title_size,
                "family": "Arial Black",
                "color": cor_detalhes,
            },
        },
        xaxis_title="Importância",
        yaxis_title="Variável",
        height=height,
        margin=dict(l=margin_left, r=30 if is_mobile else 50, t=60, b=50),
        showlegend=False,
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color, size=10 if is_mobile else 12),
        xaxis=dict(tickfont=dict(size=9 if is_mobile else 12)),
        yaxis=dict(tickfont=dict(size=9 if is_mobile else 12)),
    )
    return fig


def create_predictions_graph(theme="light", is_mobile=False):
    """Cria o gráfico de dispersão igual ao do script original"""
    if theme == "dark":
        bg_color = "#1a1d24"
        text_color = "#e0e0e0"
        grid_color = "#444444"
    else:
        bg_color = "rgba(0,0,0,0)"
        text_color = "#2d5016"
        grid_color = "#e0e0e0"

    fig = go.Figure()

    # Pontos de dispersão (igual ao seaborn.scatterplot do original)
    fig.add_trace(
        go.Scatter(
            x=model_data["y_test_real"],
            y=model_data["y_pred_real"],
            mode="markers",
            marker=dict(
                size=12 if is_mobile else 16,
                color="#28a745",  # Cor verde igual ao original
                line=dict(width=1, color="black"),  # Borda preta igual ao original
                opacity=0.7,  # Alpha igual ao original
            ),
            text=[
                f"Real: {real:,.0f} kg/ha".replace(",", ".")
                + f"<br>Previsto: {pred:,.0f} kg/ha".replace(",", ".")
                + f"<br>Erro: {abs(real-pred):,.0f} kg/ha".replace(",", ".")
                for real, pred in zip(
                    model_data["y_test_real"], model_data["y_pred_real"]
                )
            ],
            hovertemplate="<b>Predição</b><br>%{text}<extra></extra>",
            name="Predições",
        )
    )

    # Linha de referência diagonal (igual ao matplotlib.plot do original)
    min_val = min(min(model_data["y_test_real"]), min(model_data["y_pred_real"]))
    max_val = max(max(model_data["y_test_real"]), max(model_data["y_pred_real"]))

    fig.add_trace(
        go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode="lines",
            line=dict(
                dash="dash",  # Linha tracejada igual ao original
                width=2,
                color="#ff0000",  # Cor vermelha igual ao original
            ),
            name="Linha Perfeita",
            hovertemplate="Predição Perfeita<extra></extra>",
        )
    )

    height = 350 if is_mobile else 400
    title_size = 16 if is_mobile else 20

    fig.update_layout(
        title={
            "text": "Dispersão: Valor Real vs Previsto (Teste)",  # Título igual ao original
            "x": 0.5,
            "xanchor": "center",
            "font": {
                "size": title_size,
                "family": "Arial Black",
                "color": cor_detalhes,
            },
        },
        xaxis_title="Valor Real",  # Igual ao original
        yaxis_title="Valor Previsto",  # Igual ao original
        height=height,
        margin=dict(l=50, r=30, t=60, b=50),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color, size=10 if is_mobile else 12),
        # Grid igual ao original (plt.grid(True))
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor=grid_color,
            tickfont=dict(size=9 if is_mobile else 12),
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor=grid_color,
            tickfont=dict(size=9 if is_mobile else 12),
        ),
        showlegend=False,  # Sem legenda igual ao original
    )
    return fig


def create_metric_card(
    title,
    value,
    icon,
    color_class="success",
    subtitle=None,
    theme="light",
    is_mobile=False,
):
    if theme == "dark":
        card_bg = dark_theme_bg
        text_color = "#e0e0e0"
        subtitle_color = "#a0a0a0"
    else:
        card_bg = light_theme_bg
        text_color = "#333333"
        subtitle_color = "#6c757d"

    icon_size = 35 if is_mobile else 50
    value_size = "2rem" if is_mobile else "2.5rem"
    title_size = "0.9rem" if is_mobile else "1.1rem"

    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.Div(
                        [
                            DashIconify(
                                icon=icon,
                                width=icon_size,
                                className=f"text-{color_class} mb-2",
                            ),
                            html.H2(
                                value,
                                className=f"text-{color_class} fw-bold mb-1",
                                style={"fontSize": value_size},
                            ),
                            html.P(
                                title,
                                className="fw-bold mb-0",
                                style={"fontSize": title_size, "color": text_color},
                            ),
                            (
                                html.Small(
                                    subtitle,
                                    style={
                                        "color": subtitle_color,
                                        "fontSize": (
                                            "0.8rem" if is_mobile else "0.875rem"
                                        ),
                                    },
                                )
                                if subtitle
                                else None
                            ),
                        ],
                        className="text-center",
                    )
                ],
                style={"padding": "1rem" if is_mobile else "1.5rem"},
            )
        ],
        className="h-100 shadow border-0",
        style={
            "background": card_bg,
            "border-left": f"5px solid {cor_detalhes} !important",
        },
    )


# --- STORE PARA DETECTAR DISPOSITIVO MÓVEL ---
app.clientside_callback(
    """      
    function(pathname) {      
        return window.innerWidth <= 768;      
    }      
    """,
    Output("mobile-store", "data"),
    Input("url", "pathname"),
)

# --- LAYOUT PRINCIPAL ---
app.layout = html.Div(
    id="main-container",
    children=[
        dcc.Location(id="url", refresh=False),
        dcc.Store(id="theme-store", data="light"),
        dcc.Store(id="selected-year-store", data=2023),
        dcc.Store(id="mobile-store", data=False),
        # Barra superior mobile
        html.Div(
            id="mobile-navbar",
            children=[
                dbc.Navbar(
                    dbc.Container(
                        [
                            html.Div(
                                [
                                    DashIconify(
                                        icon="fa:line-chart",
                                        width=24,
                                        className="me-2",
                                        style={"color": cor_detalhes},
                                    ),
                                    html.Span(
                                        "Produtividade da Soja no RS",
                                        className="navbar-brand mb-0 h1 fw-bold",
                                        style={
                                            "color": cor_detalhes,
                                            "fontSize": "1.2rem",
                                        },
                                    ),
                                ],
                                className="d-flex align-items-center",
                            ),
                            html.Button(
                                id="theme-toggle-mobile",
                                children=[html.Span("☀️", id="theme-icon-mobile")],
                                style={
                                    "background": "transparent",
                                    "border": f"1px solid {cor_detalhes}",
                                    "borderRadius": "50%",
                                    "cursor": "pointer",
                                    "fontSize": "1.2rem",
                                    "height": "40px",
                                    "width": "40px",
                                    "display": "flex",
                                    "alignItems": "center",
                                    "justifyContent": "center",
                                    "transition": "all 0.3s ease",
                                },
                            ),
                        ],
                        fluid=True,
                        className="px-3 d-flex justify-content-between align-items-center",
                    ),
                    className="shadow-sm",
                )
            ],
            className="d-block d-md-none",
        ),
        dbc.Container(
            [
                # Header com botão de tema
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H1(
                                                    [
                                                        DashIconify(
                                                            icon="fa:line-chart",
                                                            width=40,
                                                            className="me-2 d-none d-md-inline",
                                                            style={
                                                                "color": cor_detalhes
                                                            },
                                                        ),
                                                        html.Span(
                                                            "Produtividade da Soja no RS",
                                                            id="main-title",
                                                        ),
                                                    ],
                                                    className="fw-bold text-center mb-0",
                                                    style={"color": cor_detalhes},
                                                    id="title-container",
                                                ),
                                                html.P(
                                                    id="subtitle-text",
                                                    className="lead text-center mt-3",
                                                ),
                                            ],
                                            style={"position": "relative"},
                                        ),
                                        html.Button(
                                            id="theme-toggle",
                                            children=[html.Span("☀️", id="theme-icon")],
                                            className="d-none d-md-flex",
                                            style={
                                                "position": "absolute",
                                                "top": "10px",
                                                "right": "10px",
                                                "height": "50px",
                                                "width": "50px",
                                                "background": "transparent",
                                                "border": f"1px solid {cor_detalhes}",
                                                "borderRadius": "50%",
                                                "cursor": "pointer",
                                                "fontSize": "1.5rem",
                                                "display": "flex",
                                                "alignItems": "center",
                                                "justifyContent": "center",
                                                "transition": "all 0.3s ease",
                                                "zIndex": "1000",
                                            },
                                        ),
                                    ],
                                    className="text-center py-4 py-md-5",
                                    style={"position": "relative"},
                                )
                            ]
                        )
                    ],
                    className="mb-4 mb-md-5 d-block d-md-block",
                ),
                # Métricas Principais
                html.Div(
                    id="metrics-container",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    [html.Div(id="metric-card-1")],
                                    xs=12,
                                    sm=6,
                                    className="mb-3 mb-sm-0",
                                ),
                                dbc.Col([html.Div(id="metric-card-2")], xs=12, sm=6),
                            ],
                            className="mb-4 mb-md-5",
                        ),
                    ],
                ),
                # Gráficos Principais
                html.Div(
                    id="graphs-container",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    [html.Div(id="feature-importance-card")],
                                    xs=12,
                                    lg=6,
                                    className="mb-4 mb-lg-0",
                                ),
                                dbc.Col([html.Div(id="predictions-card")], xs=12, lg=6),
                            ],
                            className="mb-4 mb-md-5",
                        ),
                    ],
                ),
                # Filtro de Ano
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        dbc.Label(
                                            "Filtrar por Ano:",
                                            html_for="year-filter",
                                            id="year-filter-label",
                                        ),
                                        dbc.Select(
                                            id="year-filter",
                                            options=[
                                                {"label": f"📅 {ano}", "value": ano}
                                                for ano in anos
                                            ],
                                            value=2023,
                                            className="fw-bold",
                                        ),
                                    ],
                                    id="year-filter-container",
                                    className="mb-4",
                                )
                            ],
                            xs=12,
                            md=6,
                            lg=4,
                        )
                    ]
                ),
                # Tabela de Dados Históricos
                html.Div(
                    id="table-section",
                    children=[
                        dbc.Row(
                            [dbc.Col([html.Div(id="data-table-card")], xs=12)],
                            className="mb-4 mb-md-5",
                        ),
                    ],
                ),
                # Footer
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Hr(id="footer-hr"),
                                html.P(
                                    [
                                        "🚀 Dashboard criado por ",
                                        html.A(
                                            "FLASHBYTE",
                                            href="https://github.com/Wesley-Sousa-Dev/PI3-Site-Random-Forest",
                                            target="_blank",
                                            className="text-decoration-none fw-bold",
                                            style={"color": cor_detalhes},
                                        ),
                                        html.Br(className="d-md-none"),
                                        html.Span(
                                            " | Modelo: Random Forest 🌱",
                                            className="d-none d-md-inline",
                                        ),
                                        html.Span(
                                            "Random Forest 🌱", className="d-md-none"
                                        ),
                                    ],
                                    id="footer-text",
                                    className="text-center",
                                ),
                            ]
                        )
                    ]
                ),
            ],
            fluid=True,
            className="px-3 px-md-4",
        ),
    ],
    style={"overflowX": "hidden", "width": "100%", "maxWidth": "100vw"},
)


# --- CALLBACKS ---
@callback(
    Output("theme-store", "data"),
    [Input("theme-toggle", "n_clicks"), Input("theme-toggle-mobile", "n_clicks")],
    State("theme-store", "data"),
)
def toggle_theme(n_clicks_desktop, n_clicks_mobile, current_theme):
    total_clicks = (n_clicks_desktop or 0) + (n_clicks_mobile or 0)
    if total_clicks == 0:
        return current_theme
    return "dark" if current_theme == "light" else "light"


@callback(Output("selected-year-store", "data"), Input("year-filter", "value"))
def update_selected_year(selected_year):
    return selected_year


@callback(
    [
        Output("main-container", "style"),
        Output("mobile-navbar", "children"),
        Output("subtitle-text", "children"),
        Output("subtitle-text", "style"),
        Output("footer-text", "style"),
        Output("footer-hr", "style"),
        Output("theme-icon", "children"),
        Output("theme-icon-mobile", "children"),
        Output("metric-card-1", "children"),
        Output("metric-card-2", "children"),
        Output("feature-importance-card", "children"),
        Output("predictions-card", "children"),
        Output("year-filter-container", "style"),
        Output("year-filter-label", "style"),
        Output("year-filter", "style"),
        Output("title-container", "style"),
    ],
    [Input("theme-store", "data"), Input("mobile-store", "data")],
)
def update_theme(theme, is_mobile):
    if theme == "dark":
        background_color = "#0e1117"
        card_color = "#1a1d24"
        text_color = "#e0e0e0"
        subtitle_color = "#a0a0a0"
        shadow = "0 4px 8px rgba(0, 0, 0, 0.3)"
        theme_icon = "🌙"
        navbar_bg = dark_theme_bg
    else:
        background_color = "#fafafa"
        card_color = "#ffffff"
        text_color = "#333333"
        subtitle_color = "#6c757d"
        shadow = "0 4px 8px rgba(0, 0, 0, 0.1)"
        theme_icon = "☀️"
        navbar_bg = light_theme_bg

    title_size = "1.8rem" if is_mobile else "3rem"
    subtitle_size = "1rem" if is_mobile else "1.3rem"
    footer_size = "0.9rem" if is_mobile else "1.1rem"

    main_style = {
        "backgroundColor": background_color,
        "color": text_color,
        "minHeight": "100vh",
        "transition": "all 0.3s ease",
        "overflowX": "hidden",
        "width": "100%",
        "maxWidth": "100vw",
        "paddingTop": "56px" if is_mobile else "0",
    }

    mobile_navbar_children = [
        dbc.Navbar(
            dbc.Container(
                [
                    html.Div(
                        [
                            DashIconify(
                                icon="fa:line-chart",
                                width=24,
                                className="me-2",
                                style={"color": cor_detalhes},
                            ),
                            html.Span(
                                "Produtividade da Soja no RS",
                                className="navbar-brand mb-0 h1 fw-bold",
                                style={"color": cor_detalhes, "fontSize": "1.2rem"},
                            ),
                        ],
                        className="d-flex align-items-center",
                    ),
                    html.Button(
                        id="theme-toggle-mobile",
                        children=[html.Span(theme_icon, id="theme-icon-mobile")],
                        style={
                            "background": "transparent",
                            "border": f"1px solid {cor_detalhes}",
                            "borderRadius": "50%",
                            "cursor": "pointer",
                            "fontSize": "1.2rem",
                            "height": "40px",
                            "width": "40px",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "transition": "all 0.3s ease",
                        },
                    ),
                ],
                fluid=True,
                className="px-3 d-flex justify-content-between align-items-center",
            ),
            className="shadow-sm",
            style={
                "minHeight": "56px",
                "position": "fixed",
                "top": "0",
                "left": "0",
                "right": "0",
                "zIndex": "1030",
                "background": navbar_bg,
                "borderBottom": f"3px solid {cor_detalhes}",
            },
        )
    ]

    subtitle_text = (
        "Modelagem com Random Forest usando dados climáticos de 2015-2025 para previsões de produtividade."
        if is_mobile
        else "Modelagem computacional da produtividade da soja em função de variações mensais de temperatura e precipitação, entre janeiro de 2015 e fevereiro de 2025, no estado do Rio Grande do Sul. Utilizou-se o modelo Random Forest para a modelagem, com o intuito de quantificar e prever o impacto dessas variações climáticas sobre a produtividade da soja."
    )

    subtitle_style = {"fontSize": subtitle_size, "color": subtitle_color}
    footer_text_style = {"fontSize": footer_size, "color": subtitle_color}
    footer_hr_style = {"border-color": cor_detalhes, "border-width": "2px"}
    title_container_style = {"fontSize": title_size, "color": cor_detalhes}

    metric_card_1 = create_metric_card(
        "Coeficiente R²",
        f"{model_data['r2']:.4f}".replace(".", ","),
        "fa:line-chart",
        "success",
        "Qualidade do ajuste",
        theme,
        is_mobile,
    )
    metric_card_2 = create_metric_card(
        "MAPE",
        f"{model_data['mape']:.2f}%".replace(".", ","),
        "fa:percent",
        "success",
        "Erro percentual médio",
        theme,
        is_mobile,
    )

    card_header_style = {
        "background": dark_theme_bg if theme == "dark" else light_theme_bg,
        "border-bottom": f"3px solid {cor_detalhes}",
        "padding": "0.75rem 1rem" if is_mobile else "1rem 1.25rem",
    }

    feature_importance_card = dbc.Card(
        [
            dbc.CardHeader(
                [
                    html.H5(
                        "Gráfico de Barras: Análise das Variáveis do Modelo",
                        className="mb-0 fw-bold",
                        style={
                            "color": cor_detalhes,
                            "fontSize": "1rem" if is_mobile else "1.25rem",
                        },
                    )
                ],
                style=card_header_style,
            ),
            dbc.CardBody(
                [
                    dcc.Graph(
                        id="feature-importance-graph",
                        figure=create_feature_importance_graph(theme, is_mobile),
                        config=get_responsive_config(),
                    )
                ],
                style={
                    "backgroundColor": card_color,
                    "padding": "0.75rem" if is_mobile else "1rem",
                },
            ),
        ],
        className="shadow border-0 h-100",
        style={"backgroundColor": card_color},
    )

    predictions_card = dbc.Card(
        [
            dbc.CardHeader(
                [
                    html.H5(
                        "Gráfico de Dispersão: Análise de Predições",
                        className="mb-0 fw-bold",
                        style={
                            "color": cor_detalhes,
                            "fontSize": "1rem" if is_mobile else "1.25rem",
                        },
                    )
                ],
                style=card_header_style,
            ),
            dbc.CardBody(
                [
                    dcc.Graph(
                        id="predictions-vs-actual-graph",
                        figure=create_predictions_graph(theme, is_mobile),
                        config=get_responsive_config(),
                    )
                ],
                style={
                    "backgroundColor": card_color,
                    "padding": "0.75rem" if is_mobile else "1rem",
                },
            ),
        ],
        className="shadow border-0 h-100",
        style={"backgroundColor": card_color},
    )

    year_filter_container_style = {
        "background": card_color,
        "padding": "15px",
        "borderRadius": "8px",
        "boxShadow": shadow,
        "transition": "all 0.3s ease",
    }
    year_filter_label_style = {
        "color": text_color,
        "fontWeight": "bold",
        "marginBottom": "8px",
        "fontSize": "1rem" if is_mobile else "1.1rem",
    }
    year_filter_select_style = {
        "border": f"2px solid {cor_detalhes}",
        "border-radius": "8px",
        "backgroundColor": card_color,
        "color": text_color,
        "fontWeight": "bold",
        "fontSize": "1rem" if is_mobile else "1.1rem",
        "transition": "all 0.3s ease",
    }

    return (
        main_style,
        mobile_navbar_children,
        subtitle_text,
        subtitle_style,
        footer_text_style,
        footer_hr_style,
        theme_icon,
        theme_icon,
        metric_card_1,
        metric_card_2,
        feature_importance_card,
        predictions_card,
        year_filter_container_style,
        year_filter_label_style,
        year_filter_select_style,
        title_container_style,
    )


@callback(
    Output("data-table-card", "children"),
    [
        Input("selected-year-store", "data"),
        Input("theme-store", "data"),
        Input("mobile-store", "data"),
    ],
)
def update_table(selected_year, theme, is_mobile):
    if theme == "dark":
        card_color = "#1a1d24"
        text_color = "#e0e0e0"
        table_cell_bg = "#141920"
        table_cell_color = "#e0e0e0"
        table_row_even = "#1a1d24"
        table_header_bg = cor_detalhes
    else:
        card_color = "#ffffff"
        text_color = "#333333"
        table_cell_bg = "#ffffff"
        table_cell_color = "#333333"
        table_row_even = "#f9f9f9"
        table_header_bg = cor_detalhes

    filtered_data = df_historico[df_historico["Ano"] == int(selected_year)].copy()

    if filtered_data.empty:
        return dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4("Nenhum dado encontrado", className="text-center"),
                        html.P(
                            f"Não há dados disponíveis para o ano {selected_year}.",
                            className="text-center",
                        ),
                    ]
                )
            ]
        )

    display_data = filtered_data.drop("Ano", axis=1)

    cell_padding = "8px" if is_mobile else "15px"
    font_size = "12px" if is_mobile else "14px"
    header_font_size = "13px" if is_mobile else "15px"

    columns = [
        {"name": "Mês", "id": "Mês", "type": "text"},
        {
            "name": "Temp (°C)" if is_mobile else "Temperatura (°C)",
            "id": "Temperatura",
            "type": "numeric",
            "format": {"specifier": ".1f"},
        },
        {
            "name": "Precip (mm)" if is_mobile else "Precipitação (mm)",
            "id": "Precipitação",
            "type": "numeric",
            "format": {"specifier": ".1f"},
        },
        {
            "name": "Á. Plant (ha)" if is_mobile else "Área Plantada (ha)",
            "id": "Área Plantada",
            "type": "numeric",
            "format": {"specifier": ",.0f"},
        },
        {
            "name": "Á. Colh (ha)" if is_mobile else "Área Colhida (ha)",
            "id": "Área Colhida",
            "type": "numeric",
            "format": {"specifier": ",.0f"},
        },
        {
            "name": "Prod (kg/ha)" if is_mobile else "Produção (kg/ha)",
            "id": "Produção",
            "type": "numeric",
            "format": {"specifier": ",.0f"},
        },
    ]

    return dbc.Card(
        [
            dbc.CardHeader(
                [
                    html.H4(
                        [
                            DashIconify(
                                icon="fa:table",
                                width=25 if is_mobile else 30,
                                className="me-2",
                                style={"color": cor_detalhes},
                            ),
                            (
                                "Dados Históricos"
                                if is_mobile
                                else "Dados Históricos por Ano"
                            ),
                        ],
                        className="mb-0 fw-bold",
                        style={
                            "color": cor_detalhes,
                            "fontSize": "1.1rem" if is_mobile else "1.5rem",
                        },
                    )
                ],
                style={
                    "background": dark_theme_bg if theme == "dark" else light_theme_bg,
                    "border-bottom": f"3px solid {cor_detalhes}",
                    "padding": "0.75rem 1rem" if is_mobile else "1rem 1.25rem",
                },
            ),
            dbc.CardBody(
                [
                    html.Div(
                        [
                            dash_table.DataTable(
                                data=display_data.to_dict("records"),
                                columns=columns,
                                style_table={"overflowX": "auto", "minWidth": "100%"},
                                style_cell={
                                    "textAlign": "center",
                                    "padding": cell_padding,
                                    "fontFamily": "Arial",
                                    "fontSize": font_size,
                                    "border": f"1px solid {cor_detalhes}",
                                    "backgroundColor": table_cell_bg,
                                    "color": table_cell_color,
                                    "whiteSpace": "normal" if is_mobile else "nowrap",
                                    "height": "auto",
                                    "minWidth": "80px" if is_mobile else "100px",
                                },
                                style_header={
                                    "backgroundColor": table_header_bg,
                                    "color": "white",
                                    "fontWeight": "bold",
                                    "fontSize": header_font_size,
                                    "border": f"1px solid {cor_detalhes}",
                                    "textAlign": "center",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                },
                                style_data_conditional=[
                                    {
                                        "if": {"row_index": "odd"},
                                        "backgroundColor": table_row_even,
                                    },
                                    {
                                        "if": {
                                            "column_id": "Temperatura",
                                            "filter_query": "{Temperatura} > 28",
                                        },
                                        "backgroundColor": "rgba(255, 193, 193, 0.7)",
                                        "color": "black",
                                        "fontWeight": "bold",
                                    },
                                    {
                                        "if": {
                                            "column_id": "Precipitação",
                                            "filter_query": "{Precipitação} > 200",
                                        },
                                        "backgroundColor": "rgba(173, 216, 230, 0.7)",
                                        "color": "black",
                                        "fontWeight": "bold",
                                    },
                                    {
                                        "if": {
                                            "column_id": "Produção",
                                            "filter_query": "{Produção} > 2800",
                                        },
                                        "backgroundColor": "rgba(144, 238, 144, 0.8)",
                                        "color": "black",
                                        "fontWeight": "bold",
                                    },
                                ],
                                style_cell_conditional=[
                                    {
                                        "if": {"column_id": "Mês"},
                                        "fontWeight": "bold",
                                        "backgroundColor": (
                                            f"rgba(40, 167, 69, 0.05)"
                                            if theme == "light"
                                            else f"rgba(40, 167, 69, 0.15)"
                                        ),
                                        "minWidth": "70px" if is_mobile else "100px",
                                    },
                                ],
                                page_size=12,
                                sort_action="native",
                                filter_action="native" if not is_mobile else "none",
                            )
                        ],
                        style={"overflowX": "auto"},
                    )
                ],
                style={
                    "backgroundColor": card_color,
                    "padding": "0.75rem" if is_mobile else "1rem",
                },
            ),
        ],
        className="shadow border-0",
        style={"backgroundColor": card_color},
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False)
