from dash import Dash, html
import dash

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Covid-19 Economic Impact Dashboards"),
    html.Nav([
        html.A("Global Dashboard", href="/global-dashboard"),
        html.A("US Dashboard", href="/US-dashboard"),
        html.A("Europe Dashboard", href="/europe-dashboard"),
        html.A("Asia Dashboard", href="/asia-dashboard"),
        html.A("Djamel's Dashboard", href="/djamel-dashboard"),
    ], style={
        'display': 'flex',
        'gap': '30px',
        'justifyContent': 'center',
        'padding': '16px 0',
        'marginBottom': '24px',
        'centered': 'true',
    }),
    dash.page_container  # Renders current page content
])

if __name__ == "__main__":
    app.run(debug=True)


