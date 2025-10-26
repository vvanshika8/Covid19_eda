# new_projet.py: Application Dash pour l'Analyse Comparative (Version Finale)

# 1. INSTALLATION ET IMPORTATIONS
# -------------------------------------------------------------------------------------

import dash
from dash import dcc, html, Input, Output, State, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os 
import numpy as np
import json 

# --- Chemins de vos fichiers locaux (CORRIGÉS) ---
# Le dossier 'data' doit se trouver dans le même répertoire que ce script.
DATA_DIR = "Data/Djamel_Data" 
OXCGRT_FILE = 'stringency_index_avg.xlsx' 
UNEMPLOYMENT_FILE = 'unemployment_data.csv'

# Construction des chemins complets (Compatible Windows/Linux/macOS)
OXCGRT_PATH = os.path.join(DATA_DIR, OXCGRT_FILE)
UNEMPLOYMENT_PATH = os.path.join(DATA_DIR, UNEMPLOYMENT_FILE)

START_YEAR = 2020
END_YEAR = 2023 

# --- SÉLECTION SPÉCIFIQUE DES 9 PAYS ---
TARGET_COUNTRIES_LIST = [
    {'CountryName': 'France', 'IncomeGroup_Custom': '1 - Haut Revenu'},
    {'CountryName': 'United Kingdom', 'IncomeGroup_Custom': '1 - Haut Revenu'},
    {'CountryName': 'Japan', 'IncomeGroup_Custom': '1 - Haut Revenu'},
    {'CountryName': 'Brazil', 'IncomeGroup_Custom': '2 - Émergent (Interm. Sup.)'},
    {'CountryName': 'China', 'IncomeGroup_Custom': '2 - Émergent (Interm. Sup.)'},
    {'CountryName': 'South Africa', 'IncomeGroup_Custom': '2 - Émergent (Interm. Sup.)'},
    {'CountryName': 'Ethiopia', 'IncomeGroup_Custom': '3 - Faible Revenu'},
    {'CountryName': 'Sudan', 'IncomeGroup_Custom': '3 - Faible Revenu'},
    {'CountryName': 'Yemen', 'IncomeGroup_Custom': '3 - Faible Revenu'},
]
df_target = pd.DataFrame(TARGET_COUNTRIES_LIST)
target_countries = df_target['CountryName'].tolist()


# 2. INITIALISATION DE L'APPLICATION DASH
# -------------------------------------------------------------------------------------

dash.register_page(__name__, path="/djamel-dashboard")


# 3. MISE EN PAGE : CORRIGÉE
# -------------------------------------------------------------------------------------

layout = html.Div([ 
    html.H2("Analyse Dynamique des 9 Pays : Rigueur Politique vs. Taux de Chômage", style={'textAlign': 'center', 'color': '#8B4513'}),
    html.P("Comparaison mensuelle des indices de politique et du chômage pour les trois groupes de revenus ciblés.", style={'textAlign': 'center', 'marginBottom': '10px'}),

    dcc.Store(id='stored-data'),
    html.Div(id='loading-error-message', style={'textAlign': 'center', 'color': 'red', 'fontSize': '1.2em'}),

    # CONTRÔLES (Utilisation correcte de style et children)
    html.Div(
        id='controls-container', 
        style={
            'display': 'none', 
            'padding': '10px', 
            'backgroundColor': '#f0f0f0', 
            'borderRadius': '5px', 
            'margin-bottom': '20px', 
            'width': '80%', 
            'margin-left': 'auto', 
            'margin-right': 'auto'
        }, 
        children=[
            html.Div([
                html.Label("1. Indicateur Politique (Axe X):", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='x-axis-selector',
                    options=[{'label': 'Indice de Rigueur (OxCGRT)', 'value': 'Stringency_Index'}],
                    value='Stringency_Index',
                    clearable=False
                )
            ], style={'width': '30%', 'display': 'inline-block', 'margin-right': '5%'}),

            html.Div([
                html.Label("2. Regroupement (Couleur) :", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='color-selector',
                    options=[
                        {'label': 'Groupe de Revenu', 'value': 'IncomeGroup_Custom'},
                        {'label': 'Pays', 'value': 'CountryName'},
                        {'label': 'Année', 'value': 'Year:nominal'}
                    ],
                    value='IncomeGroup_Custom',
                    clearable=False
                )
            ], style={'width': '30%', 'display': 'inline-block', 'margin-right': '5%'}),

            html.Div([
                html.Label("3. Animation Temporelle :", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='animation-selector',
                    options=[
                        {'label': 'Année-Mois', 'value': 'Year_Month'},
                        {'label': 'Année', 'value': 'Year'}
                    ],
                    value='Year_Month',
                    clearable=False
                )
            ], style={'width': '30%', 'display': 'inline-block'}),
        ] 
    ),

    # GRAPHIQUE PRINCIPAL
    dcc.Graph(id='main-scatter-plot', style={'height': '70vh'}),
]) 


# 4. CALLBACK 1 : Chargement et Stockage des Données
# -------------------------------------------------------------------------------------

