import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
from dash import Input, Output

dash.register_page(__name__, path='/US-dashboard')

S_P500 = pd.read_csv('Data/US_Data/SP500.csv')

fig_SP500 = px.line(S_P500, x='Time', y='Price', title='S&P 500 Closing Prices Over Time')


NASDAQ = pd.read_csv('Data/US_Data/NASDAQ100.csv')

fig_NASDAQ = px.line(NASDAQ, x='Time', y='Price', title='NASDAQ 100 Closing Prices Over Time')


GDP= pd.read_csv('Data/US_Data/GDP.csv')

fig_GDP = px.line(GDP, x='Time', y='GDP', title='US GDP Over Time')


Inflation= pd.read_csv('Data/US_Data/Inflation_Dataset.csv')

fig_Inflation = px.line(Inflation, x='Time', y='Inflation', title='US Inflation Over Time')

Unemployment= pd.read_csv('Data/US_Data/Unemployement_Dataset.csv')

fig_Unemployment = px.line(Unemployment, x='Time', y='Unemployement_Rate', title='US Unemployment Over Time')


Debts= pd.read_csv('Data/US_Data/Debts.csv')

fig_Debts = px.line(Debts, x='Time', y='Debts_Rate', title='US Debt Over Time')



layout= html.Div([
    html.H2('US Dashboard'),
    html.H3('S&P 500 Closing Prices Over Time'),
    dcc.Graph(figure=fig_SP500),
    html.H3('NASDAQ 100 Closing Prices Over Time'),
    dcc.Graph(figure=fig_NASDAQ),
    html.H3('US GDP Over Time'),
    dcc.Graph(figure=fig_GDP),
    html.H3('US Inflation Over Time'),
    dcc.Graph(figure=fig_Inflation),
    html.H3('US Unemployment Over Time'),
    dcc.Graph(figure=fig_Unemployment),
    html.H3('US Debt Over Time'),
    dcc.Graph(figure=fig_Debts),
    html.H3('Conclusion'),
    html.P('Thanks to the data we can see that the impact of the covid on the US economy wasn\'t as severe as expected. Indeed, the covid has enabled a huge growth of tech compagny like amazon, google and the US economy is drived by those big compagny so the impact of the crisis was limited by that but if the look to the unemployement rate, we can see that the US struggled more on social impact of the crisis with a longer time to go back to the previous level.')
])