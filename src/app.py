import dash
import dash_html_components as html
import dash_core_components as dcc
import altair as alt
import pandas as pd
import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from vega_datasets import data

alt.data_transformers.disable_max_rows()

df = pd.read_csv('data/processed/cleaned_data.csv') #data/processed/cleaned_data.csv
df = df.query('country == "US"') 
df['title'] = df['title'].str.split('(',expand=True)
display_df = df[['title', 'variety', 'state', 'points', 'price']]
display_df = display_df.rename(columns={'title': 'Title', 'variety':'Variety', 'state':'State', 'points':'Points', 'price':'Price'})
app = dash.Dash(__name__ , external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server

colors = {
    'background': '#111111',
    'text': '#522889'
}

collapse = html.Div(
    [
        dbc.Button(
            "Learn more",
            id="collapse-button",
            className="mb-3",
            outline=False,
            style={'margin-top': '10px',
                'width': '150px',
                'background-color': 'white',
                'color': 'steelblue'}
        ),
    ]
)

@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('MDS Winery Dashboard', style={'text-align': 'center', 'color': '#522889', 'font-size': '40px', 'font-family': 'Georgia'}),
            dbc.Collapse(html.P(
                """
                Let me introduce our MDS winery dashboard to you =)
                """,
                style={'color': 'white', 'width': '55%'}
            ), id='collapse'),
        ], md=10),
        dbc.Col([collapse])
    ], style={'backgroundColor': '#E4C8EB', 'border-radius': 3, 'padding': 15, 'margin-top': 22, 'margin-bottom': 22, 'margin-right': 11}),

    dcc.Tabs([
        dcc.Tab([
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    # html.Label([
                    #     'Country Selection']),
                    # dcc.Dropdown(
                    #     options=[{'label': country, 'value': country} for country in df['country'].unique()],
                    #     placeholder='Select a Country', 
                    #     multi=True
                    # ),
                    html.Label([
                        'State Selection'], style={
                'color': '#7a4eb5', "font-weight": "bold"
            }),
                    dcc.Dropdown(
                        id='province-widget',
                        value='select your state',  
                        options=[{'label': state, 'value': state} for state in df['state'].unique()],
                        multi=True,
                        placeholder='Select a State'
                    ),
                    html.Label(['Wine Type'], style={'color': '#7a4eb5', "font-weight": "bold"}
                    ),
                    dcc.Dropdown(
                        id='wine_variety',
                        value='select a variety', 
                        placeholder='Select a Variety', 
                        multi=True
                    ),
                    html.Br(),
                    html.Label(['Price Range'], style={
                'color': '#7a4eb5', "font-weight": "bold"
            }
                    ),
                    dcc.RangeSlider(
                        id='price',
                        min=df['price'].min(),
                        max=df['price'].max(),
                        value=[df['price'].min(), df['price'].max()],
                        marks = {4: '$4', 25: '$25', 50: '$50', 75: '$75', 100: '$100','color': '#7a4eb5'}
                    ),
                    html.Label(['Points Range'], style={
                'color': '#7a4eb5', "font-weight": "bold"
            }
                    ),
                    dcc.RangeSlider(
                        id='points',
                        min=df['points'].min(),
                        max=df['points'].max(),
                        value=[df['points'].min(), df['points'].max()],
                        marks = {80: '80', 85: '85', 90: '90', 95: '95', 100: '100'}
                        ),
                    html.Label(['Value Ratio'], style={
                'color': '#7a4eb5', "font-weight": "bold"
            }
                    ),
                    dcc.RangeSlider(min=0, 
                        max=1, 
                        step=0.1, 
                        value=[0.2,0.6], 
                        marks = {0: '0', 0.2: '0.2', 0.4: '0.4', 0.6: '0.6', 0.8: '0.8', 1: '1'}  
                    ),
                    ], md=4,
                ),
                dbc.Col([
                    html.Iframe(
                        id = 'maps',
                        style={'border-width': '0', 'width': '100%', 'height': '460px'})
                    ], md=8)
                ]),
            dbc.Row([
                    dbc.Col([
                    html.Br(),
                    dbc.Row([
                            dbc.Card([
                                dbc.CardHeader('Highest Value Wine:', 
                                style={'fontWeight': 'bold', 'color':'black','font-size': '22px', 'backgroundColor':'#9980D4','width': '100%', 'height': '100%'}),
                                html.H5(id='highest_value_name', style={'color': 'blue', 'fontSize': 18, 'width': '300px', 'height': '100%'}),
                            html.Br(),
                            html.H4(
                                id='highest_value', style={'color': 'blue', 'fontSize': 18, 'width': '300px', 'height': '100%'})])]),
                    html.Br(),     
                    dbc.Row([
                            dbc.Card([
                                dbc.CardHeader('Highest Score Wine:', 
                                style={'fontWeight': 'bold', 'color':'black','font-size': '22px', 'backgroundColor':'#9980D4', 'width': '100%', 'height': '100%'}),
                                html.H5(id='highest_score_name', style={'color': 'blue', 'fontSize': 18, 'width': '300px', 'height': '100%'}),
                            html.Br(),
                            html.H4(
                                id='highest_score',style={'color': 'blue', 'fontSize': 18, 'width': '300px', 'height': '100%'}),
                        ]),
                        ])
                    ], md = 3),
                dbc.Col([
                    
                    html.Iframe(
                        id = 'plots',
                        style={'border-width': '0', 'width': '100%', 'height': '500px'})
                    ]),

                ]),
            ], label='MDS Winery'),
        dcc.Tab([
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    # html.Label([
                    #     'Country Selection']),
                    # dcc.Dropdown(
                    #     options=[{'label': country, 'value': country} for country in df['country'].unique()],
                    #     placeholder='Select a Country', 
                    #     multi=True
                    # ),
                    html.Label([
                        'State Selection'], style={
                'color': '#7a4eb5', "font-weight": "bold"
            }),
                    dcc.Dropdown(
                        id='table_state',
                        value='select your state',  
                        options=[{'label': state, 'value': state} for state in df['state'].unique()],
                        multi=True,
                        placeholder='Select a State'
                    ),
                    html.Label(['Wine Type'], style={
                'color': '#7a4eb5', "font-weight": "bold"
            }
                    ),
                    dcc.Dropdown(
                        id='table_variety',
                        value='select a variety', 
                        placeholder='Select a Variety', 
                        multi=True
                    ),
                    html.Br(),
                    html.Label(['Price Range'], style={
                'color': '#7a4eb5', "font-weight": "bold"
            }
                    ),
                    dcc.RangeSlider(
                        id='table_price',
                        min=df['price'].min(),
                        max=df['price'].max(),
                        value=[df['price'].min(), df['price'].max()],
                        marks = {4: '$4', 25: '$25', 50: '$50', 75: '$75', 100: '$100','color': '#7a4eb5'}
                    ),
                    html.Label(['Points Range'], style={
                'color': '#7a4eb5', "font-weight": "bold"
            }
                    ),
                    dcc.RangeSlider(
                        id='table_points',
                        min=df['points'].min(),
                        max=df['points'].max(),
                        value=[df['points'].min(), df['points'].max()],
                        marks = {80: '80', 85: '85', 90: '90', 95: '95', 100: '100'}
                        ),
                    html.Label(['Value Ratio'], style={
                'color': '#7a4eb5', "font-weight": "bold"
            }
                    ),
                    dcc.RangeSlider(min=0, 
                        max=1, 
                        step=0.1, 
                        value=[0.2,0.6], 
                        marks = {0: '0', 0.2: '0.2', 0.4: '0.4', 0.6: '0.6', 0.8: '0.8', 1: '1'}  
                    ),
                ], md=4,),
                dbc.Col([
                    html.Br(),
                    html.Br(),
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": col, "id": col} for col in display_df.columns[:]], 
                        data=display_df.to_dict('records'),
                        page_size=11,
                        sort_action='native',
                        style_header = {'textAlign': 'left'},
                        style_data = {'textAlign': 'left'},
                    ),
                ], md=8)
            ]),
            dbc.Row([
                dbc.Col([
                    html.Iframe(
                        id = 'table_plots',
                        style={'border-width': '0', 'width': '100%', 'height': '500px'})]),
                dbc.Col([
                html.Iframe(
                        id = 'heat_plot',
                        style={'border-width': '0', 'width': '100%', 'height': '500px'})])
                ])     
        ],label='Data')]),
])
    

