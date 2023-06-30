from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
data = pd.read_csv('/home/aryakumar/Downloads/final.csv')
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H4('Interactive scatter plot with our Gaussian dataset with live updates'),
    dcc.Graph(id="scatter-plot"),
    html.P("Filter by sample range:"),
    dcc.RangeSlider(
        id='my-range-slider',
        min=-20, max=20, step=1,
        value=[5, 15]
    ),
])

@app.callback(
    Output("scatter-plot", "figure"), 
    Input('my-range-slider', "value"))
def update_bar_chart(slider_range):
    df = px.data.iris() # replace with your own data source
    low, high = slider_range
    # mask = (df['petal_width'] > low) & (df['petal_width'] < high)
    fig = px.scatter(data, 
        x='x', y='y',
        color="labels",
        hover_data=['x'])
    return fig

app.run_server(debug=True)