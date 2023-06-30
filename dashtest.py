import pandas as pd
from dash import Dash, dcc, html

file_path = '/home/aryakumar/Downloads/file.csv'
data = pd.read_csv(file_path)

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Avocado Analytics"),
        html.P(
            children=(
                "Analyze the benumber"
                " of avocados sol"
            ),
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["key"],
                        "y": data["x"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Aver"},
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["key"],
                        "y": data["y"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "sold"},
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
