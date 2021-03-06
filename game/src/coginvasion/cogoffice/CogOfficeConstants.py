"""
COG INVASION ONLINE
Copyright (c) CIO Team. All rights reserved.

@file CogOfficeConstants.py
@author Brian Lach
@date December 17, 2015

"""

from panda3d.core import Point3

from src.coginvasion.cog import Dept

RANDOM_FLOOR = "ran"
RECEPTION_FLOOR = "cog_first_floor"
SEWER_FLOOR = "sewer_tunnel"
CONFERENCE_FLOOR = "conf"
LOUNGE_FLOOR = "lou"
EXECUTIVE_FLOOR = "cog_interior_concept"
CUBICLE_FLOOR = "cog_floor2"
BREAK_FLOOR = "cog_breakfoor"
LONG_TEST = "testlongfloor"
SELL_FLOOR_1 = "sellbot_floor_1"
SELL_FLOOR_2 = "sellbot_floor_2"
SELL_FLOOR_3 = "sellbot_floor_3"
LAWBOT_TOP_FLOOR = "lawbot_windows_room"
LAW_FLOOR_1 = "lawbot_floor_1"

middleFloors = [LAW_FLOOR_1, SELL_FLOOR_3, LONG_TEST, SELL_FLOOR_1, SELL_FLOOR_2]

#numFloors2roomsVisited = {
#    1: [EXECUTIVE_FLOOR],
#    2: [RECEPTION_FLOOR, EXECUTIVE_FLOOR],
#    3: [RECEPTION_FLOOR, RANDOM_FLOOR, EXECUTIVE_FLOOR],
#    4: [RECEPTION_FLOOR, RANDOM_FLOOR, RANDOM_FLOOR, EXECUTIVE_FLOOR],
#    5: [RECEPTION_FLOOR, RANDOM_FLOOR, RANDOM_FLOOR, RANDOM_FLOOR, EXECUTIVE_FLOOR]
#}

numFloors2roomsVisited = {
    1: [LAWBOT_TOP_FLOOR],
    2: [RANDOM_FLOOR, LAWBOT_TOP_FLOOR],
    3: [RANDOM_FLOOR, RANDOM_FLOOR, LAWBOT_TOP_FLOOR],
    4: [RANDOM_FLOOR, RANDOM_FLOOR, RANDOM_FLOOR, LAWBOT_TOP_FLOOR],
    5: [RANDOM_FLOOR, RANDOM_FLOOR, RANDOM_FLOOR, RANDOM_FLOOR, LAWBOT_TOP_FLOOR]
}

# Faceoff: Position of Toons during faceoff
# Guard: Position of a standing Cog before activation
# Chairs: Position of a Cog in a chair
# Hangout: Position of a Cog when the toons first arrive in the elevator. (they're hanging out)

# For chairs and guards, the first item in each list is the floor section they are associated with.

# For chairs, the second item is the in-chair position of the cog, and the last item is the fly-to position.

# For guards, the second item is the guard position (where they stand and face before activation).

# For faceoff, each list is a [x, y, z, h, p, r].

