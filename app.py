# Import required libraries
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.graph_objects as go
import pandas as pd
import os

# Ensure the data directory exists
os.makedirs("data", exist_ok=True)

# Check if the data file exists, if not, create it
file_path = "data/migration_data.csv"
if not os.path.exists(file_path):
    data = {
        "Source": ["USA", "India", "Germany", "China", "Canada", "UK", "France", "Brazil", "Australia", "Japan"],
        "Destination": ["Canada", "USA", "USA", "India", "UK", "Germany", "Brazil", "USA", "USA", "China"],
        "Year": [2010, 2010, 2011, 2011, 2012, 2012, 2013, 2013, 2014, 2014],
        "Migrants": [150000, 200000, 180000, 300000, 120000, 220000, 140000, 190000, 170000, 160000],
    }
    pd.DataFrame(data).to_csv(file_path, index=False)

# Load migration data from a CSV file
df = pd.read_csv(file_path)

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
fig_sankey.update_layout(title_text="Migration Flow Between Countries", font_size=10)

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
