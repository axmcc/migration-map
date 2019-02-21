#!/usr/bin/env python3

# #### Modified from:
# https://plot.ly/python/lines-on-maps/
# 
# #### Improvements required:
# - add state/countie boundaries
# - click on Indiana county should highlight outlflow destinations
# - on click each line should provide info on number of outflows

# Import libraries
import plotly.plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import pandas as pd

#Load Data
df_locations = pd.read_excel('migration.xlsx', sheet_name='locations')
df_migration = pd.read_excel('migration.xlsx', sheet_name='county_outflow')

#Filter aggregate and non-migration reccords
df_migration = (
    df_migration[pd.notnull(df_migration['destination_xcoord'])]
    .query('non_migration == 0')
)

df_migration.reset_index(inplace=True, drop=True)

# Define counties list
counties = [ dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = df_locations['xcoord'],
        lat = df_locations['ycoord'],
        hoverinfo = 'text',
        text = df_locations['county_label'] + "<br>" +  df_locations['state_label'],
        mode = 'markers',
        marker = dict( 
            size=3, 
            color='rgb(255, 0, 0)',
            line = dict(
                width=5,
                color='rgba(68, 68, 68, 0)'
            )
        ))]

# Define migrationo paths
migration_paths = []
for i in range(len(df_migration)):
    migration_paths.append(
        dict(
            type = 'scattergeo',
            locationmode = 'USA-states',
            lon = [df_migration['origin_xcoord'][i], df_migration['destination_xcoord'][i]],

            lat = [df_migration['origin_ycoord'][i], df_migration['destination_ycoord'][i]],
            mode = 'lines',
            line = dict(
                width = 2,
                color = 'red',
            ),
            opacity = float(df_migration['sum'][i])/float(df_migration['sum'].max()),
        )
    )

# Layout setup
layout = dict(
        title = 'Outflow Migration from Indiana Counties',
        showlegend = False, 
        geo = dict(
            scope='north america',
            projection=dict( type='azimuthal equal area' ),
            showland = True,
            showlakes = True,
            showocean = True,
            landcolor = 'rgb(243, 243, 243)',
            countrycolor = 'rgb(204, 204, 204)',
            oceancolor = 'rgb(65, 105, 225)',
            lakecolor  = 'rgb(65, 105, 225)'
        ),
    )

# Output
fig = dict(data=migration_paths + counties, layout=layout )
plot(fig, filename='indiana-county-outflow.html' )
