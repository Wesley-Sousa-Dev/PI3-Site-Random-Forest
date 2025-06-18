import dash
from dash import dcc, html, dash_table, Input, Output, callback, State
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import plotly.graph_objects as go
import pandas as pd
import numpy as np

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
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME]
)
app.title = "Random Forest ML Dashboard"

cor_detalhes = "#28a745"


# --- FUNÇÕES PARA CRIAR GRÁFICOS ---
def create_feature_importance_graph(theme="light"):
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
            textfont=dict(color="white", size=12, family="Arial Black"),
            hovertemplate="<b>%{y}</b><br>Importância: %{x:.1%}<extra></extra>",
        )
    )
    fig.update_layout(
        title={
            "text": "🎯 Importância das Variáveis",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20, "family": "Arial Black", "color": cor_detalhes},
        },
        xaxis_title="Importância Relativa (%)",
        yaxis_title="Variáveis",
        height=400,
        margin=dict(l=120, r=50, t=60, b=50),
        showlegend=False,
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color, size=12),
    )
    return fig


def create_predictions_graph(theme="light"):
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
                size=14,
                color="#28a745",
                line=dict(width=2, color="#155724"),
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
            line=dict(dash="dash", width=3, color="#dc3545"),
            name="Predição Perfeita",
            hovertemplate="Linha de Referência<extra></extra>",
        )
    )
    fig.update_layout(
        title={
            "text": "📊 Predições vs. Valores Reais",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20, "family": "Arial Black", "color": cor_detalhes},
        },
        xaxis_title="Valores Reais",
        yaxis_title="Valores Preditos",
        height=400,
        margin=dict(l=50, r=50, t=60, b=50),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color, size=12),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor=(
                "rgba(255,255,255,0.9)" if theme == "light" else "rgba(26,29,36,0.9)"
            ),
            bordercolor="#28a745",
            borderwidth=2,
        ),
    )
    return fig


def create_metric_card(
    title, value, icon, color_class="success", subtitle=None, theme="light"
):
    if theme == "dark":
        card_bg = dark_theme_bg
        text_color = "#e0e0e0"
        subtitle_color = "#a0a0a0"
    else:
        card_bg = light_theme_bg
        text_color = "#333333"
        subtitle_color = "#6c757d"

    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.Div(
                        [
                            DashIconify(
                                icon=icon,
                                width=50,
                                className=f"text-{color_class} mb-3",
                            ),
                            html.H2(
                                value,
                                className=f"text-{color_class} fw-bold mb-1",
                                style={"fontSize": "2.5rem"},
                            ),
                            html.P(
                                title,
                                className="fw-bold mb-0",
                                style={"fontSize": "1.1rem", "color": text_color},
                            ),
                            (
                                html.Small(subtitle, style={"color": subtitle_color})
                                if subtitle
                                else None
                            ),
                        ],
                        className="text-center",
                    )
                ]
            )
        ],
        className="h-100 shadow border-0",
        style={
            "background": card_bg,
            "border-left": f"5px solid {cor_detalhes} !important",
        },
    )


# --- LAYOUT PRINCIPAL ---
app.layout = html.Div(
    id="main-container",
    children=[
        dcc.Store(id="theme-store", data="light"),
        dcc.Store(id="selected-year-store", data=2023),
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
                                                            width=60,
                                                            className="me-3",
                                                            style={
                                                                "color": cor_detalhes
                                                            },
                                                        ),
                                                        "ML Model Analytics Dashboard",
                                                    ],
                                                    className="display-3 fw-bold text-center mb-0",
                                                    style={"color": cor_detalhes},
                                                ),
                                                html.P(
                                                    "Análise Completa de Performance do Modelo Random Forest",
                                                    id="subtitle",
                                                    className="lead text-center mt-3",
                                                    style={"fontSize": "1.3rem"},
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
                                                    style={"fontSize": "1.5rem"},
                                                )
                                            ],
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
                                            },
                                        ),
                                    ],
                                    className="text-center py-5",
                                    style={"position": "relative"},
                                )
                            ]
                        )
                    ],
                    className="mb-5",
                ),
                # Métricas Principais - R² e MAPE
                html.Div(
                    id="metrics-container",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    [html.Div(id="metric-card-1")],
                                    md=6,
                                ),
                                dbc.Col(
                                    [html.Div(id="metric-card-2")],
                                    md=6,
                                ),
                            ],
                            className="mb-5",
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
                                    lg=6,
                                ),
                                dbc.Col(
                                    [html.Div(id="predictions-card")],
                                    lg=6,
                                ),
                            ],
                            className="mb-5",
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
                                                {"label": f"📅 Ano {ano}", "value": ano}
                                                for ano in anos
                                            ],
                                            value=2023,
                                            className="fw-bold",
                                        ),
                                    ],
                                    id="year-filter-container",
                                    style={"marginBottom": "20px"},
                                )
                            ]
                        )
                    ]
                ),
                # Tabela de Dados Históricos
                html.Div(
                    id="table-section",
                    children=[
                        dbc.Row(
                            [dbc.Col([html.Div(id="data-table-card")])],
                            className="mb-5",
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
                                            href="",
                                            className="text-decoration-none fw-bold",
                                            style={"color": cor_detalhes},
                                        ),
                                        " | Modelo: Random Forest 🌱",
                                    ],
                                    id="footer-text",
                                    className="text-center",
                                    style={"fontSize": "1.1rem"},
                                ),
                            ]
                        )
                    ]
                ),
            ],
            fluid=True,
            className="px-4",
        ),
    ],
)