@app.callback(
    Output('highest_score', 'children'),
    Input('wine_variety', 'value'),
    Input('province-widget', 'value'),
    Input('price', 'value'),
    Input('points', 'value'))
def max_score(wine_variety, selected_state, price_value, points_value):
    if selected_state == 'select your state':
        df_filtered = df
    else:
        if type(selected_state) == list:
            df_filtered = df[df['state'].isin(selected_state)]
        else:
            df_filtered = df[df['state'] == selected_state]
    if wine_variety == 'select a variety':
         df_filtered = df_filtered
    else:
        if type(wine_variety) == list:
            df_filtered = df_filtered[df_filtered['variety'].isin(wine_variety)]
        else:  
            df_filtered = df_filtered.query("variety == @wine_variety")

    df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
    df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]
    max_points = max(df_filtered['points'])
    df_filtered = df[df['points'] == max_points]
    wine_name = df_filtered['title'].iloc[0]

    return str(str(round(max_points,2)))


@app.callback(
    Output('highest_score_name', 'children'),
    Input('wine_variety', 'value'),
    Input('province-widget', 'value'),
    Input('price', 'value'),
    Input('points', 'value'))
def max_score_name(wine_variety, selected_state, price_value, points_value):
    if selected_state == 'select your state':
        df_filtered = df
    else:
        if type(selected_state) == list:
            df_filtered = df[df['state'].isin(selected_state)]
        else:
            df_filtered = df[df['state'] == selected_state]
    if wine_variety == 'select a variety':
         df_filtered = df_filtered
    else:
        if type(wine_variety) == list:
            df_filtered = df_filtered[df_filtered['variety'].isin(wine_variety)]
        else:  
            df_filtered = df_filtered.query("variety == @wine_variety")

    df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
    df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]
    max_points = max(df_filtered['points'])
    df_filtered = df[df['points'] == max_points]
    wine_name = df_filtered['title'].iloc[0]

    return str(wine_name.split(' (')[0])

