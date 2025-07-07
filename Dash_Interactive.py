import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

app = dash.Dash(__name__)
app.title = 'SpaceX Launch Records Dashboard'

options = [{'label': 'All Sites', 'value': 'ALL'}]
launch_site_names = df['Launch Site'].unique().tolist()

for site in launch_site_names:
    options.append({'label':site, 'value':site})


app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),

    dcc.Dropdown(id='site-dropdown',
                     options=options,
                     value='ALL',
                     placeholder='All Sites',
                     searchable=True,
                     style={'width':'80%', 'margin':'auto'}),

    dcc.Graph(id='success-pie-chart'),
        
    html.Br(),
    html.Div('Payload Range (kg):', style={'textAlign':'center'}),

    dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={0:'0', 2500:'2500', 5000:'5000', 7500:'7500', 10000:'10000'},
                                value=[df['Payload Mass (kg)'].min(), df['Payload Mass (kg)'].max()]),

    dcc.Graph(id='success-payload-scatter-chart')
])

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        data = df
        title = 'Total Success Launches'
        
    else:
        data = df[df['Launch Site'] == entered_site]
        title = f'Success Launches at {entered_site}'
    
    success_rate = data['class'].mean()
    fig1 = px.pie(values=[1-success_rate, success_rate], names=['Failed', 'Success'], title=title)
        
    return fig1


@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')]
)

def get_scatter_chart(entered_sites, payload_range):
    low, high = payload_range
    filtered_df = df[(df['Payload Mass (kg)'] >= low) & (df['Payload Mass (kg)'] <= high)]

    if entered_sites != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_sites]
            
    fig2 = px.scatter(data_frame=filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version', title='Payload vs. Launch Outcome')
        
    return fig2  
        

if __name__ == '__main__':
    app.run(debug=True)