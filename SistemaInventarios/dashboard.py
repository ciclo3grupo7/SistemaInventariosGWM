import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

from SistemaInventarios import appDash

data = pd.read_csv("avocado.csv")
data = data.query("type == 'conventional' and region == 'Albany'")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

## Importar la data 2
df = pd.read_csv('data.csv', delimiter = ';')
#Crear una tabla dinámica
pv = pd.pivot_table(df, index=['Name'], columns=["Status"], values=['Quantity'], aggfunc=sum, fill_value=0)
trace1 = go.Bar(x=pv.index, y=pv[('Quantity', 'declinada')], name='EnProceso')
trace2 = go.Bar(x=pv.index, y=pv[('Quantity', 'pendiente')], name='Solitado')
trace3 = go.Bar(x=pv.index, y=pv[('Quantity', 'presentada')], name='PorEntregar')
trace4 = go.Bar(x=pv.index, y=pv[('Quantity', 'ganada')], name='Entregado')


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
appDash.title = "SISTEMA DE INVENTARIOS GWM"

# Custom HTML layout
html_layout = open("SistemaInventarios/templates/DashBoard.html", "r").read()
# print("html_layout")
# print(html_layout)

appDash.index_string = html_layout

appDash.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H2(
                    children="DASHBOARD", className="header-title"
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children= dcc.Graph(
                        id='example-graph',
                        config={"displayModeBar": False},
                        figure={
                            'data': [trace1, trace2, trace3, trace4],
                            'layout':
                            go.Layout(title='Estado de Pedidos a los Proveedores', barmode='stack')
                        },
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": data["Date"],
                                    "y": data["AveragePrice"],
                                    "type": "lines",
                                    "hovertemplate": "$%{y:.2f}"
                                                     "<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Stock de Inventario",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {
                                    "tickprefix": "$",
                                    "fixedrange": True,
                                },
                                "colorway": ["#17B897"],
                            },
                        },
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": data["Date"],
                                    "y": data["Total Volume"],
                                    "type": "lines",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Unidades Vendidas",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {"fixedrange": True},
                                "colorway": ["#E12D39"],
                            },
                        },
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)