@app.callback(
    Output('highest_value_name', 'children'),
    Input('wine_variety', 'value'),
    Input('province-widget', 'value'),
    Input('price', 'value'),
    Input('points', 'value'))
def max_value_name(wine_variety, selected_state, price_value, points_value):
    if selected_state == 'select your state':
        df_filtered = df
    else:
        if type(selected_state) == list:
            df_filtered = df[df['state'].isin(selected_state)]
        else:
            df_filtered = df[df['state'] == selected_state]
    if wine_variety == 'select a variety':
         df_filtered = df_filtered
    else:
        if type(wine_variety) == list:
            df_filtered = df_filtered[df_filtered['variety'].isin(wine_variety)]
        else:  
            df_filtered = df_filtered.query("variety == @wine_variety")

    df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
    df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]
    max_value = max(df_filtered['value'])
    df_filtered = df[df['value'] == max_value]
    wine_name = df_filtered['title'].iloc[0]
    return (wine_name.split(' (')[0] + '     ')

@app.callback(
    Output('highest_value', 'children'),
    Input('wine_variety', 'value'),
    Input('province-widget', 'value'),
    Input('price', 'value'),
    Input('points', 'value'))
def max_value(wine_variety, selected_state, price_value, points_value):
    if selected_state == 'select your state':
        df_filtered = df
    else:
        if type(selected_state) == list:
            df_filtered = df[df['state'].isin(selected_state)]
        else:
            df_filtered = df[df['state'] == selected_state]
    if wine_variety == 'select a variety':
         df_filtered = df_filtered
    else:
        if type(wine_variety) == list:
            df_filtered = df_filtered[df_filtered['variety'].isin(wine_variety)]
        else:  
            df_filtered = df_filtered.query("variety == @wine_variety")

    df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
    df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]

    max_value = max(df_filtered['value'])
    df_filtered = df[df['value'] == max_value]
    return str(str(round(max_value, 2)))
  
