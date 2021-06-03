from dash_bootstrap_components._components.Col import Col
from dash_bootstrap_components._components.Row import Row
from dash_core_components.Graph import Graph
import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.6.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.SLATE],suppress_callback_exceptions=True)

# ---------- Import and clean data (importing csv into pandas)

# Mains csvs
df = pd.read_csv(r"C:\Users\iory2\Desktop\Programing\A-DASH\Unconventional\info_pozos.csv")
produ = pd.read_csv(r"C:\Users\iory2\Desktop\Programing\A-DASH\Unconventional\produ.csv")
# Subsets per well type
df_oil = df[df['tipopozo'] == 'Petrolífero']
df_gas = df[df['tipopozo'] == 'Gasífero']
# Oil and gas wells
oil_wells = df_oil['sigla'].unique()
gas_wells = df_gas['sigla'].unique()
# Productions for oil and gas wells
oil_prod = produ[produ['sigla'].isin(oil_wells)]
gas_prod = produ[produ['sigla'].isin(gas_wells)]
# Companies
empresas = df['empresa'].unique()
all_wells = df[['sigla','empresa']]

df = df.groupby(['empresa','año_inicio_perf','trayectoria']).aggregate({'sigla':'count'})
df.reset_index(inplace=True)
# For html ----------------
""" SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#656F7C",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
} """
#----------------------
sidebar = dbc.Card([
                dbc.CardBody([
                    html.H2("Menu", className="display-4 text-center"),
                    html.Hr(),
                        dbc.Nav([
                        dbc.NavLink("Home", href="/", active="exact",className='mb-1 text-center'),
                        dbc.NavLink("Pronóstico Petróleo", href="/page-1", active="exact",className='mb-1 text-center'),
                        dbc.NavLink("Fracturas", href="/page-2", active="exact",className='text-center'),
                        ],
                        vertical=True,
                        pills=True,
                    )
                ])
            ],style={'height':'100vh','width':'20rem'})
    
        

content = dbc.Container([
    # First row - title
    dbc.Row([
        dbc.Col(html.H1("Unconventional Wells in Argentina",
                        className='text-center mb-4'),
                width=12)        
    ]),
    # Second row - Wells per companu\y
    dbc.Row([
        # Wells drilled per company per year column component
        dbc.Col([
            html.H6('Select Company:', style={'textDecoration':'underline'}),
            # Company dropdown
            dcc.Dropdown(id="slct_empresa",
                 options=[{'label':empresa,'value':empresa} for empresa in empresas],
                 multi=False,
                 value='SHELL ARGENTINA S.A.',
                 style={'width': "65%"}
                 ),
            # Bar plot - Wells drilled by company by year
            dcc.Graph(id='wells_per_year')    
        ],xs=6, sm=6, md=6, lg=6, xl=6),#width={'size':6,'offset':0, 'order':1}),#size of columns, ofset is how many columns from the left de object starts, order is which object shows first
    
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Pozos Perforados")),
                dbc.CardBody([
                        html.H5("Pozos de Petróleo", className="card-title"),
                        html.H5("Pozos de Gas", className="card-title")
                        
                ])
            ]),
            dbc.Card([
                    dbc.CardBody([
                    dcc.Graph(id='some-stuff',style={'height':'23vh'})
                        
                ])
            ],style={'height':'28vh'}),
        ],width=3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.CardHeader("Producción Petroleo")
                ])
            ]),
            dbc.Card([
                dbc.CardBody([
                    dbc.CardHeader("Producción Gas")
                    
                ])
            ])
        ],width=3)               
    
    
    ],no_gutters=False,justify='start'), # no_gutters False make a space between de columns,
                                          # justify: start,center,end,between, around
    # Second row
    dbc.Row([
        # Oil production column component
        dbc.Col([
            
            html.H6('Select Oil Well', style={'textDecoration':'underline'}),
            # Select oil well dropdown
            dcc.Dropdown(
                        id='slct_oil_well',
                        multi=True,
                        style={'width': "50%"}
            ),
            
            # Oil checklist
            dcc.Checklist(id = 'graph_config',
                options = [
                    {'label': 'Todos los pozos', 'value': 'todos'},
                    {'label': 'Filtrar por trayectoria', 'value': 'trayectoria'}
                ],
                value = ['todos'],
                labelStyle={"display": "inline-block"}, #labelStyle = dict(display='block'),
                className='mt-2'
               
            ),
            # Oil producion line-graph
            dcc.Graph(id='wellprod')
        ],xs=6, sm=6, md=6, lg=6, xl=6 ),#width = 6 ), #xs=6, sm=6, md=6, lg=6, xl=6),#width={'size':6})
        
        # GAS production column component
        dbc.Col([
            html.H6(
                'Select Gas Well', style={'textDecoration':'underline'}
            ),
            # Select gas well dropdown 
            dcc.Dropdown(
                        id='slct_gas_well',
                        multi=True,
                        style={'width': "50%"}
            ),
            # Gas checklist
            dcc.Checklist(id = 'gas_graph_config',
                options = [
                    {'label': 'Todos los pozos', 'value': 'todos'},
                    {'label': 'Filtrar por trayectoria', 'value': 'trayectoria'}
                ],
                value = ['todos'],
                labelStyle={"display": "inline-block"}, #labelStyle = dict(display='block'),
                className='mt-2'
               
            ),
            # Gas production line-graph
            dcc.Graph(id='gas_prod')

        ],xs=6, sm=6, md=6, lg=6, xl=6 )
            
    ], align="center")#justify='around') #no_gutters=False,justify='around'),

],fluid=True,style={'width': "80%"})





