from dash.exceptions import PreventUpdate
from pandas.core.frame import DataFrame
from dash_bootstrap_components._components.Col import Col
from dash_bootstrap_components._components.Row import Row
from dash_core_components.Graph import Graph
from dash_html_components.H5 import H5
import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import numpy as np

import dash  # (version 1.6.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.SLATE],suppress_callback_exceptions=True)

# ---------- Import and clean data (importing csv into pandas)

# Mains csvs
df = pd.read_csv(r"C:\Users\Juli\Documents\Programing\Unconventional_Oil_Gas\info_pozos.csv")
produ = pd.read_csv(r"C:\Users\Juli\Documents\Programing\Unconventional_Oil_Gas\produ.csv")
# Esto lo hago aca pero tengo que hacerlo en Produccion.ipynb
pozos_convencionales = df[df['tipo_recurso']=='CONVENCIONAL']['sigla'].to_list()
df=df[-df['sigla'].isin(pozos_convencionales)]
produ=produ[-produ['sigla'].isin(pozos_convencionales)]
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

""" df = df.groupby(['empresa','año_inicio_perf','trayectoria']).aggregate({'sigla':'count'})
df.reset_index(inplace=True) """
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
                    ],vertical=True,pills=True),
                    dcc.Dropdown(id='select_recurso',
                                options=[{'label':recurso,'value':recurso} for recurso in df['sub_tipo_recurso'].unique()],
                                value= ''),
                    dcc.Store(id='memory_recurso')
                
                ])
            ],style={'height':'101vh','width':'20rem'})
    
        

content = dbc.Container([
    # First row - title
    dbc.Row([
        dbc.Col(html.H1("Unconventional Wells in Argentina",
                        className='text-center mb-4'),
                width=12)        
    ],className='mb-4 mt-4'),
    # Second row - Wells per company
    dbc.Row([
        # Wells drilled per company per year column component
        dbc.Col([
            html.H6('Select Company:', style={'textDecoration':'underline'}),
            # Company dropdown
            dcc.Dropdown(id="slct_empresa",
                 options=[{'label':empresa,'value':empresa} for empresa in empresas],
                 multi=False,
                 value='PLUSPETROL S.A.',
                 style={'width':'20rem','color':'#272B30','background-color':'#515960'}
                 ),
            # Bar plot - Wells drilled by company by year
            dcc.Graph(id='wells_per_year',style={'height':'39vh'})    
        ],xs=6, sm=6, md=6, lg=6, xl=6),#width={'size':6,'offset':0, 'order':1}),#size of columns, ofset is how many columns from the left de object starts, order is which object shows first

        # Card - Pozos Perforados
    
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5(id='pozos-perforados', children="Pozos Perforados",className = 'text-center',style={'color': '#F2F5ED'})),
                dbc.CardBody([
                        html.H5(id='pozos-petroleo',children="Pozos de Petróleo", className="card-title, text-center",style={'color': '#00CC96'}),
                        html.H5(id='pozos-gas',children="Pozos de Gas", className="card-title, text-center",style={'color': '#EF553B'})
                        
                ])
            ]),
            # Card Graph
            dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='pie-chart',style={"height": "100%", "width": "100%"})#'height':'23vh' })
                        
                ])
            ],style={'height':'26vh'}),
        ],width=3),
        
        # Card - Produccion
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Producción",className = 'text-center',style={'color': '#F2F5ED'})),
                dbc.CardBody([
                    html.H5(id='produccion-petroleo',children="", className="card-title text-center",style={'color': '#00CC96'}),
                    html.H5(id='produccion-gas',children="", className="card-title text-center",style={'color': '#EF553B'})
                    
                ])
            ],style={'height':'15vh'}),
            dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='formaciones-graph',style={"height": "100%", "width": "100%"})#'height':'23vh' })
                        
                ])
            ],style={'height':'26vh'})
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
                        style={'width':'20rem','color':'#272B30','background-color':'#515960'}
            ),
            
            # Oil checklist
            dcc.Checklist(id = 'graph_config',
                options = [
                    {'label': 'Todos los pozos', 'value': 'todos'},
                    {'label': 'Filtrar por trayectoria', 'value': 'trayectoria'}
                ],
                value = ['todos'],
                labelStyle={"display": "inline-block",'padding':'0.2rem'}, #labelStyle = dict(display='block'),
                className='mt-2'
               
            ),
            # Oil producion line-graph
            dcc.Graph(id='wellprod',style={'height':'40vh'})
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
                        style={'width':'20rem','color':'#272B30','background-color':'#515960'}
            ),
            # Gas checklist
            dcc.Checklist(id = 'gas_graph_config',
                options = [
                    {'label': 'Todos los pozos', 'value': 'todos'},
                    {'label': 'Filtrar por trayectoria', 'value': 'trayectoria'}
                ],
                value = ['todos'],
                labelStyle={"display": "inline-block",'padding':'0.2rem'}, #labelStyle = dict(display='block'),
                className='mt-2'
               
            ),
            # Gas production line-graph
            dcc.Graph(id='gas_prod',style={'height':'40vh'})

        ],xs=6, sm=6, md=6, lg=6, xl=6 )
            
    ], align="center",className='mt-4')#justify='around') #no_gutters=False,justify='around'),

],fluid=True,style={'width': "80%"})