@app.callback(
    Output('table_variety', 'options'),
    Input('province-widget', 'value'))
def wine_options(state):
    if state == 'select your state':
        df_filtered = df
    else:
        if type(state) == list:
            df_filtered = df[df['state'].isin(state)]
        else:
            df_filtered = df[df['state'] == state]
    return [{'label': variety, 'value': variety} for variety in df_filtered['variety'].unique()]

@app.callback(
    Output('wine_variety', 'options'),
    Input('table_state', 'value'))
def wine_options(state):
    if state == 'select your state':
        df_filtered = df
    else:
        if type(state) == list:
            df_filtered = df[df['state'].isin(state)]
        else:
            df_filtered = df[df['state'] == state]
    return [{'label': variety, 'value': variety} for variety in df_filtered['variety'].unique()]


@app.callback(
    Output('plots', 'srcDoc'),
    Input('province-widget', 'value'),
    Input('price', 'value'),
    Input('points', 'value'))
def plot_altair(selected_state, price_value, points_value):
    if selected_state == 'select your state':
        df_filtered = df
    else:
        if type(selected_state) == list:
            df_filtered = df[df['state'].isin(selected_state)]
        else:
            df_filtered = df[df['state'] == selected_state]
    # filterng data based on wine variety selection
    # if wine_variety == 'select a variety':
    #     df_filtered = df_filtered
    # else:
    #     if type(wine_variety) == list:
    #         df_filtered = df_filtered[df_filtered['variety'].isin(wine_variety)]
    #     else:  
    #         df_filtered = df_filtered.query("variety == @wine_variety")

    df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
    df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]

    data = df_filtered.groupby('variety')[['price', 'points']].mean()


    new_data = data.sort_values(by='price', ascending=False).head(10).reset_index()

    click = alt.selection_multi(fields=['variety'])
    
    ranked_bar1= (alt.Chart(new_data).mark_bar().encode(
        alt.X('variety' +':N', 
        sort=alt.EncodingSortField(
            field='points',  
            op="sum",  
            order='descending'
            )),
        alt.Y('points' + ':Q', title='Points',
        scale=alt.Scale(domain=[min(new_data['points']),
        max(new_data['points'])])),
        color=alt.Color('variety',scale=alt.Scale(scheme='bluepurple'), legend=None),
        opacity=alt.condition(click, alt.value(0.9), alt.value(0.2)))
.add_selection(click)).properties(width=300, height=300).interactive()

    
    ranked_bar = (alt.Chart(new_data).mark_bar().encode(
        alt.X('variety' +':N', 
        sort=alt.EncodingSortField(
            field='price',  
            op="sum",  
            order='descending'
            )),
        alt.Y('price' + ':Q', title='Price($)',
        scale=alt.Scale(domain=[min(new_data['price']),
        max(new_data['price'])])),
        color=alt.Color('variety',scale=alt.Scale(scheme='bluepurple'), legend=None),
        opacity=alt.condition(click, alt.value(0.9), alt.value(0.2)))
.add_selection(click)).properties(width=300, height=300) 
    chart = (ranked_bar1 | ranked_bar).configure_axisX(
                labelAngle=60)
    return chart.to_html()

@app.callback(
    Output('maps', 'srcDoc'),
    Input('province-widget', 'value'),
    Input('price', 'value'),
    Input('points', 'value'),
    Input('wine_variety', 'value'))
