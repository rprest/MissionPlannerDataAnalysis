#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

input_tlog = "C:/Users/ryan/OneDrive/DroneProjects/MissionPlannerDataAnalysis/Data/MissionPlanTestData.xlsx"

df = pd.read_excel(input_tlog, sheet_name=0, header=None)

inputRows = len(df)

gpsRows = df[df[9] == 'mavlink_global_position_int_t'].copy()

gpsRowCt = len(gpsRows)

print(inputRows)
print(gpsRowCt)

# gpsRows.to_excel('gps_data.xlsx', index=False)

gps_data = pd.DataFrame({

    'time': gpsRows[11].values,
    'latitude': gpsRows[13].values,
    'longitude': gpsRows[15].values,
    'altitude': gpsRows[17].values,
    'relative_alt': gpsRows[19].values,

})

gps_data['latitude'] = pd.to_numeric(gps_data['latitude']) / 1e7
gps_data['longitude'] = pd.to_numeric(gps_data['longitude']) / 1e7

gps_data['altitude'] = pd.to_numeric(gps_data['altitude']) / 1000
gps_data['relative_alt'] = pd.to_numeric(gps_data['relative_alt']) / 1000
gps_data['time'] = pd.to_numeric(gps_data['time']) / 1000

finalGPS = gps_data[7:].copy()

centLong = finalGPS.mean().longitude
centLat = finalGPS.mean().latitude
centAlt = finalGPS.mean().altitude

finalGPS['relLat'] = (finalGPS['latitude'] - centLat) * 111320 * np.cos(np.radians(centLat))
finalGPS['relLong'] = (finalGPS['longitude'] - centLong) * 110540
finalGPS['relAlt'] = finalGPS['altitude'] - centAlt
finalGPS['relTime'] = (finalGPS['time'] - finalGPS.iloc[0].time)

finalGPS = finalGPS[715:802].copy()

# finalGPS.to_excel('C:/Users/ryan/OneDrive/DroneProjects/MissionPlannerDataAnalysis/Data/finalGPS.xlsx', index=False)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# ax.scatter(finalGPS['longitude'], 
#            finalGPS['latitude'], 
#            finalGPS['altitude'], 
#            c='b', 
#            marker='.')

# plt.show()

fig = px.scatter_3d(finalGPS, x='relLong', y='relLat', z='relAlt', 
                    color='relTime',
                    color_continuous_scale='deep'
                    )

fig.update_traces(
    marker=dict(
        size=8
        )
    )

fig.update_layout(
    scene=dict(
        xaxis=dict(
            showgrid=True,
            tickformat='.1f'
            ),
        yaxis=dict(
            showgrid=True,
            tickformat='.1f'
            ),
        zaxis=dict(
            showgrid=True,
            tickformat='.1f'
            ),
        aspectmode='data'
    )
)
fig.show()

# fig = make_subplots(
#     rows = 1, cols=2,
#     specs=[[{'type':'scatter'}, {'type':'scatter3d'}]],
#     horizontal_spacing=0.1
# )

# fig.add_trace(
#     go.Scatter(
#         x=finalGPS['relLong'],
#         y=finalGPS['relLat'],
#         mode='markers',
#         marker=dict(
#             size=12,
#             color=finalGPS['relTime'],
#             colorscale='deep',
#             # colorbar=dict(title='Time (s)'),
#             showscale=True
#         ),
#         name='2D'
#     ),
#     row=1, col=1
# )

# fig.add_trace(
#     go.Scatter3d(
#         x=finalGPS['relLong'],
#         y=finalGPS['relLat'],
#         z=finalGPS['relAlt'],
#         mode='markers',
#         marker=dict(
#             size=8,
#             color=finalGPS['relTime'],
#             colorscale='deep',
#             # colorbar=dict(title='Time (s)'),
#             showscale=True
#         ),
#         name='3D'
#     ),
#     row=1, col=2
# )

# fig.update_scenes(
#     aspectmode='data',
#     row=1, col=2
# )


#fig.show()

fig.write_html("C:/Users/ryan/OneDrive/DroneProjects/MissionPlannerDataAnalysis/Data/droneGPSdata2.html")