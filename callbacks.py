from dash.dependencies import Input, Output
from layouts import comex, via
import plotly.express as px
import pandas as pd

from app import app

def update_visualization(year_dropdown, mov_dropdown, prod_dropdown):
    comexf = comex[comex['ANO'] == year_dropdown]

    if mov_dropdown:
        comexf = comexf[comexf['MOVIMENTACAO'] == mov_dropdown.encode('utf-8')]

    if prod_dropdown:
        comexf = comexf[comexf['COD_NCM'] == prod_dropdown]

    return comexf

@app.callback(
    Output('total-movimentado', 'children'),
    [Input('year-dropdown', 'value'),
     Input('mov-dropdown', 'value'),
     Input('prod-dropdown', 'value')])
def update_card(year_dropdown, mov_dropdown, prod_dropdown):
    comexf = update_visualization(year_dropdown, mov_dropdown, prod_dropdown)

    valorTotal = 'Valor: {}'.format(comexf['VL_QUANTIDADE'].sum())

    return valorTotal

@app.callback(
    Output('prod-graph', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('mov-dropdown', 'value'),
     Input('prod-dropdown', 'value')])
def update_bars(year_dropdown, mov_dropdown, prod_dropdown):
    comexf = update_visualization(year_dropdown, mov_dropdown, prod_dropdown)

    return {
        'data': [dict(
            x=comexf['MES'],
            y=comexf['VL_QUANTIDADE'],
            type='bar',
        )]
    }

@app.callback(
    Output("utilizacao-via", "figure"), 
    [Input('year-dropdown', 'value'),
     Input('mov-dropdown', 'value'),
     Input('prod-dropdown', 'value')])
def update_pie(year_dropdown, mov_dropdown, prod_dropdown):
    comexf = update_visualization(year_dropdown, mov_dropdown, prod_dropdown)

    dff = pd.merge(via, comexf, on="COD_VIA")

    figVIA = px.pie(dff, values='VL_PESO_KG', names='NO_VIA')
    return figVIA