@dash.callback(
    Output('stored-data', 'data'),
    Output('loading-error-message', 'children'),
    Output('controls-container', 'style'), 
    Input('stored-data', 'id') 
)
def load_and_store_data(_):
    """Charge, prépare et stocke les données dans le dcc.Store."""
    try:
        # Utilisation de encoding='latin-1' pour résoudre l'erreur Unicode
        
        # --- 2.1. Chargement de l'Indice de Rigueur (OxCGRT) ---
        df_oxcgrt = pd.read_excel(OXCGRT_PATH,sheet_name='Sheet1') 
        id_vars_oxcgrt = ['country_code', 'country_name', 'region_code', 'region_name', 'jurisdiction']
        
        df_oxcgrt = df_oxcgrt.melt(
            id_vars=id_vars_oxcgrt, var_name='Date_Raw', value_name='Stringency_Index'
        )
        
        df_oxcgrt['Date'] = pd.to_datetime(df_oxcgrt['Date_Raw'], format='%d%b%Y', errors='coerce')
        df_oxcgrt = df_oxcgrt.dropna(subset=['Date', 'Stringency_Index'])
        
        df_oxcgrt['Year'] = df_oxcgrt['Date'].dt.year
        df_oxcgrt['Year_Month'] = df_oxcgrt['Date'].dt.to_period('M').astype(str)
        df_oxcgrt = df_oxcgrt.rename(columns={'country_name': 'CountryName'})
        
        df_policy_monthly = df_oxcgrt.groupby(['CountryName', 'Year_Month', 'Year'])['Stringency_Index'].mean().reset_index()
        df_policy_monthly = df_policy_monthly[df_policy_monthly['CountryName'].isin(target_countries)]
        
        # --- 2.2. Chargement des Données de Chômage (ILOSTAT) ---
        df_unemployment_raw = pd.read_csv(UNEMPLOYMENT_PATH, skiprows=4, encoding='latin-1')

        df_unemployment = df_unemployment_raw.melt(
            id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'],
            value_vars=[str(y) for y in range(START_YEAR, END_YEAR + 1)],
            var_name='Year',
            value_name='Unemployment_Rate'
        ).dropna(subset=['Unemployment_Rate'])

        df_unemployment['Year'] = df_unemployment['Year'].astype(int)
        df_unemployment = df_unemployment.rename(columns={'Country Name': 'CountryName'})
        df_unemployment = df_unemployment[df_unemployment['CountryName'].isin(target_countries)][['CountryName', 'Year', 'Unemployment_Rate']]

        # --- 2.3. Fusion Finale ---
        df_final = pd.merge(df_policy_monthly, df_unemployment, on=['CountryName', 'Year'], how='left')
        df_final = df_final.dropna(subset=['Unemployment_Rate', 'Stringency_Index'])
        df_final = pd.merge(df_final, df_target, on='CountryName', how='left')
        
        if df_final.empty:
             raise ValueError("Le DataFrame final est vide après le filtrage. Vérifiez la correspondance des noms de pays.")

        # Sérialiser en JSON
        data_json = df_final.to_json(orient='split')
        print(f"Fusion terminée. Nombre d'observations : {len(df_final)}. Prêt pour l'affichage.")
        
        # Succès : Retourne les données et affiche les contrôles
        return data_json, "", {
            'padding': '10px', 
            'backgroundColor': '#f0f0f0', 
            'borderRadius': '5px', 
            'margin-bottom': '20px', 
            'width': '80%', 
            'margin-left': 'auto', 
            'margin-right': 'auto'
        }

    except (FileNotFoundError, ValueError) as e:
        error_msg = f"❌ ERREUR DE CHARGEMENT : {e}"
        print(error_msg)
        # Échec : Retourne des données vides et cache les contrôles
        return None, error_msg, {'display': 'none'}
    except Exception as e:
        error_msg = f"❌ ERREUR FATALE LORS DU TRAITEMENT : {e}"
        print(error_msg)
        return None, error_msg, {'display': 'none'}


# 5. CALLBACK 2 : Mise à Jour du Graphique à partir des Données Stockées (CORRIGÉ)
# -------------------------------------------------------------------------------------

@dash.callback(
    Output('main-scatter-plot', 'figure'),
    [
        Input('x-axis-selector', 'value'),
        Input('color-selector', 'value'),
        Input('animation-selector', 'value')
    ], # Correction de la SyntaxError: unterminated string literal
    State('stored-data', 'data') 
)
def update_graph(x_col, color_col, animation_col, data_json):
    
    if data_json is None:
        return go.Figure().update_layout(title="ERREUR: Le chargement des données a échoué. Voir le message d'erreur ci-dessus.", height=500)
    
    df_final = pd.read_json(data_json, orient='split')
    df_final['Year'] = df_final['Year'].astype(str)
    
    plot_color_col = color_col.split(':')[0]
    
    fig = px.scatter(
        df_final, 
        x=x_col, 
        y='Unemployment_Rate',
        color=plot_color_col,
        animation_frame=animation_col,
        hover_data=['CountryName', 'IncomeGroup_Custom', 'Year', 'Unemployment_Rate'],
        size=x_col, 
        title=f"Rigueur Politique vs. Taux de Chômage ({df_final['Year'].min()} - {df_final['Year'].max()})",
        labels={
            'Unemployment_Rate': 'Taux de Chômage (ILO/BM, %)',
            'Stringency_Index': 'Indice de Rigueur OxCGRT'
        },
        template='plotly_white'
    )

    fig.update_layout(
        transition_duration=500,
        xaxis_range=[-5, 105], 
        yaxis_title='Taux de Chômage (%)',
        xaxis_title='Indice de Rigueur OxCGRT'
    )
    fig.update_traces(marker=dict(size=15, opacity=0.7, line=dict(width=1, color='DarkSlateGrey')))
    
    return fig

# 6. EXÉCUTION DE L'APPLICATION
# -------------------------------------------------------------------------------------