# ------------------------------------------------------------------------------
#                                   App layout
# -----------------------------------------------------------------------------
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(sidebar,xs=2, sm=2, md=2, lg=2, xl=2),#width=2),
        dbc.Col(content,xs=9, sm=9, md=9, lg=9, xl=9)# width=9)
    ])
],fluid=True)

# ------------------------------------------------------------------------------
#                                   App Callbacks
# ------------------------------------------------------------------------------

#Tight or Shale Dropdown Callback
@app.callback(
    Output('memory_recurso','data'),
    Input('select_recurso','value')
)
def filter_tigh_shale(recurso_selected):
    if not recurso_selected:
        return df.to_dict()
    
    filtered = df[df['sub_tipo_recurso']== recurso_selected]
    return filtered.to_dict()

# Drilled Wells Callback
@app.callback(
Output(component_id='wells_per_year', component_property='figure'),
    [Input('memory_recurso','data'),
    Input(component_id='slct_empresa', component_property='value')]
)
def update_graph(data,option_slctd):
    if data is None:
        raise PreventUpdate
    dff = pd.DataFrame.from_dict(data)
    dff = dff.groupby(['empresa','año_inicio_perf','trayectoria']).aggregate({'sigla':'count'})
    dff.reset_index(inplace=True)    
    dff = dff[dff["empresa"] == option_slctd]
    

    # Drilled Wells Graph
    fig = px.bar(dff, x='año_inicio_perf', y='sigla',color='trayectoria',color_discrete_sequence=["#FF6692","#A8B9C8",'#1DC4E0'])
    fig.update_layout(
            template='plotly_dark',
            plot_bgcolor= 'rgba(0, 0, 0, 0)',
            paper_bgcolor= 'rgba(0, 0, 0, 0)',
            title = {'text':'Pozos Perforados por Año','y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'},
            xaxis_title = 'Años',
            yaxis_title = 'Cantidad de Pozos',
        )
    

    return  fig

