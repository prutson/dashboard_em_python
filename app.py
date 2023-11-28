from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import dash

import plotly.express as px
import plotly.graph_objects as go
from dash_bootstrap_templates import load_figure_template

# Serve para adicionar o template em todas as figs
load_figure_template("darkly")

app = dash.Dash(
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True
)
server = app.server

# Carregando dados e tratando as datas
df_data = pd.read_csv("supermarket_sales.csv")
df_data["Date"] = pd.to_datetime(df_data["Date"])


app.layout = html.Div(children=[
            dbc.Row([
            dbc.Col(
            dbc.Card([
                html.H1('Hello Word'),
                html.Hr(),
                html.P('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent massa.'),
                html.Hr(),

                html.H5('Cidades', style={'margin-top':'50px'}),
                dcc.Checklist(df_data['City'].unique(),
                            df_data['City'].unique(), 
                            id='check_city', 
                            inputStyle={'margin-right':'10px'}),
                
                html.H5('Variável de análise', style={'margin-top':'50px'}),
                dcc.RadioItems(['gross income', 'Rating'], 
                               'gross income', 
                               id='main_variable', 
                               style={"display": "flex"},
                               inputStyle={'margin-right':'5px', 'margin-left':'5px'}),
            ], className='bg-secondary text-white p-3', style={'height':'100vh', 'padding':'30px'}), md=2),
            dbc.Col(
            html.Div(children=[
                dbc.Row([
                    dbc.Col(
                        dbc.Card([
                            dbc.CardBody([
                                html.H4('By City', className="card-title"),
                                dcc.Graph(id='city_fig', style={'height':'30vh'})
                            ])
                        ])
                    , md=4),
                    dbc.Col(
                        dbc.Card([
                            dbc.CardBody([
                                html.H4('By Gender', className="card-title"),
                                dcc.Graph(id='gender_fig', style={'height':'30vh'})
                            ])
                        ])
                    , md=4),
                    dbc.Col(
                        dbc.Card([
                            dbc.CardBody([
                                html.H4('By Payment', className="card-title"),
                                dcc.Graph(id='pay_fig', style={'height':'30vh'})
                            ])
                        ])
                    , md=4),
                ]),
                dcc.Graph(id='income_per_product_fig', style={'height':'60vh'})
            ])
            , md=10)
            ])
        
    ])

@app.callback(
    [
        Output('city_fig', 'figure'),
        Output('pay_fig', 'figure'),
        Output('gender_fig', 'figure'),
        Output('income_per_product_fig', 'figure'),
    ],
    [
        Input('check_city', 'value'),
        Input('main_variable', 'value'),
    ]
)
def render_graph(cities, main_variable):

    operation = np.sum if main_variable == "gross income" else np.mean
    df_filtered = df_data[df_data["City"].isin(cities)]

    df_city = df_filtered.groupby("City")[main_variable].apply(operation).to_frame().reset_index()
    df_product_income = df_filtered.groupby(["Product line", "City"])[[main_variable]].apply(operation).reset_index()
    df_payment = df_filtered.groupby(["Payment"])[main_variable].apply(operation).to_frame().reset_index()
    df_gender = df_filtered.groupby(["Gender"])[main_variable].apply(operation).to_frame().reset_index()

    fig_city = px.bar(df_city, 
                      x="City", 
                      y=main_variable)
    fig_payment = px.bar(df_payment, 
                         y="Payment", 
                         x=main_variable,
                         orientation="h")
    fig_gender = px.bar(df_gender, 
                         y="Gender", 
                         x=main_variable,
                         orientation="h")
    fig_product_income = px.bar(df_product_income, 
                                x=main_variable, 
                                y="Product line", 
                                color="City", 
                                orientation="h",
                                barmode='group')

    fig_city.update_layout(margin=dict(l=0, r=0, t=20, b=20))
    fig_gender.update_layout(margin=dict(l=0, r=0, t=20, b=20))
    fig_payment.update_layout(margin=dict(l=0, r=0, t=20, b=20))
    fig_product_income.update_layout(margin=dict(l=0, r=0, t=20, b=20))

    return fig_city, fig_payment, fig_gender, fig_product_income

if __name__ == "__main__":
    app.run_server(port=8050, debug=True)