import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

from layouts import layoutCOMEX, layoutVIA, layoutSH2, layoutDataSeg, layoutDataSegNCMSH, layoutDataVis, cards, colors
import callbacks

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/comex':
         return layoutCOMEX
    elif pathname == '/via':
         return layoutVIA
    elif pathname == '/sh2':
         return layoutSH2
    elif pathname == '/datasegmentation':
         return layoutDataSeg
    elif pathname == '/datasegmentationNCMSH':
         return layoutDataSegNCMSH
    elif pathname == '/datavisualization':
         return layoutDataVis
    else:
        return cards

if __name__ == '__main__':
    app.run_server(debug=True)