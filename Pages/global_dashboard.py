import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Load Datasets
# --------------------------------------------------
GDP_df = pd.read_csv("Data/World_Data/API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2_23243.csv", skiprows=4)
Inflation_df = pd.read_csv("Data/World_Data/API_FP.CPI.TOTL.ZG_DS2_en_csv_v2_23195.csv", skiprows=4)
Unemployment_df = pd.read_csv("Data/World_Data/API_SL.UEM.TOTL.ZS_DS2_en_csv_v2_25091.csv", skiprows=4)
Health_df = pd.read_csv("Data/World_Data/worldometer_coronavirus_daily_data.csv") 

# --------------------------------------------------
# Clean and Prepare Data
# --------------------------------------------------
Health_df.columns = Health_df.columns.str.strip().str.lower()

# Year columns for economic datasets
year_cols = [col for col in GDP_df.columns if col.isdigit()]
# Only years >= 2017
year_cols_filtered = [col for col in year_cols if int(col) >= 2017]

# List of countries
countries = GDP_df["Country Name"].dropna().unique()

# Ensure date is datetime for health data
Health_df["date"] = pd.to_datetime(Health_df["date"], errors="coerce")
health_countries = Health_df["country"].dropna().unique()

# --------------------------------------------------
# Register Dash Page (only if app exists)
# --------------------------------------------------

dash.register_page(__name__, path="/global-dashboard")

# --------------------------------------------------
# Layout
# --------------------------------------------------
layout = html.Div([
    html.H1("🌍 Global Economic & Health Dashboard", style={'textAlign': 'center', 'marginBottom': 30}),

    # GDP Section
    html.H3("Global GDP Growth Rate Over Time (%)"),
    dcc.Dropdown(
        id="country-dropdown-gdp-global",
        options=[{"label": c, "value": c} for c in countries],
        value=["France", "India", "United States"],
        multi=True,
        style={"width": "60%"}
    ),
    dcc.Graph(id="gdp-graph-global"),

    # Inflation Section
    html.H3("Global Inflation Rate Over Time (%)"),
    dcc.Dropdown(
        id="country-dropdown-inflation-global",
        options=[{"label": c, "value": c} for c in countries],
        value=["France", "India", "United States"],
        multi=True,
        style={"width": "60%"}
    ),
    dcc.Graph(id="inflation-graph-global"),

    # Unemployment Section
    html.H3("Global Unemployment Rate Over Time (%)"),
    dcc.Dropdown(
        id="country-dropdown-unemployment-global",
        options=[{"label": c, "value": c} for c in countries],
        value=["France", "India", "United States"],
        multi=True,
        style={"width": "60%"}
    ),
    dcc.Graph(id="unemployment-graph-global"),

    # Health Section
    html.H3("Global COVID-19 Health Statistics"),
    dcc.Dropdown(
        id="country-dropdown-health-global",
        options=[{"label": c, "value": c} for c in health_countries],
        value=["India", "France", "United States"],
        multi=True,
        style={"width": "60%"}
    ),
    dcc.RadioItems(
        id="health-metric-radio-global",
        options=[
            {"label": "Daily New Cases", "value": "daily_new_cases"},
            {"label": "Active Cases", "value": "active_cases"},
            {"label": "Daily New Deaths", "value": "daily_new_deaths"},
        ],
        value="daily_new_cases",
        inline=True,
        style={"marginBottom": "10px"}
    ),
    dcc.Graph(id="health-graph-global"),
])

# --------------------------------------------------
# Callbacks
# --------------------------------------------------

@dash.callback(
    Output("gdp-graph-global", "figure"),
    [Input("country-dropdown-gdp-global", "value")]
)
def update_gdp(selected_countries):
    filtered = GDP_df[GDP_df["Country Name"].isin(selected_countries)]
    gdp_melted = filtered.melt(
        id_vars=["Country Name"],
        value_vars=year_cols_filtered,
        var_name="Year",
        value_name="GDP Growth (%)"
    )
    fig = px.line(
        gdp_melted,
        x="Year",
        y="GDP Growth (%)",
        color="Country Name",
        title="GDP Growth Rate Over Time"
    )
    return fig


@dash.callback(
    Output("inflation-graph-global", "figure"),
    [Input("country-dropdown-inflation-global", "value")]
)
def update_inflation(selected_countries):
    filtered = Inflation_df[Inflation_df["Country Name"].isin(selected_countries)]
    inflation_melted = filtered.melt(
        id_vars=["Country Name"],
        value_vars=year_cols_filtered,
        var_name="Year",
        value_name="Inflation (%)"
    )
    fig = px.line(
        inflation_melted,
        x="Year",
        y="Inflation (%)",
        color="Country Name",
        title="Inflation Rate Over Time"
    )
    return fig


@dash.callback(
    Output("unemployment-graph-global", "figure"),
    [Input("country-dropdown-unemployment-global", "value")]
)
def update_unemployment(selected_countries):
    filtered = Unemployment_df[Unemployment_df["Country Name"].isin(selected_countries)]
    unemployment_melted = filtered.melt(
        id_vars=["Country Name"],
        value_vars=year_cols_filtered,
        var_name="Year",
        value_name="Unemployment (%)"
    )
    fig = px.line(
        unemployment_melted,
        x="Year",
        y="Unemployment (%)",
        color="Country Name",
        title="Unemployment Rate Over Time"
    )
    return fig


@dash.callback(
    Output("health-graph-global", "figure"),
    [Input("country-dropdown-health-global", "value"),
     Input("health-metric-radio-global", "value")]
)
def update_health(selected_countries, metric):
    filtered = Health_df[
        (Health_df["country"].isin(selected_countries)) &
        (Health_df["date"].dt.year >= 2017)
    ]
    fig = px.line(
        filtered,
        x="date",
        y=metric,
        color="country",
        title=f"{metric.replace('_', ' ').title()} Over Time"
    )
    fig.update_layout(xaxis_title="Date", yaxis_title=metric.replace("_", " ").title())
    return fig

# --------------------------------------------------
# Run standalone (optional)
# --------------------------------------------------
if __name__ == "__main__":
    from dash import Dash
    app = Dash(__name__)
    app.layout = layout
    app.run_server(debug=True)
