import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.SLATE])

# ---------- Import and clean data (importing csv into pandas)

df = pd.read_csv(r"C:\Users\iory2\Desktop\Programing\A-DASH\info_pozos.csv")
produ = pd.read_csv(r"C:\Users\iory2\Desktop\Programing\A-DASH\produ.csv")
empresas = df['empresa'].unique()
all_wells = df[['sigla','empresa']]

df = df.groupby(['empresa','año_inicio_perf','trayectoria']).aggregate({'sigla':'count'})
df.reset_index(inplace=True)

# ------------------------------------------------------------------------------
# App layout
app.layout =  html.Div(dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Unconventional Wells per Year by Company",
                        className='text-center text-primary mb-4'),
                width=12)        
    ]),

    dbc.Row([
        
        dbc.Col([
            html.P('Select Company:', style={'textDecoration':'underline'}),
            dcc.Dropdown(id="slct_empresa",
                 options=[{'label':empresa,'value':empresa} for empresa in empresas],
                 multi=False,
                 value='YPF S.A.',
                 style={'width': "60%"}
                 ),
            dcc.Graph(id='wells_per_year')    
        ],xs=12, sm=12, md=12, lg=12, xl=12), #width={'size':6,'offset':0, 'order':1}),#size of columns, ofset is how many columns from the left de object starts, order is which object shows first
                      
    ],no_gutters=False,justify='center'), # no_gutters False make a space between de columns,
                                          # justify: start,center,end,between, around

    dbc.Row([
        # Well production 
        dbc.Col([
            
            html.P('Select Well', style={'textDecoration':'underline'}),
            
            dcc.Dropdown(
                        id='slct_well',
                        multi=True),
            
            # graph_config
            dcc.Checklist(id = 'graph_config',
                options = [
                    {'label': 'Todos los pozos', 'value': 'todos'},
                ],
                value = [],
                labelStyle = dict(display='block')),
            # wellprod
            dcc.Graph(id='wellprod')


        ],xs=12, sm=12, md=12, lg=12, xl=12),#width={'size':6})
        html.Br(),
        
        
    ], align="center",justify='around') #no_gutters=False,justify='around'),

],fluid=False))


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
Output(component_id='wells_per_year', component_property='figure'),
    Input(component_id='slct_empresa', component_property='value')
)
def update_graph(option_slctd):

    dff = df.copy()
    dff = dff[dff["empresa"] == option_slctd]
    

    # Plotly Express
    fig = px.bar(dff, x='año_inicio_perf', y='sigla',color='trayectoria')

    return  fig

# Well Dropdown
@app.callback(
    Output('slct_well','options'),
    Input('slct_empresa','value')
)
def wells_options(selected_company):
    mask = all_wells['empresa'] == selected_company
    pozos_unicos = all_wells[mask]['sigla'].unique()
    return [{'label':pozo,'value':pozo} for pozo in pozos_unicos]

# Production graph
@app.callback(
    Output('wellprod','figure'),
    [Input('slct_well','value'),
    Input('graph_config','value'),
    Input('slct_empresa','value')]
)

def well_prod(well_selected,graph_config,selected_company):
    if 'todos' in graph_config:
        print('hola')
        dff = produ[produ['empresa'] == selected_company]
        fig = px.line(dff, x="meses_prod", y="net_oil_prod",color='sigla')
        return fig
    else:
        dff = produ[produ['sigla'].isin(well_selected)]
        fig = px.line(dff, x="meses_prod", y="net_oil_prod",color='sigla')
        return fig



# ------------------------------------------------------------------------------



if __name__ == '__main__':
    app.run_server(debug=True)