POINTS = {RECEPTION_FLOOR: {'chairs': [[0, (0.91, 16.92, 0, 149.53, 0, 0), (-5.03, 8.69, 0, 331.11, 0, 0)]],
                   'guard': [[0, (-24.8844, 14.6984, 0.025, 270, 0, 0)],
                             [0, (-24.7556, 9.97378, 0.025, 270, 0, 0)],
                             [0, (-24.7342, 4.31459, 0.025, 270, 0, 0)],
                             [0, (-24.717, -0.469944, 0.025, 270, 0, 0)]],
                   'faceoff': [[-0.00392879, -2.6104, 0.025, 72.7151, 0, 0],
                               [-0.0059577, 1.44267, 0.025, 77.4296, 0, 0],
                               [0.0266161, 5.98924, 0.025, 86.452, 0, 0],
                               [0.252626, 10.0329, 0.025, 92.4258, 0, 0]],
                    'hangout': [[-36, 23, 0, 172, 0, 0],
                                [-35.6, 9.3, 0, 4, 0, 0],
                                [-31, -0.4, 0, -75, 0, 0],
                                [-15, 22, 0, -128, 0, 0],
                                [-36, -5, 0, -82, 0, 0]],
                    'barrels': [[(-18.3062, 68.6546, 6.18613), (36.5808, 0, 0)],
                                 [(-18.4405, 32.2494, 6.1865), (-217.912, 0, 0)],
                                 [(-38.144, 68.6539, 0.025), (-317.147, 0, 0)]]},
         EXECUTIVE_FLOOR: {'chairs': [
                        # Small room chairs
                        [0, (-65.01, -12.46, 0, 0, 0, 0), (-59.73, 1.16, 0, 0, 0, 0)],

                        # Large room chairs
                        [1, (12.08, 5.43, 0, 270, 0, 0), (0.16, 5.50, 0, 0, 0, 0)],
                        [1, (12.08, -3.03, 0, 270, 0, 0), (0.16, -2.37, 0, 0, 0, 0)],
                        [1, (18.15, 12.0, 0, 180, 0, 0), (7.02, -14.69, 0, 0, 0, 0)],
                        [1, (18.15, -9.25, 0, 0, 0, 0), (7.02, 15.03, 0, 0, 0, 0)],

                        [2, (-5.66, 43.43, 0, 159.35, 0, 0), (-6.69, 26.24, 0, 0, 0, 0)],
                        [2, (6.38, 56.02, 0, 331.45, 0, 0), (9.25, 71.16, 0, 0, 0, 0)]
                    ],
                    'guard': [
                        # Small room guards
                        [0, (-45, 14, 0, 91.5449, 0, 0)],
                        [0, (-45, 9, 0, 88.9605, 0, 0)],
                        [0, (-45, 3, 0, 86.619, 0, 0)],
                        [0, (-45, -2, 0, 78.1931, 0, 0)],

                        # Large room guards
                        [1, (-13.329, 30.022, 0, 180.862, 0, 0)],
                        [1, (-8.81858, 30.1296, 0, 179.246, 0, 0)],
                        [1, (-3.17527, 30.2092, 0, 176.022, 0, 0)],
                        [1, (0.911327, 30.252, 0, 177.616, 0, 0)],

                        [2, (-13.329, 70.022, 0, 0, 0, 0)],
                        [2, (-8.81858, 70.1296, 0, 0, 0, 0)],
                        [2, (-3.17527, 70.2092, 0, 0, 0, 0)],
                        [2, (0.911327, 70.252, 0, 0, 0, 0)],
                    ],
                    'hangout': [[-27, -3.25, 0, -295, 0, 0],
                                [-29.048, -10.65, 0.0, -42.23, 0.0, 0.0],
                                [-37.7, -14.6, 0.0, 10, 0, 0],
                                [-28.17, 8.11, 0.0, -186, 0, 0],
                                [-45, -9.9, 0, -252.9, 0, 0],
                                [-35, -16, 0, -380.6, 0, 0]],
                    'faceoff': [[-65.9154, 15.2706, 0, -102.464, 0, 0],
                                 [-65.9885, 11.5694, 0, -104.592, 0, 0],
                                 [-65.9267, 7.78086, 0, -97.9578, 0, 0],
                                 [-65.9494, 3.9793, 0, -92.8673, 0, 0]],
                    'barrels': []},
         CONFERENCE_FLOOR: {'chairs': [[0, (17.16, 8.54, 0, 90, 0, 0), (6.42, 8.54, 0, 90, 0, 0)],
                                      [0, (-13.49, 16.70, 0, 180, 0, 0), (-0.95, 19.57, 0, 180, 0, 0)],
                                      [0, (-18.82, 9.99, 0, 270, 0, 0), (-5.61, 29.19, 0, 270, 0, 0)],
                                      [0, (-18.82, 1.08, 0, 270, 0, 0), (1.63, 29.19, 0, 270, 0, 0)]],
                     'guard': [[0, (8.96618, 32, 0.025, 0, 0, 0)],
                               [0, (4.47451, 32, 0.025, 0, 0, 0)],
                               [0, (-0.543322, 32, 0.025, 0, 0, 0)],
                               [0, (-6.3705, 32, 0.025, 0, 0, 0)]],
                     'faceoff': [[5.91218, 51.6934, 0.025, 180, 0, 0],
                                 [1.88198, 51.6582, 0.025, 180, 0, 0],
                                 [-2.13479, 51.8396, 0.025, 180, 0, 0],
                                 [-6.00451, 51.9631, 0.025, 180, 0, 0]],
                     'hangout': [[9.7, 17.17, 0, -46, 0, 0],
                                 [-0.9, 14.5, 0, 39, 0, 0],
                                 [15.6, 25.0, 0, 56, 0, 0],
                                 [-10, 26, 0, 9.5, 0, 0],
                                 [3.7, 8.3, 0, -54, 0, 0],
                                 [2.1, 22.4, 0, 26, 0, 0]],
                     'barrels': [[(43.33, -12.04, 0), (142.52 - 180, 0, 0)],
                                 [(43.33, -17.79, 0), (90 - 180, 0, 0)],
                                 [(43.33, -38.51, 0), (90 - 180, 0, 0)],
                                 [(30.80, -41.05, 0), (323.75 - 180, 0, 0)]]},

        LOUNGE_FLOOR: {'chairs': [[0, (31.46, 64.83, 0, 351.87, 0, 0), (29.74, 50.05, 0, 0, 0, 0)],
                                  [0, (26.22, 66.4, 0, 327.09, 0, 0), (18.6, 53.53, 0, 0, 0, 0)],
                                  [0, (22.22, 69.97, 0, 302.15, 0, 0), (12.18, 62.86, 0, 282.38, 0, 0)],
                                  [0, (20.45, 75.12, 0, 282.38, 0, 0), (8, 73.38, 0, 282.38, 0, 0)],
                                  [0, (-26.46, 18.47, 0, 90, 0, 0), (-13, 18.47, 0, 0, 0, 0)],
                                  [0, (-26.46, 26.19, 0, 90, 0, 0), (-13, 26.19, 0, 0, 0, 0)],
                                  [0, (-26.46, 34.05, 0, 90, 0, 0), (-26.46, 34.05, 0, 0, 0, 0)]],
                    'guard': [[0, (-2.5, 45, 0, 180, 0, 0)],
                              [0, (-7.5, 45, 0, 180, 0, 0)],
                              [0, (2.5, 45, 0, 180, 0, 0)],
                              [0, (7.5, 45, 0, 180, 0, 0)]],
                    'faceoff': [[7.5, 20, 0, 0, 0, 0],
                                [2.5, 20, 0, 0, 0, 0],
                                [-2.5, 20, 0, 0, 0, 0],
                                [-7.5, 20, 0, 0, 0, 0]],
                    'hangout': [[12.6, 62.6, 0, -143, 0, 0],
                                [-10.7, 61.56, 0, 166, 0, 0],
                                [0, 72.6, 0, 13, 0, 0],
                                [11, 70, 0, 301, 0, 0],
                                [-1, 62.9, 0, 221, 0, 0],
                                [-9.5, 69.6, 0, 571, 0, 0]],
                    'barrels': [[(48, 58, 0), (0, 0, 0)],
                                [(54, 58, 0), (0, 0, 0)],
                                [(54, 34, 0), (180, 0, 0)],
                                [(48, 34, 0), (180, 0, 0)]]}
}
