import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

#app = Dash(__name__)


external_stylesheets = [

    {

        "href": "https://fonts.googleapis.com/css2?"

                "family=Lato:wght@400;700&display=swap",

        "rel": "stylesheet",

    },

]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = "ISB Analytics: Understand Your Venture!"

server=app.server


app.layout = html.Div([
    html.H4('Interactive scatter plot for Model Accuracy'),
    dcc.Graph(id="scatter-plot"),
    html.P("Filter by Test length:"),
    dcc.RangeSlider(
        id='range-slider',
        min=0, max=1, step=0.1,
        marks={0: '0', 1: '1'},
        value=[0.1, 1]
    ),
])


@app.callback(
    Output("scatter-plot", "figure"), 
    Input("range-slider", "value"))
def update_bar_chart(slider_range):
    #df = px.data.iris() # replace with your own data source
    df = pd.read_csv(
    "Results.csv", header=0
    )
    x=df.iloc[0,:]
    y=df.iloc[1,:]

    df1 = pd.DataFrame(x)
    df2 = pd.DataFrame(y)
    df = pd.concat([df1,df2],axis=1,ignore_index=True)#, left_index=True, right_index=True)
    df.drop(df.index[0], axis=0, inplace=True)
    df.rename(columns = {'0':'Test Length', '1':'Accuracy'}, inplace = True)
    df.columns = ['Test_Length', 'Accuracy']


    low, high = slider_range
    f='Test_Length'
    mask = (df[f] > low) & (df[f] < high)
    fig = px.scatter(
        df[mask], x=f, y="Accuracy")
    fig.update_traces(marker={'size': 15}) 
    return fig


app.run_server(debug=True)