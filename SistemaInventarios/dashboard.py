import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from flask import render_template

from SistemaInventarios import appDash

#print("Entro dashboard2")
appDash.index_string = "{%app_entry%} {%config%} {%scripts%} {%renderer%}"
appDash.layout = html.Div()

def dashboard_principal(tipoUsuario, usuario, infoUser, opcMenu):
    #print("entro a dashboard_principal()")
    data = pd.read_csv("avocado.csv")
    #print("data1:",data)
    data = data.query("type == 'conventional' and region == 'Albany'")
    #print("data2:",data)
    data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
    data.sort_values("Date", inplace=True)
    #print("data3:",data)

    ## Importar la data 2
    df = pd.read_csv('data.csv', delimiter = ';')
    #Crear una tabla dinámica
    pv = pd.pivot_table(df, index=['Name'], columns=["Status"], values=['Quantity'], aggfunc=sum, fill_value=0)
    trace1 = go.Bar(x=pv.index, y=pv[('Quantity', 'declinada')], name='EnProceso')
    trace2 = go.Bar(x=pv.index, y=pv[('Quantity', 'pendiente')], name='Solitado')
    trace3 = go.Bar(x=pv.index, y=pv[('Quantity', 'presentada')], name='PorEntregar')
    trace4 = go.Bar(x=pv.index, y=pv[('Quantity', 'ganada')], name='Entregado')


    appDash.title = "Sistema de Inventarios GWM - Dashboard"

    # Custom HTML layout

    rtaHTML = render_template("DashBoard.html",title=appDash.title, usuario=usuario, infoUser=infoUser, opcMenu=opcMenu)
    rtaHTML = rtaHTML.replace("__app_entry__", "{%app_entry%}")
    rtaHTML = rtaHTML.replace("__config__", "{%config%}")
    rtaHTML = rtaHTML.replace("__scripts__", "{%scripts%}")
    rtaHTML = rtaHTML.replace("__renderer__", "{%renderer%}")
    html_layout = rtaHTML
    #f= open("xxDashboard.html","w")
    #f.write(html_layout)
    #f.close()
    #print("creo xxDashboard.html")

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
            html.Table(
                children=[
                    html.Tr(
                        children=[
                            html.Td(
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
                            html.Td(
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
                        ]
                    ),
                    html.Tr(
                        children=[
                            html.Td(
                                children= dcc.Graph(
                                    id='example-graph2',
                                    config={"displayModeBar": False},
                                    figure={
                                        'data': [trace1, trace2, trace3, trace4],
                                        'layout':
                                        go.Layout(title='Estado de Pedidos a los Proveedores', barmode='stack')
                                    },
                                ),
                                className="card",
                            ),
                            html.Td(
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
                        ]
                    )
                ],
                className="wrapper",
            ),
        ]
    )