# --- CALLBACK PARA ALTERNAR TEMA ---
@callback(
    Output("theme-store", "data"),
    Input("theme-toggle", "n_clicks"),
    State("theme-store", "data"),
)
def toggle_theme(n_clicks, current_theme):
    if n_clicks is None:
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
        Output("subtitle", "style"),
        Output("footer-text", "style"),
        Output("footer-hr", "style"),
        Output("theme-icon", "children"),
        Output("metric-card-1", "children"),
        Output("metric-card-2", "children"),
        Output("feature-importance-card", "children"),
        Output("predictions-card", "children"),
        Output("year-filter-container", "style"),
        Output("year-filter-label", "style"),
        Output("year-filter", "style"),
    ],
    [Input("theme-store", "data")],
)
def update_theme(theme):
    if theme == "dark":
        background_color = "#0e1117"
        card_color = "#1a1d24"
        text_color = "#e0e0e0"
        subtitle_color = "#a0a0a0"
        shadow = "0 4px 8px rgba(0, 0, 0, 0.3)"
        theme_icon = "🌙"
    else:
        background_color = "#fafafa"
        card_color = "#ffffff"
        text_color = "#333333"
        subtitle_color = "#6c757d"
        shadow = "0 4px 8px rgba(0, 0, 0, 0.1)"
        theme_icon = "☀️"

    main_style = {
        "backgroundColor": background_color,
        "color": text_color,
        "minHeight": "100vh",
        "transition": "all 0.3s ease",
    }
    subtitle_style = {"fontSize": "1.3rem", "color": subtitle_color}
    footer_text_style = {"fontSize": "1.1rem", "color": subtitle_color}
    footer_hr_style = {"border-color": cor_detalhes, "border-width": "2px"}

    metric_card_1 = create_metric_card(
        "Coeficiente R²",
        f"{model_data['r2']:.4f}",
        "fa:line-chart",
        "success",
        "Qualidade do ajuste do modelo",
        theme,
    )
    metric_card_2 = create_metric_card(
        "MAPE",
        f"{model_data['mape']:.2f}%",
        "fa:percent",
        "success",
        "Erro percentual médio absoluto",
        theme,
    )
    feature_importance_card = dbc.Card(
        [
            dbc.CardHeader(
                [
                    html.H5(
                        "Análise de Importância",
                        className="mb-0 fw-bold",
                        style={"color": cor_detalhes},
                    )
                ],
                style={
                    "background": dark_theme_bg if theme == "dark" else light_theme_bg,
                    "border-bottom": f"3px solid {cor_detalhes}",
                },
            ),
            dbc.CardBody(
                [
                    dcc.Graph(
                        id="feature-importance-graph",
                        figure=create_feature_importance_graph(theme),
                    )
                ],
                style={"backgroundColor": card_color},
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
                        style={"color": cor_detalhes},
                    )
                ],
                style={
                    "background": dark_theme_bg if theme == "dark" else light_theme_bg,
                    "border-bottom": f"3px solid {cor_detalhes}",
                },
            ),
            dbc.CardBody(
                [
                    dcc.Graph(
                        id="predictions-vs-actual-graph",
                        figure=create_predictions_graph(theme),
                    )
                ],
                style={"backgroundColor": card_color},
            ),
        ],
        className="shadow border-0 h-100",
        style={"backgroundColor": card_color},
    )

    # Estilo do filtro de ano
    year_filter_container_style = {
        "marginBottom": "20px",
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
        "fontSize": "1.1rem",
    }
    year_filter_select_style = {
        "border": f"2px solid {cor_detalhes}",
        "border-radius": "8px",
        "backgroundColor": card_color,
        "color": text_color,
        "fontWeight": "bold",
        "fontSize": "1.1rem",
        "transition": "all 0.3s ease",
    }

    return (
        main_style,
        subtitle_style,
        footer_text_style,
        footer_hr_style,
        theme_icon,
        metric_card_1,
        metric_card_2,
        feature_importance_card,
        predictions_card,
        year_filter_container_style,
        year_filter_label_style,
        year_filter_select_style,
    )


