import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# ---------- Import and clean data (importing csv into pandas)
# df = pd.read_csv("intro_bees.csv")
df = pd.read_csv("info_pozos.csv")
empresas = df['empresa'].unique()
all_wells = df[['sigla','empresa']]

df = df.groupby(['empresa','año_inicio_perf','trayectoria']).aggregate({'sigla':'count'})
df.reset_index(inplace=True)

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Unconventional Wells per Year by Company", style={'text-align': 'center'}),

    html.H3('Select Company'),
    dcc.Dropdown(id="slct_empresa",
                 options=[{'label':empresa,'value':empresa} for empresa in empresas],
                 multi=False,
                 value='YPF S.A.',
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='wells_per_year', figure={}),
    html.Br(),

    html.H3('Select Well'),
    dcc.Dropdown(
        id='slct_well',
        style={'width': "40%"})


])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='wells_per_year', component_property='figure')],
    [Input(component_id='slct_empresa', component_property='value')]
)
def update_graph(option_slctd):

    container = "The company chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["empresa"] == option_slctd]
    

    # Plotly Express
    fig = px.bar(dff, x='año_inicio_perf', y='sigla',color='trayectoria')

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return container, fig


@app.callback(
    Output('slct_well','options'),
    Input('slct_empresa','value')
)
def wells_options(selected_company):
    mask = all_wells['empresa'] == selected_company
    pozos_unicos = all_wells[mask]['sigla'].unique()
    return [{'label':pozo,'value':pozo} for pozo in pozos_unicos]


# ------------------------------------------------------------------------------







if __name__ == '__main__':
    app.run_server(debug=True)