# ------------------------------------------------------------------------------
# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(sidebar,xs=2, sm=2, md=2, lg=2, xl=2),#width=2),
        dbc.Col(content,xs=9, sm=9, md=9, lg=9, xl=9)# width=9)
    ])
],fluid=True)

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components

# Wells drilled by year by company
@app.callback(
Output(component_id='wells_per_year', component_property='figure'),
    Input(component_id='slct_empresa', component_property='value')
)
def update_graph(option_slctd):

    dff = df.copy()
    dff = dff[dff["empresa"] == option_slctd]
    

    # Plotly Express
    fig = px.bar(dff, x='año_inicio_perf', y='sigla',color='trayectoria')
    fig.update_layout(
            template='plotly_dark',
            plot_bgcolor= 'rgba(0, 0, 0, 0)',
            paper_bgcolor= 'rgba(0, 0, 0, 0)',
            title = {'text':'Pozos Perforados por Año','y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'},
            xaxis_title = 'Años',
            yaxis_title = 'Cantidad de Pozos'
        )

    return  fig

# Wells Dropdown selection
@app.callback(
    [Output('slct_oil_well','options'),
    Output('slct_gas_well','options')],
    Input('slct_empresa','value')
)
def wells_options(selected_company):
    dff = df_oil.copy()
    dff = dff[dff['empresa'] == selected_company]
    pozos_unicos_oil = dff['sigla'].to_list()

    dff = df_gas.copy()
    dff = dff[dff['empresa'] == selected_company]
    pozos_unicos_gas = dff['sigla'].to_list()
    return [{'label':pozo,'value':pozo} for pozo in pozos_unicos_oil], [{'label':pozo,'value':pozo} for pozo in pozos_unicos_gas]

# Oil Production graph
@app.callback(
    Output('wellprod','figure'),
    [Input('slct_oil_well','value'),
    Input('graph_config','value'),
    Input('slct_empresa','value')]
)

def well_prod(well_selected,graph_config,selected_company):
    if 'todos' in graph_config:
        print('hola')
        dff = oil_prod.copy()
        dff = dff[dff['empresa'] == selected_company]
        fig = px.line(dff, x="meses_prod", y="net_oil_prod",color='sigla',title='Net Oil Production')
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor= 'rgba(0, 0, 0, 0)',
            paper_bgcolor= 'rgba(0, 0, 0, 0)',
            title = {'text':'Producción de Petróleo','y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'},
            xaxis_title = 'Meses',
            yaxis_title = 'Acumulada Petróleo [m3]'
        )
        return  fig
    
    else:
        dff = oil_prod.copy()
        dff = dff[dff['sigla'].isin(well_selected)]
        fig = px.line(dff, x="meses_prod", y="net_oil_prod",color='sigla')
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor= 'rgba(0, 0, 0, 0)',
            paper_bgcolor= 'rgba(0, 0, 0, 0)',
            title = {'text':'Producción de Petróleo','y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'},
            xaxis_title = 'Meses',
            yaxis_title = 'Acumulada Petróleo [m3]'
        )

        
        return fig


# Gas Production graph
@app.callback(
    Output('gas_prod','figure'),
    [Input('slct_gas_well','value'),
    Input('gas_graph_config','value'),
    Input('slct_empresa','value')]
)

def gas_well_prod(well_selected,graph_config,selected_company):
    if 'todos' in graph_config:
        print('hola')
        dff = gas_prod.copy()
        dff = dff[dff['empresa'] == selected_company]
        fig = px.line(dff, x="meses_prod", y="net_gas_prod",color='sigla',title='Net Gas Production')
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor= 'rgba(0, 0, 0, 0)',
            paper_bgcolor= 'rgba(0, 0, 0, 0)',
            title = {'text':'Producción de Gas','y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'},
            xaxis_title = 'Meses',
            yaxis_title = 'Acumulada Gas [m3?]'
        )

        return  fig
    
    else:
        dff = gas_prod.copy()
        dff = dff[dff['sigla'].isin(well_selected)]
        fig = px.line(dff, x="meses_prod", y="net_gas_prod",color='sigla', title='Net Gas Production')
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor= 'rgba(0, 0, 0, 0)',
            paper_bgcolor= 'rgba(0, 0, 0, 0)',
            title = {'text':'Producción de Gas','y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'},
            xaxis_title = 'Meses',
            yaxis_title = 'Acumulada Gas [m3?]'
        )
        
        return fig



# ------------------------------------------------------------------------------



if __name__ == '__main__':
    app.run_server(debug=True)


# TENGO QUE HACER LOS CALLBACKS DEL GRAFICO DE PRODUCCION DE GAS
# YA HICE LOS OUTPUTS DE: Well Dropdown @app.callback