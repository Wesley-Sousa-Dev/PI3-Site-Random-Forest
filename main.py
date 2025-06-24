import dash
from dash import dcc, html, dash_table, Input, Output, callback, State
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os

dark_theme_bg = "linear-gradient(135deg, #1a1d24 0%, #2a2e3a 100%)"
light_theme_bg = "linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)"

# --- DADOS DO MODELO ---
model_data = {
    "r2": 0.9566,
    "mape": 4.58,
    "best_params": {
        "n_estimators": 4000,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "max_features": "sqrt",
        "max_depth": 35,
    },
    "feature_names": [
        "Mês",
        "Temperatura",
        "Precipitação",
        "Área Plantada",
        "Área Colhida",
    ],
    "feature_importances": np.array([0.15, 0.30, 0.25, 0.20, 0.10]),
    "y_test": np.array(
        [
            3100,
            1900,
            3250,
            1500,
            2800,
            3300,
            2000,
            1800,
            3150,
            3000,
            1450,
            1950,
            3200,
            2750,
            1550,
        ]
    ),
    "y_pred_rf": np.array(
        [
            3050,
            1950,
            3200,
            1520,
            2750,
            3280,
            2030,
            1810,
            3100,
            2950,
            1480,
            1920,
            3180,
            2700,
            1530,
        ]
    ),
}

