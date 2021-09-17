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
                                # TASK 1: Add a dropdown list to enable Launch Site selection                              
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)

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

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                #html.Div(dcc.Graph(id='success-pie-chart')),
                                #dcc.Loading(id='loading-1', type='default',children=html.Div('success-pie-chart')),                               
                                html.Br(),
                                html.Br(),

                                # Update graph figures for success-pie-chart.
                                html.Div([ ], id='plot1'),
                                html.Div([ ], id='plot2'),
                                html.Div([ ], id='plot3'),                               
                                html.Div([ ], id='plot4'),
                                html.Div([ ], id='plot5'),
                                html.Div([ ], id='plot6'),
                                html.Div([ ], id='plot7'),

                                # style={'display': 'flex'}),

                                html.Div([
                                        html.Div([
                                                html.H4("Payload range (Kg):",
                                                style = {'margin-right': '2em'}),
                                        ]),
                                # TASK 3: Add a slider to select payload range
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

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                #html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                #dcc.Loading(id='loading-2', type='default',children=html.Div('success-payload-scatter-chart')),
                                html.Br(),
                                html.Br(),

                                # Update graph figures for success-payload-scatter-chart.                               
                                html.Div([ ], id='plot8'),
                                html.Div([ ], id='plot9'),                                       
                                html.Div([ ], id='plot10'),
                                html.Div([ ], id='plot11'),
                                html.Div([ ], id='plot12')

                                #style={'display': 'flex'}),

                  ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback([Output(component_id = 'plot1', component_property = 'children'),
               Output(component_id = 'plot2', component_property = 'children'),
               Output(component_id = 'plot3', component_property = 'children'),
               Output(component_id = 'plot4', component_property = 'children'),
               Output(component_id = 'plot5', component_property = 'children'),
               Output(component_id = 'plot6', component_property = 'children'),
               Output(component_id = 'plot7', component_property = 'children')
                ],
               Input(component_id='site-dropdown', component_property='value'),
                [State('plot1','children'), State('plot2','children'),
                 State('plot3','children'), State('plot4','children'),
                 State('plot5','children'), State('plot6','children'),
                 State('plot7','children')]
              )

# define get_pie(site)
def get_graphs(site,c1,c2,c3,c4,c5,c6,c7):
        # pie section
        #check if site value passed to a function equalls to that in dataframe.
        pie_data = spacex_df[spacex_df['Launch Site']== site]
        #line_data = spacex_df.groupby(['Launch Site','class']).sum().reset_index()
        #tree_data = spacex_df.groupby(['Launch Site','class']).size().reset_index()

        if site == 'All':
                # pie figure
                pie_fig = px.pie(spacex_df, values='class', names='Launch Site',
                                  title= "Total Success Launches by: {}".format(site) + 
                                  " Sites using pie.")
                # bar figure
                bar_fig = px.bar(spacex_df, x = 'Launch Site', y = 'class', color='Launch Site', 
                                        title= "Total Success Launches by: {}".format(site) + " Sites using bar.")
                # treemap figure
                tree_fig = px.treemap(spacex_df, path = ['class','Launch Site'],values = 'class', color = 'Launch Site',
                                        color_continuous_scale = 'RdBu', title = "Total Success Launches by: {}".format(site) +
                                        " Sites using treemap.")
                # box figure
                box_fig = px.box(spacex_df, x='class', y='Launch Site',orientation='h',color='Launch Site', notched=True, 
                                        title="Total Success Launches by: {}".format(site) + " Sites using box.")
                # violin figure
                violin_fig = px.violin(spacex_df, x='Launch Site',y = 'class',color = 'Launch Site', box=True, points='all',
                                               title="Total Success Launches by: {}".format(site) + " Sites using violin." )
                # histogram figure
                hist_fig = px.histogram(spacex_df, x='class', y = 'Launch Site', color = 'Launch Site', 
                                                title="Total Success Launches by: {}".format(site) + " Sites using histogram." )

                den_heatmap_fig = px.density_heatmap(spacex_df, x='Launch Site',y='class', hover_name='Launch Site',
                                                        color_continuous_scale=['red','green','blue','yellow','black','blue','gray','green'],
                                                        height=600, title="Total Success Launches by: {}".format(site) + " Sites using density heatmap.")
                
                return [
                        dcc.Graph(figure=pie_fig), 
                        dcc.Graph(figure=bar_fig),
                        dcc.Graph(figure=tree_fig),
                        dcc.Graph(figure=box_fig),
                        dcc.Graph(figure=violin_fig),
                        dcc.Graph(figure=hist_fig),
                        dcc.Graph(figure=den_heatmap_fig)                             
                        ]

        else:
               
                group_data = pie_data.groupby(['Launch Site','class']).size().reset_index(name='class count')
                 # pie section
                pie_fig = px.pie(group_data, values='class count', names='class', 
                                        title= "Total Success Launches by site: {}".format(site) + ' using pie.')
                 # bar section
                bar_fig = px.bar(group_data, x='class count', y='Launch Site', color='class', 
                                        title= "Total Success Launches by site: {}".format(site) + ' using bar.')
                 # treemap section
                tree_fig = px.treemap(group_data, values = 'class count', color = 'class', path = ['class','Launch Site'],
                                        color_continuous_scale = 'RdBu', title = "Total Success Launches by: {}".format(site) + 
                                        ' using treemap.')
                 # box section
                box_fig = px.box(group_data, x='class count',y='Launch Site',orientation='h',color='Launch Site', notched=True, 
                                        title="Total Success Launches by: {}".format(site) + ' using box.')
                # violin figure
                violin_fig = px.violin(group_data, x='Launch Site', y = 'class',color = 'Launch Site', box=True, points='all',
                                               title="Total Success Launches by: {}".format(site) + 
                                               ' using violin.')
                # histogram figure
                hist_fig = px.histogram(group_data, x='class count', y = 'Launch Site', color = 'class', 
                                                title="Total Success Launches by: {}".format(site) +
                                                 ' using histogram.')
                # density_heatmap figure
                den_heatmap_fig = px.density_heatmap(group_data, x='class count',y='Launch Site', hover_name='Launch Site',
                                                        color_continuous_scale=['red','green','blue','yellow','black'],
                                                        height=600, title="Total Success Launches by: {}".format(site) + 
                                                        ' using density_heatmap.')

                return [dcc.Graph(figure=pie_fig), 
                        dcc.Graph(figure=bar_fig),
                        dcc.Graph(figure=tree_fig),
                        dcc.Graph(figure=box_fig),
                        dcc.Graph(figure=violin_fig),
                        dcc.Graph(figure=hist_fig),
                        dcc.Graph(figure=den_heatmap_fig)
                        ]


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
#def get_scatter(site,slider):
@app.callback([Output(component_id = 'plot8', component_property='children'),
                Output(component_id = 'plot9', component_property = 'children'),
                Output(component_id = 'plot10', component_property = 'children'),
                Output(component_id = 'plot11', component_property = 'children'),
                Output(component_id = 'plot12', component_property = 'children')],

              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')],

               [State('plot8','children'),State('plot9','children'),
               State('plot10','children'),State('plot11','children'),
               State('plot12','children')],
              )

# function for 
def other_graphs(site,slider_range,c8,c9,c10,c11,c12):
        low,high= slider_range 
        low = min(spacex_df['Payload Mass (kg)'])
        high = max(spacex_df['Payload Mass (kg)'])

        sliding = (spacex_df['Payload Mass (kg)'] >=low) & (spacex_df['Payload Mass (kg)'] <= high)
        scatter_df = spacex_df[sliding]

        if site == 'All':
                # scatter figure
                scat_fig = px.scatter(scatter_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',
                                        title='Correlation between Payload and Success for {}'.format(site) +
                                        ' Sites using scatter.')

                scat_modify_fig = px.scatter(scatter_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',
                                                size_max=50,marginal_y ='box',height = 500, marginal_x='box',
                                                trendline='ols', template='plotly_white', hover_name='Launch Site',
                                                title='Correlation between Payload and Success for {}'.format(site) +
                                                ' Sites using tuned scatter.')

                scatter_matric_fig = px.scatter_matrix(scatter_df, dimensions=['Payload Mass (kg)','class'],color='Booster Version Category',
                                                      title='Correlation between Payload and Success for {}'.format(site) +
                                                      ' Sites using scatter_matrix.')


                par_coord_fig = px.parallel_coordinates(scatter_df, dimensions=['Payload Mass (kg)', 'class' ],
                                                        color ='class', color_continuous_scale= ['red','green','blue'], height=600, 
                                                        title='Correlation between Payload and Success for {}'.format(site) +
                                                         ' Sites using parallel_coordinates.')

                par_cat_fig = px.parallel_categories(scatter_df, dimensions=['Payload Mass (kg)', 'class'],
                                                        color ='class', color_continuous_scale= ['red','green','blue'],
                                                        height=600, dimensions_max_cardinality=50,
                                                        title='Correlation between Payload and Success for {}'.format(site) +
                                                        ' Sites using parallel_categories.')

                return [dcc.Graph(figure=scat_fig),
                        dcc.Graph(figure=scat_modify_fig),
                        dcc.Graph(figure=scatter_matric_fig),
                        dcc.Graph(figure=par_coord_fig),
                        dcc.Graph(figure=par_cat_fig)
                                ]

        else:
                #check if site value passed to a function equalls to that in dataframe.
                scatter_data = scatter_df[scatter_df['Launch Site'] == site]
                
                scat_fig = px.scatter(scatter_data,x='Payload Mass (kg)',y='class',color='Booster Version Category',
                                        title='Correlation between Payload and Success for {}'.format(site) +
                                        ' using scatter.')

                scat_modify_fig = px.scatter(scatter_data, x='Payload Mass (kg)', y='class', color="Booster Version Category",
                                          size_max=50, marginal_y ='box', height = 500, marginal_x='box',
                                          trendline='ols', template='plotly_white', hover_name='Launch Site',
                                          title='Correlation between Payload and Success for site: {}'.format(site) +
                                          ' using tuned scatter.')

                scat_matric_fig = px.scatter_matrix(scatter_data, dimensions = ['Payload Mass (kg)','class'],
                                                    color='Booster Version Category', hover_name='Booster Version Category',
                                                    opacity= 0.5, title='Correlation between Payload and Success for {}'.format(site) +
                                                    'using scatter_matrix.')

                par_coord_fig = px.parallel_coordinates(scatter_data, dimensions=['Payload Mass (kg)', 'class'],
                                                        color ='class', color_continuous_scale= ['red','green','blue'],
                                                         height=600, title='Correlation between Payload and Success for {}'.format(site) + 
                                                         ' using parallel_coordinates.')

                par_cat_fig = px.parallel_categories(scatter_data, dimensions=['Payload Mass (kg)', 'class'],
                                                        color ='class', color_continuous_scale= ['red','green','blue'],
                                                        height=600, dimensions_max_cardinality=50,
                                                        title='Correlation between Payload and Success for {}'.format(site) + 
                                                        ' using parallel_coordinates.')
                
                return [dcc.Graph(figure=scat_fig),
                        dcc.Graph(figure=scat_modify_fig),
                         dcc.Graph(figure=scat_matric_fig),   
                         dcc.Graph(figure=par_coord_fig),
                         dcc.Graph(figure=par_cat_fig)
                                ]



# Run the app
if __name__ == '__main__':
        app.run_server(debug=True)
        
