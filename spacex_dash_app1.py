# Import required libraries
from json import loads
from dash_core_components.Graph import Graph
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output,State
import plotly.express as px
#from dash import no_update


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
site_list = ['All','CCAFS LC-40', 'VAFB SLC-4E', 'KSC LC-39A', 'CCAFS SLC-40']

# Create a dash application
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Create an app layout
app.layout = html.Div(children=[
                                html.H3('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 
                                                'color': '#503D36',
                                                'backgroundColor': "white",
                                                'font-size': 23}),
                                # Add a dropdown list to enable Launch Site selection                              
                                # The default select value is for ALL sites

                                # outer division
                                html.Div([
                                    # inner division
                                    html.Div([
                                        # Create an division for adding dropdown helper text for report type
                                        html.Div([
                                                html.H3('Launching Site:', 
                                                style = {'margin-right': '2em'}),
                                                ]),
                                        # create dropdown list or options for launch sites
                                        dcc.Dropdown(id ='site-dropdown',
                                                options = [{'label': i, 'value': i } for i in (site_list)
                                                        #{'label': 'All', 'value': 'All'},
                                                        #{'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                        #{'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                        #{'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                        #{'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                        
                                                        ],
                                                value = 'All',
                                                multi=False,
                                                placeholder = 'Select a Launching site', 
                                                searchable = True,
                                                style = {'width':'80%','padding':'3px', 'font-size':'20px',
                                                                'text-align-last':'center'}
                                                     ),

                                                ],
                                                style={'display':'flex'}
                                            ),
                                ]),
                                html.Br(),
                                html.Br(),

                                # Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),                               
                                html.Br(),
                                html.Br(),

                                html.Div([
                                        html.Div([
                                                html.H4("Payload range (Kg):",
                                                style = {'margin-right': '2em'}),
                                        ]),
                                # Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min= 0, max= 10000, step= 1000,
                                                value=[min_payload, max_payload],
                                                marks={0: {'label': '0', 'style': {'color': '#f50'}},
                                                        2500: {'label': '2500'},
                                                        5000: {'label': '5000'},
                                                        7500:{'label': '7500'},
                                                        10000: {'label': '10000', 'style': {'color': '#f50'}}
                                                        }
                                                ),
                                                ]),

                                # Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                html.Br(),
                                html.Br(),

                  ])

# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id = 'success-pie-chart', component_property = 'figure'),
               Input(component_id='site-dropdown', component_property='value'),
              )

# function for pie plot
def get_graphs(site):

        #check if site value passed to a function equalls to that in dataframe.
        pie_data = spacex_df[spacex_df['Launch Site']== site]

        if site == 'All':
                pie_fig = px.pie(spacex_df, values='class', names='Launch Site',
                                 title= "Total Success Launches by: {}".format(site) + " Sites.")
                
                return pie_fig  

        else:
               
                group_data = pie_data.groupby(['Launch Site','class']).size().reset_index(name='class count')                
                pie_fig = px.pie(group_data, values='class count', names='class', 
                                    title= "Total Success Launches by site: {}".format(site))        

                return pie_fig


# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# def get_scatter(site,slider):
@app.callback(Output(component_id = 'success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')],             
              )

# function for scatter plot.
def get_scatter(site,slider_range):
        low,high= slider_range 
        low = min(spacex_df['Payload Mass (kg)'])
        high = max(spacex_df['Payload Mass (kg)'])

        sliding = (spacex_df['Payload Mass (kg)'] >=low) & (spacex_df['Payload Mass (kg)'] <= high)
        scatter_df = spacex_df[sliding]

        if site == 'All':
                # scatter figure
                scatter_fig = px.scatter(scatter_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',
                                        title='Correlation between Payload and Success for {}'.format(site) +' Sites.')


                return scatter_fig
                        

        else:
                #check if site value passed to a function equalls to that in dataframe.
                scatter_data = scatter_df[scatter_df['Launch Site'] == site]
                
                scatter_fig = px.scatter(scatter_data,x='Payload Mass (kg)',y='class',color='Booster Version Category',
                                           title='Correlation between Payload and Success for {}'.format(site))

                return scatter_fig



# Run the app
if __name__ == '__main__':
        app.run_server(debug=True)
