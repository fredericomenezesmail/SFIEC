import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import dash_table as dt

colors = {
    'background': '#FFFFFF',
    'text': '#111111',
    'backgroundFIEC': '#005CAA',
    'textFIEC': '#FFFFFF'
}

via = pd.read_excel('app/static/d_via.xlsx')
sh2 = pd.read_excel('app/static/d_sh2.xlsx')
comex = pd.read_csv('app/static/f_comex.csv')
# comex = pd.read_csv('app/static/f_comex_1000.csv')

comexSH2 = pd.merge(sh2, comex, on="COD_NCM")

years = comex['ANO'].unique()
prods = comex['COD_NCM'].unique()
movs = comex['MOVIMENTACAO'].unique()
months = comex['MES'].unique()

figProd = px.bar(comex, x="MES", y="VL_QUANTIDADE", barmode="group")

def generate_table(dataframe, min_rows=1):
    return html.Table(
        [
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(max(len(dataframe), min_rows))
        ])
    ])

# 1) f_comex.csv
layoutCOMEX = html.Div([
    generate_table(comex)
])

# 1) d_via
layoutVIA = html.Div([
    generate_table(via)
])

# 1) d_sh2
layoutSH2 = html.Div([
    generate_table(sh2)
])

# 2) a) Filtros ano, movimentacao
layoutDataSeg = html.Div([
    html.H3(
        children='Segmentacao de dados',
        style={
            'textAlign': 'center',
            'color': colors['textFIEC'],
            'backgroundColor': colors['backgroundFIEC']
        }
    ),

    dt.DataTable(
        id='data-segmentation',
        columns=[{"name": i, "id": i} for i in comex.columns],
        data=comex.to_dict('records'),
        filter_action="native"
    )
])

# 2) a) iii) Filtro produto NCM SH2
layoutDataSegNCMSH = html.Div([
    html.H3(
        children='Segmentacao de dados',
        style={
            'textAlign': 'center',
            'color': colors['textFIEC'],
            'backgroundColor': colors['backgroundFIEC']
        }
    ),

    dt.DataTable(
        id='data-segmentation',
        columns=[{"name": i, "id": i} for i in comexSH2.columns],
        data=comexSH2.to_dict('records'),
        filter_action="native"
    )
])

# 2) b) Total movimentado
# 2) c) i) Visualizacao grafico de barras
layoutDataVis = html.Div([

    html.H3(
        children='Visualizacoes',
        style={
            'textAlign': 'center',
            'color': colors['textFIEC'],
            'backgroundColor': colors['backgroundFIEC']
        }
    ),

    dbc.Card(
        [
            dbc.CardHeader("Total Movimentado"),
            dbc.CardBody("Total", id="total-movimentado")
        ],
        style={"width": "22rem"}, color=colors['backgroundFIEC'], inverse=True
    ),
    html.Br(),

    dbc.Card([
        dbc.CardHeader("Filtros"),
        dbc.CardBody([

            html.Div([
                html.H5(
                    children='Ano', style={'display': 'inline-block'}
                ),

                html.Div([
                    dcc.Dropdown(
                        id='year-dropdown',
                        options=[{'label': i, 'value': i} for i in years],
                        value='',
                        style={
                            'color': colors['text']
                        }
                    )
                ],
                className='four columns',
                style={'width': '50%'}),
            ]),

            html.Div([
                html.H5(
                    children='Movimentacao'
                ),

                html.Div([
                    dcc.Dropdown(
                        id='mov-dropdown',
                        options=[{'label': i, 'value': i} for i in movs],
                        value='',
                        style={
                            'color': colors['text']
                        }
                    )
                ],
                className='four columns',
                style={'width': '50%'}),
            ]),

            html.Div([
                html.H5(
                    children='NCM'
                ),

                html.Div([
                    dcc.Dropdown(
                        id='prod-dropdown',
                        options=[{'label': i, 'value': i} for i in prods],
                        value='',
                        style={
                            'color': colors['text']
                        }
                    )
                ], 
                className='four columns',
                style={'width': '50%'})
            ]),
            html.Br(),

            ]),
        ],
        style={"width": "22rem"}, color=colors['backgroundFIEC'], inverse=True
    ),
    html.Br(),

    html.H3(
        children='Quantidade produto / mes',
        style={
            'textAlign': 'center',
            'color': colors['textFIEC'],
            'backgroundColor': colors['backgroundFIEC']
        }
    ),

    html.Div([
        dcc.Graph(id='prod-graph'),
    ], className='row'),

    html.H3(
        children='Utilizacao por VIA',
        style={
            'textAlign': 'center',
            'color': colors['textFIEC'],
            'backgroundColor': colors['backgroundFIEC']
        }
    ),

    dcc.Graph(id='utilizacao-via'),

])

cards = html.Div([
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("COMEX"),
                dbc.CardBody([
                    html.P("Dados f_comex.csv", className="card-text"),
                    dbc.Button(
                        "COMEX", color="dark", className="mt-auto", href="/comex",
                            style={'width': '35%'}
                    ),
                    html.Br()]),
                ],
                color=colors['backgroundFIEC'], inverse=True
            ),
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("VIA"),
                dbc.CardBody([
                    html.P("Dados d_via.xlsx", className="card-text"),
                    dbc.Button(
                        "VIA", color="dark", className="mt-auto", href="/via",
                            style={'width': '35%'}
                    ),
                    html.Br()]),
                ],
                color=colors['backgroundFIEC'], inverse=True
            ),
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("SH2"),
                dbc.CardBody([
                    html.P("Dados d_sh2.xlsx", className="card-text"),
                    dbc.Button(
                        "SH2", color="dark", className="mt-auto", href="/sh2",
                            style={'width': '35%'}
                    ),
                    html.Br()]),
                ],
                color=colors['backgroundFIEC'], inverse=True
            ),
        ),],
        className="mb-4",
    ),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Segmentacao de dados"),
                dbc.CardBody([
                    html.P("Filtros (segmentacao de dados)", className="card-text"),
                    html.P("i) Ano.", className="card-text"),
                    html.P("ii) Movimentacao (Importacao e Exportacao).", className="card-text"),
                    dbc.Button(
                        "Segmentacao", color="dark", className="mt-auto", href="/datasegmentation",
                            style={'width': '35%'}
                    ),
                    html.Br()]),
                ],
                color=colors['backgroundFIEC'], inverse=True
            ),
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Segmentacao de dados"),
                dbc.CardBody([
                    html.P("Filtros (segmentacao de dados)", className="card-text"),
                    html.P("iii) Produto (NM_SH2).", className="card-text"),
                    dbc.Button(
                        "Segmentacao NM_SH2", color="dark", className="mt-auto", href="/datasegmentationNCMSH",
                            style={'width': '35%'}
                    ),
                    html.Br()]),
                ],
                color=colors['backgroundFIEC'], inverse=True
            ),
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Visualizacoes"),
                dbc.CardBody([
                    html.P("Visualizacao de dados por segmentacao", className="card-text"),
                    html.P("i) Grafico de Barras.", className="card-text"),
                    html.P("ii) Grafico de Pizza.", className="card-text"),
                    # html.P("iii) Tabela com o total por estado.", className="card-text"),
                    dbc.Button(
                        "Visualizacoes", color="dark", className="mt-auto", href="/datavisualization",
                            style={'width': '35%'}
                    ),
                    html.Br()]),
                ],
                color=colors['backgroundFIEC'], inverse=True
            ),
        ),],
        className="mb-4",
    )
])