# --- DADOS HISTÓRICOS SIMULADOS (2018-2025) ---
np.random.seed(42)
anos = list(range(2018, 2026))
meses = [
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

dados_historicos = []
for ano in anos:
    for i, mes in enumerate(meses, 1):
        temp_base = 25 + 5 * np.sin(2 * np.pi * i / 12)
        precip_base = 150 + 100 * np.sin(2 * np.pi * (i + 3) / 12)
        dados_historicos.append(
            {
                "Ano": ano,
                "Mês": mes,
                "Temperatura": round(temp_base + np.random.normal(0, 3), 1),
                "Precipitação": round(max(0, precip_base + np.random.normal(0, 30)), 1),
                "Área Plantada": round(1000 + np.random.normal(0, 200)),
                "Área Colhida": round(950 + np.random.normal(0, 180)),
                "Produção": round(
                    2500 + 500 * np.sin(2 * np.pi * i / 12) + np.random.normal(0, 300)
                ),
            }
        )

df_historico = pd.DataFrame(dados_historicos)

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
        green_colors = ["#2d5016", "#3d6b1f", "#4d8629", "#5da032", "#6ebb3c"]
    else:
        bg_color = "rgba(0,0,0,0)"
        text_color = "#2d5016"
        green_colors = ["#2d5016", "#3d6b1f", "#4d8629", "#5da032", "#6ebb3c"]

    fig = go.Figure(
        go.Bar(
            x=sorted_feature_importances,
            y=sorted_feature_names,
            orientation="h",
            marker=dict(color=green_colors, line=dict(color="#1e3a0f", width=1)),
            text=[f"{val:.1%}" for val in sorted_feature_importances],
            textposition="inside",
            textfont=dict(
                color="white", size=10 if is_mobile else 12, family="Arial Black"
            ),
            hovertemplate="<b>%{y}</b><br>Importância: %{x:.1%}<extra></extra>",
        )
    )

    # Configurações responsivas
    height = 300 if is_mobile else 400
    margin_left = 100 if is_mobile else 120
    title_size = 16 if is_mobile else 20

    fig.update_layout(
        title={
            "text": "🎯 Importância das Variáveis",
            "x": 0.5,
            "xanchor": "center",
            "font": {
                "size": title_size,
                "family": "Arial Black",
                "color": cor_detalhes,
            },
        },
        xaxis_title="Importância (%)" if is_mobile else "Importância Relativa (%)",
        yaxis_title="Variáveis",
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
    if theme == "dark":
        bg_color = "#1a1d24"
        text_color = "#e0e0e0"
    else:
        bg_color = "rgba(0,0,0,0)"
        text_color = "#2d5016"

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=model_data["y_test"],
            y=model_data["y_pred_rf"],
            mode="markers",
            marker=dict(
                size=10 if is_mobile else 14,
                color="#28a745",
                line=dict(width=1 if is_mobile else 2, color="#155724"),
                opacity=0.8,
            ),
            text=[
                f"Real: {real:,.0f}<br>Previsto: {pred:,.0f}<br>Erro: {abs(real-pred):,.0f}"
                for real, pred in zip(model_data["y_test"], model_data["y_pred_rf"])
            ],
            hovertemplate="<b>Predição</b><br>%{text}<extra></extra>",
            name="Predições",
        )
    )
    min_val = min(min(model_data["y_test"]), min(model_data["y_pred_rf"]))
    max_val = max(max(model_data["y_test"]), max(model_data["y_pred_rf"]))
    fig.add_trace(
        go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode="lines",
            line=dict(dash="dash", width=2 if is_mobile else 3, color="#dc3545"),
            name="Predição Perfeita",
            hovertemplate="Linha de Referência<extra></extra>",
        )
    )

    # Configurações responsivas
    height = 300 if is_mobile else 400
    title_size = 16 if is_mobile else 20

    fig.update_layout(
        title={
            "text": (
                "📊 Predições vs. Reais"
                if is_mobile
                else "📊 Predições vs. Valores Reais"
            ),
            "x": 0.5,
            "xanchor": "center",
            "font": {
                "size": title_size,
                "family": "Arial Black",
                "color": cor_detalhes,
            },
        },
        xaxis_title="Valores Reais",
        yaxis_title="Valores Preditos",
        height=height,
        margin=dict(l=40 if is_mobile else 50, r=30 if is_mobile else 50, t=60, b=50),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color, size=10 if is_mobile else 12),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor=(
                "rgba(255,255,255,0.9)" if theme == "light" else "rgba(26,29,36,0.9)"
            ),
            bordercolor="#28a745",
            borderwidth=1 if is_mobile else 2,
            font=dict(size=9 if is_mobile else 12),
        ),
        xaxis=dict(tickfont=dict(size=9 if is_mobile else 12)),
        yaxis=dict(tickfont=dict(size=9 if is_mobile else 12)),
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

    # Tamanhos responsivos
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
        # Barra superior mobile (só aparece no mobile)
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
                    # REMOVIDO: style={"minHeight": "56px"},
                )
            ],
            className="d-block d-md-none",
        ),
        dbc.Container(
            [
                # Header com botão de tema (só desktop)
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
                                            children=[
                                                html.Span(
                                                    "☀️",
                                                    id="theme-icon",
                                                )
                                            ],
                                            className="d-none d-md-flex",  # Só desktop
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
                # Métricas Principais - R² e MAPE
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
                                dbc.Col(
                                    [html.Div(id="metric-card-2")],
                                    xs=12,
                                    sm=6,
                                ),
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
                                dbc.Col(
                                    [html.Div(id="predictions-card")],
                                    xs=12,
                                    lg=6,
                                ),
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


# --- CALLBACK PARA ALTERNAR TEMA (ambos os botões) ---
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


# --- CALLBACK PARA ATUALIZAR O ANO SELECIONADO ---
@callback(Output("selected-year-store", "data"), Input("year-filter", "value"))
def update_selected_year(selected_year):
    return selected_year


# --- CALLBACK PARA ATUALIZAR TEMA VISUAL E COMPONENTES ---
@callback(
    [
        Output("main-container", "style"),
        Output("mobile-navbar", "children"),  # ALTERADO: de "style" para "children"
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

    # Estilos responsivos
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
        "paddingTop": "56px" if is_mobile else "0",  # Espaço para navbar mobile
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
        "Modelagem com Random Forest usando dados climáticos de 2018-2025 para previsões de produtividade."
        if is_mobile
        else "Modelagem computacional da produtividade da soja em função de variações mensais de temperatura e precipitação, entre janeiro de 2018 e fevereiro de 2025, no estado do Rio Grande do Sul. Utilizou-se o modelo Random Forest para a modelagem, com o intuito de quantificar e prever o impacto dessas variações climáticas sobre a produtividade da soja."
    )

    subtitle_style = {"fontSize": subtitle_size, "color": subtitle_color}
    footer_text_style = {"fontSize": footer_size, "color": subtitle_color}
    footer_hr_style = {"border-color": cor_detalhes, "border-width": "2px"}

    title_container_style = {"fontSize": title_size, "color": cor_detalhes}

    metric_card_1 = create_metric_card(
        "Coeficiente R²",
        f"{model_data['r2']:.4f}",
        "fa:line-chart",
        "success",
        "Qualidade do ajuste",
        theme,
        is_mobile,
    )
    metric_card_2 = create_metric_card(
        "MAPE",
        f"{model_data['mape']:.2f}%",
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
                        "Análise de Importância",
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
                        "Análise de Predições",
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

    # Estilo do filtro de ano
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
        theme_icon,  # Mesmo ícone para ambos os botões
        metric_card_1,
        metric_card_2,
        feature_importance_card,
        predictions_card,
        year_filter_container_style,
        year_filter_label_style,
        year_filter_select_style,
        title_container_style,
    )


# --- CALLBACK PARA ATUALIZAR A TABELA ---
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

    filtered_data = df_historico[df_historico["Ano"] == selected_year].copy()
    display_data = filtered_data.drop("Ano", axis=1)

    # Configurações responsivas para a tabela
    cell_padding = "8px" if is_mobile else "15px"
    font_size = "12px" if is_mobile else "14px"
    header_font_size = "13px" if is_mobile else "15px"

    # Colunas responsivas
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
            "name": "Prod (ton)" if is_mobile else "Produção (ton)",
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
                                style_table={
                                    "overflowX": "auto",
                                    "minWidth": "100%",
                                },
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
