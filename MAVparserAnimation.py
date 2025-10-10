#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from manim import *

class DronePathAnimation(Scene): 
    def construct(self):

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

        # Slice to final data set
        finalGPS = finalGPS[715:802].copy()

        x_data = finalGPS['relLong'].values
        y_data = finalGPS['relLat'].values

        scale_factor = 5 / max(abs(x_data).max(), abs(y_data).max())
        xScaled = x_data * scale_factor
        yScaled = y_data * scale_factor

        axes = Axes(
            x_range=[xScaled.min() - 1, xScaled.max() + 1, 1],
            y_range=[yScaled.min() - 0.5, yScaled.max() + 0.5, 1],
            x_length=10,
            y_length=10,
            axis_config={"include_tip": False, "color": BLACK},
        )

        self.add(axes)

        points = [axes.c2p(xScaled[i], yScaled[i]) for i in range(len(xScaled))]

        drone = Dot(points[0], color=BLUE, radius=0.15)

        path = VMobject(points[0], color=RED)
        # path = VMobject(color=RED)
        # path.set_points_as_corners([points[0], points[0]])

        self.add(drone, path)

        def update_drone(mob, alpha):

            idx = int(alpha * (len(points) - 1))

            mob.move_to(points[idx])

        devPts = []

        def update_path(mob, alpha):

            idx = int(alpha * (len(points) - 1))

            mob.set_points_smoothly(points[:idx + 1])

            while len(devPts) <= idx:
                new_pt = len(devPts)
                new_dot = Dot(points[new_pt], color=RED, radius=0.15)
                new_dot.set_opacity(0)
                devPts.append(new_dot)
                self.add(new_dot)
                self.play(FadeIn(new_dot), run_time=0.1)

        self.play(
            UpdateFromAlphaFunc(path, update_path),
            UpdateFromAlphaFunc(drone, update_drone),
            run_time=10,
            rate_func=smooth
        )

        self.wait(1)


        # finalGPS.to_excel('C:/Users/ryan/OneDrive/DroneProjects/MissionPlannerDataAnalysis/Data/finalGPS.xlsx', index=False)

        # fig = plt.figure()
        # ax = fig.add_subplot(111, projection='3d')

        # ax.scatter(finalGPS['longitude'], 
        #            finalGPS['latitude'], 
        #            finalGPS['altitude'], 
        #            c='b', 
        #            marker='.')

        # plt.show()

        # fig = px.scatter_3d(finalGPS, x='relLong', y='relLat', z='relAlt', 
        #                     color='relTime',
        #                     color_continuous_scale='deep'
        #                     )

        # fig.update_traces(
        #     marker=dict(
        #         size=10
        #         )
        #     )

        # fig.update_layout(
        #     scene=dict(
        #         xaxis=dict(
        #             showgrid=True,
        #             tickformat='.1f'
        #             ),
        #         yaxis=dict(
        #             showgrid=True,
        #             tickformat='.1f'
        #             ),
        #         zaxis=dict(
        #             showgrid=True,
        #             tickformat='.1f'
        #             ),
        #         aspectmode='data'
        #     )
        # )
        # fig.show()

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

        # fig.write_html("C:/Users/ryan/OneDrive/DroneProjects/MissionPlannerDataAnalysis/Data/droneGPSdata2.html")