import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
from scipy.stats import pearsonr

# Load real data
df = pd.read_csv("team_perf.csv")

# Initialize app
app = dash.Dash(__name__)
app.title = "NBA Clutch Analytics Dashboard"

# Helper function to make a correlation scatter plot
def make_correlation_plot(x_metric, y_metric, title, df):
    # Calculate correlation
    corr = df[x_metric].corr(df[y_metric])
    
    # Format hover text
    hover_text = df.apply(
        lambda row: f"Team: {row['team']}<br>{x_metric.replace('_', ' ').title()}: {row[x_metric]:.1f}%<br>{y_metric.replace('_', ' ').title()}: {row[y_metric]:.1f}%", 
        axis=1
    )

    fig = px.scatter(
        df,
        x=x_metric,
        y=y_metric,
        text='team',  # Optional: team name shown on plot
        hover_name='team',
        hover_data={x_metric: False, y_metric: False},  # Removed 'text'
        title=f"{title}<br><sup>Correlation: {corr:.2f}</sup>",
        trendline="ols"
    )
    
    fig.update_traces(hovertext=hover_text, hoverinfo='text')

    fig.update_layout(
        title_x=0.5,
        margin=dict(l=40, r=40, t=80, b=40),
        height=400
    )

    return fig



# App layout
app.layout = html.Div([
    html.H1("NBA Clutch Analytics (2024–2025)", style={'textAlign': 'center'}),

    html.H2("Team Win Percentages", style={'marginTop': '20px'}),
    html.Label("Select Metric to Plot:"),
    dcc.Dropdown(
        id='metric-dropdown',
        options=[
            {'label': 'Clutch Win %', 'value': 'clutch_win_pct'},
            {'label': 'Overall Win %', 'value': 'overall_win_pct'},
            {'label': 'Home Win %', 'value': 'home_win_pct'}
        ],
        value='clutch_win_pct'
    ),
    dcc.Graph(id='bar-chart'),

    html.H2("Correlation: Overall Win % vs. Clutch Win %"),
    dcc.Graph(
        figure=make_correlation_plot('overall_win_pct', 'clutch_win_pct', 
                                     "Overall Win % vs. Clutch Win %", df)
    ),

    html.H2("Correlation: Home Win % vs. Clutch Win %"),
    dcc.Graph(
        figure=make_correlation_plot('home_win_pct', 'clutch_win_pct', 
                                     "Home Win % vs. Clutch Win %", df)
    )
])

# Callback for the bar chart
@app.callback(
    dash.dependencies.Output('bar-chart', 'figure'),
    [dash.dependencies.Input('metric-dropdown', 'value')]
)
def update_bar_chart(selected_metric):
    fig = px.bar(df, x='team', y=selected_metric, color='team',
                 title=f"{selected_metric.replace('_', ' ').title()} by Team")
    return fig

# Run server
if __name__ == '__main__':
    app.run(debug=True)
