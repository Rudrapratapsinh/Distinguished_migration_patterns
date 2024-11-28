# Import required libraries
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.graph_objects as go
import pandas as pd

# Load sample data for migration patterns
data = {
    "Source": ["Asia", "Asia", "Africa", "Europe", "South America"],
    "Destination": ["North America", "Europe", "Europe", "North America", "Europe"],
    "Migrants": [10500000, 5000000, 6200000, 7800000, 4500000],
    "Year": [2015, 2016, 2017, 2018, 2019]
}
df = pd.DataFrame(data)

# Initialize the Dash app
app = Dash(__name__)

# Create visualizations
# Sankey Diagram for migration flow
labels = list(set(df['Source'].tolist() + df['Destination'].tolist()))
source_indices = df['Source'].apply(lambda x: labels.index(x))
target_indices = df['Destination'].apply(lambda x: labels.index(x))

fig_sankey = go.Figure(go.Sankey(
    node=dict(
        pad=15, thickness=20, line=dict(color="black", width=0.5),
        label=labels
    ),
    link=dict(
        source=source_indices,
        target=target_indices,
        value=df['Migrants']
    )
))
fig_sankey.update_layout(title_text="Migration Flow Between Regions", font_size=10)

# Time-series trend
fig_line = go.Figure()
for source in df['Source'].unique():
    source_data = df[df['Source'] == source]
    fig_line.add_trace(go.Scatter(
        x=source_data['Year'],
        y=source_data['Migrants'],
        mode='lines+markers',
        name=source
    ))
fig_line.update_layout(
    title="Migration Trends Over Time",
    xaxis_title="Year",
    yaxis_title="Number of Migrants",
    template="plotly_white"
)

# Layout for the app
app.layout = html.Div([
    html.Header([
        html.H1("Migration Patterns Dashboard", style={"textAlign": "center", "padding": "10px", "backgroundColor": "#f4f4f9", "color": "#4a4e69"}),
    ], style={"marginBottom": "20px"}),

    # Section for Sankey Diagram
    html.Div([
        html.H3("Migration Flow Visualization", style={"textAlign": "center"}),
        dcc.Graph(id="sankey_diagram", figure=fig_sankey, config={"displayModeBar": False}),
    ], style={"marginBottom": "30px", "padding": "20px", "backgroundColor": "#f7f7f7", "borderRadius": "8px"}),

    # Section for Line Chart
    html.Div([
        html.H3("Migration Trends Over Time", style={"textAlign": "center"}),
        dcc.Graph(id="line_chart", figure=fig_line, config={"displayModeBar": False}),
    ], style={"marginBottom": "30px", "padding": "20px", "backgroundColor": "#f7f7f7", "borderRadius": "8px"}),

    # Data Table Section
    html.Div([
        html.H3("Raw Data Table", style={"textAlign": "center"}),
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "center", "padding": "10px", "border": "1px solid #ccc"},
            style_header={"backgroundColor": "#4a4e69", "color": "white", "fontWeight": "bold"},
            style_data={"backgroundColor": "#f4f4f9"},
        ),
    ], style={"padding": "20px", "backgroundColor": "#f7f7f7", "borderRadius": "8px"}),
], style={"fontFamily": "Arial, sans-serif", "margin": "0 auto", "maxWidth": "1200px", "padding": "20px"})

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

