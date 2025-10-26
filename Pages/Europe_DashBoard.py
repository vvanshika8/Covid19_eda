import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
from dash import Input, Output

STOCKXX_600 = pd.read_csv('Data/Europe_Data/STOXX 600 Historical Data (1).csv')
STOCKXX_600['Date'] = pd.to_datetime(STOCKXX_600['Date'])
STOCKXX_600_sorted = STOCKXX_600.sort_values(by='Date', ascending=True)


fig = px.line(STOCKXX_600, x='Date', y='Price', title='StockXX 600 Closing Prices Over Time')

dash.register_page(__name__, path='/europe-dashboard')

GDP_Data = pd.read_csv('Data/Europe_Data/GDP_Dataset.csv')

time_col = GDP_Data.columns[0]  # la première colonne pour le temps
countries = GDP_Data.columns[6:]  # les colonnes suivantes sont les pays (noms colonnes)
countries = [GDP_Data.columns[1]] + GDP_Data.columns[6:].tolist()

countries_2 = GDP_Data.columns[6:]
# Extract GDP data for 2019 and 2022
gdp_2019 = GDP_Data[GDP_Data['Time'] == 2019][countries_2].T.reset_index()
gdp_2022 = GDP_Data[GDP_Data['Time'] == 2022][countries_2].T.reset_index()

# Rename columns for clarity
gdp_2019.columns = ['Country', 'GDP']
gdp_2022.columns = ['Country', 'GDP']

all_countries = pd.concat([gdp_2019['Country'], gdp_2022['Country']]).unique()

# Define colors (you can define specific colors or generate them)
import plotly.colors as plc
colors = plc.qualitative.Safe  # example qualitative color palette

# If more countries than colors, extend colors list
base_colors = plc.qualitative.Dark24

import itertools
# Repeat colors if countries exceed palette length
colors = list(itertools.islice(itertools.cycle(base_colors), len(all_countries)))

# Create mapping dictionary
color_map = dict(zip(all_countries, colors))

# Create pie charts with Plotly Express
fig_2019 = px.pie(gdp_2019, names='Country', values='GDP', title='GDP by Country (2019)', 
                  color='Country', color_discrete_map=color_map)

fig_2022 = px.pie(gdp_2022, names='Country', values='GDP', title='GDP by Country (2022)', 
                  color='Country', color_discrete_map=color_map)

fig_2019.update_traces(textinfo='none', hovertemplate='%{label}: %{percent:.1%}')
fig_2022.update_traces(textinfo='none', hovertemplate='%{label}: %{percent:.1%}')


Influation_Data = pd.read_csv('Data/Europe_Data/Inflation_Dataset.csv')
time_col_Inf = Influation_Data.columns[0]  # la première colonne pour le temps
countries_Inf = Influation_Data.columns[1:]

Freet_Data = pd.read_csv('Data/Europe_Data/Freet_Dataset.csv')
time_col_Freet = Freet_Data.columns[0]  # la première colonne pour le temps
countries_Freet = Freet_Data.columns[1:]
Freet_Data[countries_Freet] = Freet_Data[countries_Freet].apply(pd.to_numeric, errors='coerce')

Tourism_Data = pd.read_csv('Data/Europe_Data/Tourism_Dataset.csv')
time_col_Tourism = Tourism_Data.columns[0]  # la première colonne pour le temps
countries_Tourism = Tourism_Data.columns[1:]
Tourism_Data[countries_Tourism] = Tourism_Data[countries_Tourism].apply(pd.to_numeric, errors='coerce')

Debts_Data = pd.read_csv('Data/Europe_Data/Debts_Dataset.csv')
time_col_Debts = Debts_Data.columns[0]  # la première colonne pour le temps
countries_Debts = Debts_Data.columns[1:]

Unemployment= pd.read_csv('Data/Europe_Data/Unemployment_Dataset.csv')
time_col_Unemployment = Unemployment.columns[0]  # la première colonne pour le temps
countries_Unemployment = Unemployment.columns[1:]
Unemployment[countries_Unemployment] = Unemployment[countries_Unemployment].apply(pd.to_numeric, errors='coerce')

Poverty= pd.read_csv('Data/Europe_Data/Poverty_Dataset.csv')
time_col_Poverty = Poverty.columns[0]  # la première colonne pour le temps
countries_Poverty = Poverty.columns[1:]
Poverty[countries_Poverty] = Poverty[countries_Poverty].apply(pd.to_numeric, errors='coerce')

# Load the dataset
df = pd.read_excel('Data/Europe_Data/Aids_Dataset.xlsx', sheet_name='Sheet1')

# Convert the data to long format
long_df = df.melt(id_vars='Country', var_name='Category', value_name='Value')

# Create the bar plot
fig_Aids = px.bar(long_df, x='Country', y='Value', color='Category', barmode='group')
fig_Aids.update_layout(title='Financial support by Country during Covid',
                       yaxis_title='Amount (in % of GDP)',
                       xaxis_title='Country')