def plot_map(selected_state, price_value, points_value,wine_variety):
    if selected_state == 'select your state':
        df_filtered = df
    else:
        if type(selected_state) == list:
            df_filtered = df[df['state'].isin(selected_state)]
        else:
            df_filtered = df[df['state'] == selected_state]
    # filterng data based on wine variety selection
    if wine_variety == 'select a variety':
        df_filtered = df_filtered
    else:
        if type(wine_variety) == list:
            df_filtered = df_filtered[df_filtered['variety'].isin(wine_variety)]
        else:  
            df_filtered = df_filtered.query("variety == @wine_variety")

    state_map = alt.topo_feature(data.us_10m.url, 'states')
    df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
    df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]
    states_grouped = df_filtered.groupby(['state', 'state_id'], as_index=False)
    wine_states = states_grouped.agg({'points': ['mean'],
                                      'price': ['mean'],
                                      'value': ['mean'],
                                      'description': ['count']})

    wine_states.columns = wine_states.columns.droplevel(level=1)
    wine_states = wine_states.rename(columns={"state": "State",
                                              "state_id": "State ID",
                                              "description": "Num Reviews",
                                              "points": 'Ave Rating',
                                              "price": 'Ave Price',
                                              "value": 'Ave Value'})


    map_click = alt.selection_multi(fields=['State'])
    states = alt.topo_feature(data.us_10m.url, "states")

    
    colormap = alt.Scale(domain=[0, 100, 1000, 2000, 4000, 8000, 16000, 32000],
                         range=['#C7DBEA', '#CCCCFF', '#B8AED2', '#3A41C61',
                                '#9980D4', '#722CB7', '#663399', '#512888'])


    foreground = (alt.Chart(states).mark_geoshape().encode(
        color=alt.Color('Num Reviews:Q', scale=colormap), opacity=alt.condition(map_click, alt.value(1), alt.value(0.2)),

        tooltip=[alt.Tooltip('State:O'),
                 alt.Tooltip('Ave Rating:Q', format='.2f'),
                 alt.Tooltip('Ave Price:Q', format='$.2f'),
                 alt.Tooltip('Ave Value:Q', format='.2f'),
                 alt.Tooltip('Num Reviews:Q')]
    ).mark_geoshape(
        stroke='black',
        strokeWidth=0.5
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(wine_states,
                             'State ID',
                             ['State', 'State ID', 'Ave Rating', 'Ave Price', 'Ave Value', 'Num Reviews'])
    ).add_selection(map_click)
    ).project(
        type='albersUsa'
    )
    background = alt.Chart(states).mark_geoshape(
        fill='#EAEDED',
        stroke='dimgray'
    ).project(
        'albersUsa'
    )
    chart = (background + foreground).configure_view(
                height=400,
                width=570,
                strokeWidth=4,
                fill=None,
                stroke=None)
    return chart.to_html()

@app.callback(
    Output('table', 'data'),
    Input('table_state', 'value'),
    Input('table_price', 'value'),
    Input('table_points', 'value'),
    Input('table_variety', 'value'))
def table(state, price, points, variety):
    if state == 'select your state':
        df_filtered = display_df
    else:
        if type(state) == list:
            df_filtered = display_df[display_df['State'].isin(state)]
        else:
            df_filtered = display_df[display_df['State'] == state]
    if type(variety) == list:
        df_filtered = df_filtered[df_filtered['Variety'].isin(variety)]
    else:  
        df_filtered = df_filtered.query("Variety == @variety")   

    df_filtered = df_filtered[(df_filtered['Price'] >= min(price)) & (df_filtered['Price'] <= max(price))]
    df_filtered = df_filtered[(df_filtered['Points'] >= min(points)) & (df_filtered['Points'] <= max(points))]
   
    return df_filtered.to_dict('records')

@app.callback(
    Output('table_plots', 'srcDoc'),
    Input('table_state', 'value'),
    Input('table_price', 'value'),
    Input('table_points', 'value'),
    Input('table_variety', 'value'))