# Card Values callback
@app.callback(
    [Output('pozos-perforados','children'),
    Output('pozos-petroleo','children'),
    Output('pozos-gas','children'),
    Output('produccion-petroleo','children'),
    Output('produccion-gas','children'),
    Output('pie-chart','figure')],
    Input('slct_empresa','value')
)
def update_card_values(company_selected):
    # Total Pozos petroleo
    dff = df_oil.copy()
    dff_g = dff.groupby('empresa').aggregate({'sigla':'count'})
    n_pozos_petroleo = dff_g.loc[company_selected,'sigla']
    pozos_petroleo = f'Pozos Petróleros: {n_pozos_petroleo}'
    # Total Pozos Gas
    dff = df_gas.copy()
    dff_g = dff.groupby('empresa').aggregate({'sigla':'count'})
    n_pozos_gas = dff_g.loc[company_selected,'sigla']
    pozos_gas = f'Pozos Gasíferos: {n_pozos_gas}'
    # Pozos Totales
    n_pozos_totales = n_pozos_gas + n_pozos_petroleo
    pozos_totales = f'Pozos Totales: {n_pozos_totales}'
    
    #Pie-Chart
    labels = ['Pozos Petroleo','Pozos Gas']
    values = [n_pozos_petroleo,n_pozos_gas]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.45)])
    fig.update_layout(
            template='plotly_dark',
            plot_bgcolor= 'rgba(0, 0, 0, 0)',
            paper_bgcolor= 'rgba(0, 0, 0, 0)',
            #title = {'text':'Pozos Perforados por Año','y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'},
            showlegend=False,
            margin=dict(l=30, r=30, t=30, b=30),
            )
    fig.update_traces(marker=dict(colors=('#00BF8C','#EF553C')))
    
    
    
    # Producción Petróleo
    dff = oil_prod.copy()
    dff_g = dff.groupby(['empresa','sigla'],as_index=False).aggregate({'net_oil_prod':'max','net_gas_prod':'max'})
    dff_gg = dff_g.groupby('empresa').aggregate({'net_oil_prod':'sum','net_gas_prod':'sum'})
    # tengo un netoil parcial y un net gas parcial porque oil_prod y gas_prod, tienen produccion tanto de gas como de oil
    net_oil_oilDf = dff_gg.loc[company_selected,'net_oil_prod']
    net_gas_oilDf = dff_gg.loc[company_selected,'net_gas_prod']

    # Producción Gas
    dff = gas_prod.copy()
    dff_g = dff.groupby(['empresa','sigla'],as_index=False).aggregate({'net_oil_prod':'max','net_gas_prod':'max'})
    dff_gg = dff_g.groupby('empresa').aggregate({'net_oil_prod':'sum','net_gas_prod':'sum'})
    net_oil_gasDf = dff_gg.loc[company_selected,'net_oil_prod']
    net_gas_gasDf = dff_gg.loc[company_selected,'net_gas_prod']

    produccion_gas = np.round(int(net_gas_oilDf  + net_gas_gasDf)/1000000,2)
    produccion_gas = f'Gas: {produccion_gas} Mm3'
    produccion_petroleo = np.round(int(net_oil_oilDf + net_oil_gasDf)/1000000,2)
    produccion_petroleo = f'Petróleo: {produccion_petroleo} Mm3'

    
    
            
        
    
    return pozos_totales , pozos_petroleo , pozos_gas , produccion_petroleo, produccion_gas,fig



# Productive Formations Graph
@app.callback(
Output(component_id='formaciones-graph', component_property='figure'),
    Input(component_id='slct_empresa', component_property='value')
)

def update_formation_graph(selected_company):
    dff = df.copy()
    dff = dff[dff['empresa']== selected_company]
    dff= dff[dff['tipopozo'].isin(['Petrolífero','Gasífero'])]
    top5_form = dff['formacion'].value_counts()[:5]
    top5_form = top5_form.index.to_list()
    dff_g = dff.groupby(['empresa','formacion','tipopozo'],as_index=False).aggregate({'sigla':'count'})
    dff_g = dff_g[dff_g['formacion'].isin(top5_form)]
    dff_g = dff_g.sort_values(by=['formacion','sigla'],ascending = False)
    
    fig = px.bar(dff_g,x='sigla', y='formacion',orientation='h',color='tipopozo',color_discrete_map={"Gasífero": "#EF553C" ,"Petrolífero":"#00BF8C"})
    fig.update_layout(
            template='plotly_dark',
            plot_bgcolor= 'rgba(0, 0, 0, 0)',
            paper_bgcolor= 'rgba(0, 0, 0, 0)',
            #title = {'text':'Pozos Perforados por Año','y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'},
            xaxis_title = 'Pozos',
            yaxis_title = 'Formación',
            showlegend=False,
            margin=dict(l=1, r=1, t=1, b=1)
            
        )
    
    return fig

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
            yaxis_title = 'Acumulada Petróleo [m3]',
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