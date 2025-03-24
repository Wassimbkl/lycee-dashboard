import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Charger les fichiers CSV
annuaire_df = pd.read_csv("Data/annuaire-de-leducation.csv", sep=";", dtype=str)
resultats_df = pd.read_csv("Data/fr-en-indicateurs-de-resultat-des-lycees-gt_v2.csv", sep=";", dtype=str)

# Filtrer sur l'Île-de-France (Code région : 11)
annuaire_df = annuaire_df[annuaire_df['Code_region'] == '11']
resultats_df = resultats_df[resultats_df['Code region'] == '11']

# Nettoyage des données
annuaire_df['latitude'] = pd.to_numeric(annuaire_df['latitude'], errors='coerce')
annuaire_df['longitude'] = pd.to_numeric(annuaire_df['longitude'], errors='coerce')
resultats_df['Taux de reussite - Toutes series'] = pd.to_numeric(resultats_df['Taux de reussite - Toutes series'], errors='coerce')

# Fusionner les données sur l'identifiant UAI
lycees_df = pd.merge(annuaire_df, resultats_df, left_on='Identifiant_de_l_etablissement', right_on='UAI', how='inner')

# Créer l'application Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Mise en page du tableau de bord
app.layout = dbc.Container([
    html.H1("Tableau de bord des Lycées en Île-de-France", className="text-center mt-4"),
    
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='dropdown-departement',
                options=[{'label': dep, 'value': dep} for dep in sorted(lycees_df['Libelle_departement'].dropna().unique())],
                placeholder="Sélectionnez un département"
            ),
        ], width=4),
        
        dbc.Col([
            dcc.Dropdown(
                id='dropdown-ville',
                options=[],
                placeholder="Sélectionnez une ville"
            ),
        ], width=4),
        
        dbc.Col([
            dcc.Dropdown(
                id='dropdown-specialite',
                options=[{'label': col, 'value': col} for col in ['Voie_generale', 'Voie_technologique', 'Voie_professionnelle']],
                placeholder="Sélectionnez une spécialité"
            ),
        ], width=4)
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='map-lycees', style={'height': '500px'})
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                id='table-lycees',
                columns=[{'name': col, 'id': col} for col in ['Nom_etablissement', 'Nom_commune', 'Libelle_departement']],
                page_size=10,
                style_table={'overflowX': 'auto'}
            )
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='graph-bac')
        ], width=12)
    ])
])

# Callbacks pour mettre à jour les options de ville et les résultats
@app.callback(
    Output('dropdown-ville', 'options'),
    Input('dropdown-departement', 'value')
)
def update_ville_options(selected_departement):
    if selected_departement:
        villes = lycees_df[lycees_df['Libelle_departement'] == selected_departement]['Nom_commune'].dropna().unique()
        return [{'label': v, 'value': v} for v in sorted(villes)]
    return []

@app.callback(
    [Output('map-lycees', 'figure'),
     Output('table-lycees', 'data'),
     Output('graph-bac', 'figure')],
    [Input('dropdown-departement', 'value'),
     Input('dropdown-ville', 'value'),
     Input('dropdown-specialite', 'value')]
)
def update_dashboard(departement, ville, specialite):
    filtered_df = lycees_df.copy()
    if departement:
        filtered_df = filtered_df[filtered_df['Libelle_departement'] == departement]
    if ville:
        filtered_df = filtered_df[filtered_df['Nom_commune'] == ville]
    if specialite:
        filtered_df = filtered_df[filtered_df[specialite] == '1']
    
    # Vérifier s'il y a des données avant d'afficher
    if filtered_df.empty:
        return px.scatter_mapbox(), [], px.bar()
    
    # Carte interactive
    fig_map = px.scatter_mapbox(
        filtered_df,
        lat='latitude',
        lon='longitude',
        text='Nom_etablissement',
        zoom=9,
        mapbox_style='carto-positron'
    )
    
    # Tableau des lycées
    table_data = filtered_df[['Nom_etablissement', 'Nom_commune', 'Libelle_departement']].to_dict('records')
    
    # Graphique des résultats au Bac
    fig_bac = px.bar(
        filtered_df,
        x='Nom_etablissement',
        y='Taux de reussite - Toutes series',
        title="Taux de Réussite au Bac",
        labels={'Taux de reussite - Toutes series': 'Taux de Réussite (%)'},
        color='Taux de reussite - Toutes series'
    )
    
    return fig_map, table_data, fig_bac

if __name__ == '__main__':
    app.run_server(debug=True)