def table_plot(selected_state, price_value, points_value, wine_variety):
    if selected_state == 'select your state':
        df_filtered = df
    else:
        if type(selected_state) == list:
            df_filtered = df[df['state'].isin(selected_state)]
        else:
            df_filtered = df[df['state'] == selected_state]
    # filterng data based on wine variety selection
    if wine_variety == 'select a variety':
        df_filtered = df_filtered
    else:
        if type(wine_variety) == list:
            df_filtered = df_filtered[df_filtered['variety'].isin(wine_variety)]
        else:  
            df_filtered = df_filtered.query("variety == @wine_variety")
    df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
    df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]
    
    selection = alt.selection_multi(    
            fields=['variety'], # limit selection to the Major_Genre field
            bind='legend')

    select_price = alt.selection_interval(empty='all', encodings=['x'])
    select_points= alt.selection_interval(empty='all', encodings=['x'])

    multidim_legend = alt.Chart(df_filtered).mark_point(filled=True).encode(
        x=alt.X('state'),
        y=alt.Y('variety', axis=None),
        size =alt.Size('count()', legend=None),
        color = alt.Color('variety'),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
    ).add_selection(selection).properties(height=100, width=100)

    price_slider = alt.Chart(df_filtered).mark_bar().encode(
    alt.X('price', title='', axis=alt.Axis(grid=False),
          scale=alt.Scale(domain=[0, 110])),
    alt.Y('count()', title='', axis=None)
    ).properties(height=40, width=100).add_selection(select_price)

    points_slider = alt.Chart(df_filtered).mark_bar().encode(
    alt.X('points', title='', axis=alt.Axis(grid=False),
          scale=alt.Scale(domain=[75, 105])),
    alt.Y('count()', title='', axis=None)
    ).properties(height=40, width=100).add_selection(select_points)

    # text = alt.Chart(df_filtered).mark_text().encode(
    #     y=alt.y('title',axis=None))

    chart1 = alt.Chart(df_filtered).mark_point().encode(
        x=alt.X('price', scale=alt.Scale(zero=False)),
        y=alt.Y('points', scale=alt.Scale(zero=False)),
        color = alt.Color('variety'),#, scale=alt.Scale(scheme='bluepurple')),
        opacity = alt.condition(select_price & select_points & selection, alt.value(0.5), alt.value(0)),
        tooltip='title').add_selection(selection).interactive()
    
    chart = chart1|(price_slider & points_slider & multidim_legend)

    return chart.to_html()

@app.callback(
    Output('table_state', 'value'),
    Output('table_variety', 'value'),
    Output('table_points', 'value'),
    Output('table_price', 'value'),
    Input('province-widget', 'value'),
    Input('wine_variety', 'value'),
    Input('points', 'value'),
    Input('price', 'value'))
def cross_tab_update_price(state, variety, points, price):
    return state, variety, points, price

@app.callback(
    Output('heat_plot', 'srcDoc'),
    Input('province-widget', 'value'),
    Input('price', 'value'),
    Input('points', 'value'))
def plot_heat(selected_state, price_value, points_value):
    if selected_state == 'select your state':
        df_filtered = df
    else:
        if type(selected_state) == list:
            df_filtered = df[df['state'].isin(selected_state)]
        else:
            df_filtered = df[df['state'] == selected_state]
    df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
    df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]

    variety_df = df_filtered.groupby(['variety']).size().reset_index(name='counts')
    variety_df = variety_df.sort_values(by='counts')
    popular_varieties = variety_df.query('counts > 500')['variety']

    # Filter the data set to include only popular grape varieties
    varieties_plot_data = df_filtered[df_filtered['variety'].isin(popular_varieties.tolist())]
    varieties_heatmap_plot = alt.Chart(varieties_plot_data.query('price < 100')).mark_rect().encode(
    x=alt.X("price" + ':Q',
                    bin=alt.Bin(maxbins=10),
                    title="Price ($)"),
            y=alt.Y('variety:O', 
                    title="Grape Variety"),
            color=alt.Color('average(price):Q',
                            scale=alt.Scale(scheme="bluepurple"),
            legend=alt.Legend(
                            orient='right', title="Average Value")
                        ),
            tooltip=[alt.Tooltip('average(points):Q', format='.2f'),
                     alt.Tooltip('average(price)', format='$.2f'),
                     alt.Tooltip('average(value)', format='.2f'),
                     alt.Tooltip('count(title)')]
    ).properties(
            title="Average price for Popular Grape Varieties"
    ).configure_axis(
            grid=False,
            labelAngle=0). properties(width=300, height=300)
    return varieties_heatmap_plot.to_html()



if __name__ == '__main__':
    app.run_server(debug=True)