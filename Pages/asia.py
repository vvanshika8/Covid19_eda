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
year_cols_filtered = [col for col in year_cols if int(col) >= 2017]

# Focused countries
countries_focus = ["China", "Japan", "South Korea"]

# Ensure date is datetime for health data
Health_df["date"] = pd.to_datetime(Health_df["date"], errors="coerce")

# --------------------------------------------------
# Register Dash Page
# --------------------------------------------------
dash.register_page(__name__, path="/asia-dashboard")

# --------------------------------------------------
# Layout
# --------------------------------------------------
layout = html.Div([
    html.H1("🌏 Asia Economic & Health Dashboard", style={'textAlign': 'center', 'marginBottom': 30}),

    # GDP Section
    html.H3("GDP Growth Rate Over Time (%)"),
    dcc.Graph(id="gdp-graph-asia"),

    # Inflation Section
    html.H3("Inflation Rate Over Time (%)"),
    dcc.Graph(id="inflation-graph-asia"),

    # Unemployment Section
    html.H3("Unemployment Rate Over Time (%)"),
    dcc.Graph(id="unemployment-graph-asia"),

    # Health Section
    html.H3("COVID-19 Health Statistics"),
    dcc.RadioItems(
        id="health-metric-radio-asia",
        options=[
            {"label": "Daily New Cases", "value": "daily_new_cases"},
            {"label": "Active Cases", "value": "active_cases"},
            {"label": "Daily New Deaths", "value": "daily_new_deaths"},
        ],
        value="daily_new_cases",
        inline=True,
        style={"marginBottom": "10px"}
    ),
    dcc.Graph(id="health-graph-asia"),
])

# --------------------------------------------------
# Callbacks
# --------------------------------------------------
@dash.callback(
    Output("gdp-graph-asia", "figure"),
    Input("gdp-graph-asia", "id")  # dummy input to trigger callback
)
def update_gdp_asia(_):
    filtered = GDP_df[GDP_df["Country Name"].isin(countries_focus)]
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
        title="GDP Growth Rate Over Time (China, Japan, South Korea)"
    )
    return fig

@dash.callback(
    Output("inflation-graph-asia", "figure"),
    Input("inflation-graph-asia", "id")
)
def update_inflation_asia(_):
    filtered = Inflation_df[Inflation_df["Country Name"].isin(countries_focus)]
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
        title="Inflation Rate Over Time (China, Japan, South Korea)"
    )
    return fig

@dash.callback(
    Output("unemployment-graph-asia", "figure"),
    Input("unemployment-graph-asia", "id")
)
def update_unemployment_asia(_):
    filtered = Unemployment_df[Unemployment_df["Country Name"].isin(countries_focus)]
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
        title="Unemployment Rate Over Time (China, Japan, South Korea)"
    )
    return fig

@dash.callback(
    Output("health-graph-asia", "figure"),
    Input("health-metric-radio-asia", "value")
)
def update_health_asia(metric):
    filtered = Health_df[
        (Health_df["country"].isin(countries_focus)) &
        (Health_df["date"].dt.year >= 2017)
    ]
    fig = px.line(
        filtered,
        x="date",
        y=metric,
        color="country",
        title=f"{metric.replace('_', ' ').title()} Over Time (China, Japan, South Korea)"
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
