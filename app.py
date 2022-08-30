import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

data = pd.read_csv("kbopitchingdata.csv")
data = data.query("team == 'Doosan Bears'")
# print(list(data.columns))

treed = {'group1': ['item1', 'item2'], 'group2': ['thing1', 'thing2']}


def generate_tree(treedict):
    return html.Div(
        [
            # detail tags allows for hidden component
            html.Details(
                [
                    html.Summary(k),
                    html.Div(
                        [
                            html.Details(
                                html.Summary(item)
                            ) for item in treedict[k]
                        ], style={'text-indent': '2em'}
                    )
                ]
            ) for k in treedict
        ]
    )


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"  # external style sheet
                "family=Lato:wght@400;700&display=swap",  # font family
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)  # create instance of Dash class
server = app.server
app.title = "Doosan Bears Stats: 곰들아!"  # set application title

# define layout of application
app.layout = html.Div(  # define html parent component
    # two children: heading (html.H1) and paragraph (html.P)
    children=[
        html.Div(
            # classname arguments define the look of each component (from style.css)
            children=[
                html.P(children="⚾", className="header-emoji"),
                html.H1(
                    children="Doosan Bears Statistics", className="header-title"
                ),
                html.P(
                    children="Analyze statistics from the Doosan Bears Korean baseball team",
                    className="header-description",
                ),
            ],
            className="header",
        ),

        generate_tree(treed),

        html.Div(
            children=dcc.Graph(
                id="win-loss",
                config={"displayModeBar": False},
                figure={
                    "data": [
                        {
                            "x": data["year"],
                            "y": data["win_loss_percentage"],
                            "type": "scatter",
                        },
                    ],
                    "layout": {
                        "title": {
                            "text": "Win-Loss Ratio over the years",
                            "x": 0.05,
                            "xanchor": "left",
                        },
                        "xaxis": {"fixedrange": True},
                        "yaxis": {
                            "fixedrange": True,
                        },
                        "colorway": ["blue"],
                    },
                },
            ),
            className="card",
        ),
        html.Div(
            dcc.Graph(
                figure={
                    "data": [
                        {
                            "x": data["year"],
                            "y": data["home_runs"],
                            "type": "lines",
                        },
                    ],
                    "layout": {
                            "title": {
                                "text": "Home Runners",
                                "x": 0.05,
                                "xanchor": "left",
                            },
                            "xaxis": {"fixedrange": True},
                            "yaxis": {
                                "fixedrange": True,
                            },
                            "colorway": ["red"],
                    },
                },
            ),
            className="card",
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