layout = html.Div([
    html.H2('Analytics'),
    html.H3('STOXX 600 Closing Prices Over Time'),
    dcc.Graph(figure=fig),
    html.H3('GDP Over Time by Country'),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in countries],  # liste des pays
        value=countries[0],
        multi=True   # valeur par défaut
    ),
    dcc.Graph(id='gdp-graph'),
    html.H3('GDP Distribution in 2019 and 2022'),
        html.Div([
        html.Div([dcc.Graph(figure=fig_2019)], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(figure=fig_2022)], style={'width': '48%', 'display': 'inline-block'})
    ]),
    dcc.Dropdown(
        id='country-dropdown-inf',
        options=[{'label': c, 'value': c} for c in countries_Inf],  # liste des pays
        value=countries_Inf[0],
        multi=True, # valeur par défaut
    ),
    dcc.Graph(id='inflation-graph'),
    html.H3('Gross weight of goods transported Over Time by Country'),
    dcc.Dropdown(
        id='country-dropdown-freet',
        options=[{'label': c, 'value': c} for c in countries_Freet],  # liste des pays
        value=countries_Freet[0],
        multi=True   # valeur par défaut
    ),
    dcc.Graph(id='freet-graph'),
    html.H3('Tourism Over Time by Country'),
    dcc.Dropdown(
        id='country-dropdown-tourism',
        options=[{'label': c, 'value': c} for c in countries_Tourism],  # liste des pays
        value=countries_Tourism[0],
        multi=True   # valeur par défaut
    ),
    dcc.Graph(id='tourism-graph'),
    html.H3('Debts Over Time by Country'),
    dcc.Dropdown(
        id='country-dropdown-debts',
        options=[{'label': c, 'value': c} for c in countries_Debts],  # liste des pays
        value=countries_Debts[0],
        multi=True   # valeur par défaut
    ),
    dcc.Graph(id='debts-graph'),
    html.H3('Unemployment Over Time by Country'),
    dcc.Dropdown(
        id='country-dropdown-unemployment',
        options=[{'label': c, 'value': c} for c in countries_Unemployment],  # liste des pays
        value=countries_Unemployment[0],
        multi=True   # valeur par défaut
    ),
    dcc.Graph(id='unemployment-graph'),
    html.H3('Poverty Over Time by Country'),
    dcc.Dropdown(
        id='country-dropdown-poverty',
        options=[{'label': c, 'value': c} for c in countries_Poverty],  # liste des pays
        value=countries_Poverty[0],
        multi=True   # valeur par défaut
    ),
    dcc.Graph(id='poverty-graph'),
    html.H3('Financial support by Country during Covid'),
    dcc.Graph(figure=fig_Aids),
    html.H3('Conclusion'),
    html.P('The European economy was at the start of the covid impact, indeed key indicators such as GDP, Inflation, Unemployment, and Poverty all showed significant changes during this period. The GDP saw a notable decline in 2020, but we had a rebound in the following years, depending of Country payement the rebound was more or less important but all countries were able to recover. Inflation rates spiked in 2022 but it is hard to determine if this was a direct result of the pandemic but the destabilization of the economy certainly played a role. We have seen with the data that tourism was heavily impacted during the pandemic more than other sectors like freet transport which showed more resilience.')
])

@dash.callback(
    Output('gdp-graph', 'figure'),
    [Input('country-dropdown', 'value'),]
)

def update_graph(selected_country):
    fig = px.line(
        GDP_Data,
        x=time_col,
        y=selected_country,
        title=f'GDP of {selected_country} Over Time'
    )
    fig.update_layout(
    yaxis_title="GDP (millions of euros)")
    return fig

@dash.callback(
    Output('inflation-graph', 'figure'),
    [Input('country-dropdown-inf', 'value'),])

def update_inflation_graph(selected_country_inf):
    fig_inf = px.line(
        Influation_Data,
        x=time_col_Inf,
        y=selected_country_inf,
        title=f'Inflation of {selected_country_inf} Over Time'
    )
    fig_inf.update_layout(
    yaxis_title="Inflation rate (% of GDP)",
     )
    
    return fig_inf

@dash.callback(
    Output('freet-graph', 'figure'),
    [Input('country-dropdown-freet', 'value'),])

def update_freet_graph(selected_country_freet):
    fig_freet = px.line(
        Freet_Data,
        x=time_col_Freet,
        y=selected_country_freet,
        title=f'Gross weight of goods transported of {selected_country_freet} Over Time'
    )
    fig_freet.update_layout(
    yaxis_title="Gross weight of goods transported (1000 tonnes)",
    )
    return fig_freet

@dash.callback(
    Output('tourism-graph', 'figure'),
    [Input('country-dropdown-tourism', 'value'),])

def update_tourism_graph(selected_country_tourism):
    fig_tourism = px.line(
        Tourism_Data,
        x=time_col_Tourism,
        y=selected_country_tourism,
        title=f'Tourism of {selected_country_tourism} Over Time'
    )
    fig_tourism.update_layout(
    yaxis_title="Arrivals at tourist accommodation establishments",
     )
    return fig_tourism

@dash.callback(
    Output('debts-graph', 'figure'),
    [Input('country-dropdown-debts', 'value'),])

def update_debts_graph(selected_country_debts):
    fig_debts = px.line(
        Debts_Data,
        x=time_col_Debts,
        y=selected_country_debts,
        title=f'Debts of {selected_country_debts} Over Time'
    )
    fig_debts.update_layout(
    yaxis_title="Debt (% of GDP)"

)
    return fig_debts

@dash.callback(
    Output('unemployment-graph', 'figure'),
    [Input('country-dropdown-unemployment', 'value'),])

def update_unemployment_graph(selected_country_unemployment):
    fig_unemployment = px.line(
        Unemployment,
        x=time_col_Unemployment,
        y=selected_country_unemployment,
        title=f'Unemployment of {selected_country_unemployment} Over Time'
    )
    fig_unemployment.update_layout(
    yaxis_title="Unemployment Rate (%)",
    
)
    return fig_unemployment

@dash.callback(
    Output('poverty-graph', 'figure'),
    [Input('country-dropdown-poverty', 'value'),])

def update_poverty_graph(selected_country_poverty):
    fig_poverty = px.line(
        Poverty,
        x=time_col_Poverty,
        y=selected_country_poverty,
        title=f'Poverty of {selected_country_poverty} Over Time'
    )
    fig_poverty.update_layout(
    yaxis_title="At risk of poverty or social exclusion (%)",

)
    return fig_poverty