# --- CALLBACK PARA ATUALIZAR A TABELA ---
@callback(
    Output("data-table-card", "children"),
    [Input("selected-year-store", "data"), Input("theme-store", "data")],
)
def update_table(selected_year, theme):
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

    return dbc.Card(
        [
            dbc.CardHeader(
                [
                    html.H4(
                        [
                            DashIconify(
                                icon="fa:table",
                                width=30,
                                className="me-2",
                                style={"color": cor_detalhes},
                            ),
                            "Dados Históricos por Ano",
                        ],
                        className="mb-0 fw-bold",
                        style={"color": cor_detalhes},
                    )
                ],
                style={
                    "background": dark_theme_bg if theme == "dark" else light_theme_bg,
                    "border-bottom": f"3px solid {cor_detalhes}",
                },
            ),
            dbc.CardBody(
                [
                    dash_table.DataTable(
                        data=display_data.to_dict("records"),
                        columns=[
                            {"name": "Mês", "id": "Mês", "type": "text"},
                            {
                                "name": "Temperatura (°C)",
                                "id": "Temperatura",
                                "type": "numeric",
                                "format": {"specifier": ".1f"},
                            },
                            {
                                "name": "Precipitação (mm)",
                                "id": "Precipitação",
                                "type": "numeric",
                                "format": {"specifier": ".1f"},
                            },
                            {
                                "name": "Área Plantada (ha)",
                                "id": "Área Plantada",
                                "type": "numeric",
                                "format": {"specifier": ",.0f"},
                            },
                            {
                                "name": "Área Colhida (ha)",
                                "id": "Área Colhida",
                                "type": "numeric",
                                "format": {"specifier": ",.0f"},
                            },
                            {
                                "name": "Produção (ton)",
                                "id": "Produção",
                                "type": "numeric",
                                "format": {"specifier": ",.0f"},
                            },
                        ],
                        style_table={"overflowX": "auto"},
                        style_cell={
                            "textAlign": "center",
                            "padding": "15px",
                            "fontFamily": "Arial",
                            "fontSize": "14px",
                            "border": f"1px solid {cor_detalhes}",
                            "backgroundColor": table_cell_bg,
                            "color": table_cell_color,
                        },
                        style_header={
                            "backgroundColor": table_header_bg,
                            "color": "white",
                            "fontWeight": "bold",
                            "fontSize": "15px",
                            "border": f"1px solid {cor_detalhes}",
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
                                "width": "15%",
                                "fontWeight": "bold",
                                "backgroundColor": (
                                    f"rgba(40, 167, 69, 0.05)"
                                    if theme == "light"
                                    else f"rgba(40, 167, 69, 0.15)"
                                ),
                            },
                            {"if": {"column_id": "Temperatura"}, "width": "17%"},
                            {"if": {"column_id": "Precipitação"}, "width": "17%"},
                            {"if": {"column_id": "Área Plantada"}, "width": "17%"},
                            {"if": {"column_id": "Área Colhida"}, "width": "17%"},
                            {"if": {"column_id": "Produção"}, "width": "17%"},
                        ],
                    )
                ],
                style={"backgroundColor": card_color},
            ),
        ],
        className="shadow border-0",
        style={"backgroundColor": card_color},
    )


if __name__ == "__main__":
    app.run(debug=True)
