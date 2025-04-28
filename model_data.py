"""
Data structures for the infrastructure project management model.
This module contains classes to organize and access the model parameters.
"""

class ModelData:
    """
    Class to store and access all model parameters
    """
    def __init__(self):
        # Number of elements
        self.NUM_project = 3  # j = 0, 1, 2 (3 projects)
        self.NUM_raw_mat = 4  # k = 0, 1, 2, 3 (4 raw materials)
        self.NUM_act = 23     # i = 0, 1, ..., 22 (23 activities)
        self.NUM_sup = 4      # s = 0, 1, 2, 3 (4 suppliers)
        self.NUM_order = 5    # o = 0, 1, 2, 3, 4 (5 orders)
        
        # Quantity of raw materials needed for each project
        # Quantity[k][j], k=0..3 (raw materials), j=0..2 (projects)
        self.Quantity = [
            [720, 560, 640],  # K=1
            [720, 560, 640],  # K=2
            [720, 560, 640],  # K=3
            [200, 320, 360]   # K=4
        ]

        # Supplier capacities
        # Capacity[k][s], k=0..3 (raw materials), s=0..3 (suppliers)
        self.Capacity = [
            [500, 300, 700, 650],  # K=1
            [1000, 1200, 0, 0],    # K=2
            [400, 350, 700, 620],  # K=3
            [220, 400, 500, 0]     # K=4
        ]

        # Target completion dates for each project
        self.Target = [418, 370, 423]  # Projects 1, 2, 3

        # Activity durations for each activity and project
        # Duration[i][j], i=0..22 (activities), j=0..2 (projects)
        self.Duration = [
            [18, 13, 15],  # Activity 1
            [7, 5, 6],     # Activity 2
            [20, 40, 45],  # Activity 3
            [5, 3, 4],     # Activity 4
            [8, 5, 7],     # Activity 5
            [36, 28, 32],  # Activity 6
            [18, 14, 16],  # Activity 7
            [18, 14, 16],  # Activity 8
            [36, 28, 32],  # Activity 9
            [18, 14, 16],  # Activity 10
            [18, 13, 15],  # Activity 11
            [7, 5, 6],     # Activity 12
            [20, 40, 45],  # Activity 13
            [5, 3, 4],     # Activity 14
            [8, 5, 7],     # Activity 15
            [36, 28, 32],  # Activity 16
            [18, 14, 16],  # Activity 17
            [18, 14, 16],  # Activity 18
            [36, 28, 32],  # Activity 19
            [18, 14, 16],  # Activity 20
            [7, 7, 7],     # Activity 21
            [3, 3, 3],     # Activity 22
            [40, 32, 35]   # Activity 23
        ]

        # Penalties for delays per project
        self.Penalty = [1500, 3000, 2500]  # Daily penalty for projects 1, 2, 3

        # Estimated delivery times (in days) and costs (in NIS) for raw materials
        # Delivery_Time[k][s][j]
        self.Delivery_Time = [
            # Supplier 1, 2, 3, 4
            [[9, 7, 11], [13, 10, 9], [8, 7, 8], [17, 15, 18]],  # K=1
            [[9, 7, 11], [13, 10, 9], [0, 0, 0], [0, 0, 0]],     # K=2
            [[9, 7, 11], [13, 10, 9], [8, 7, 8], [17, 15, 18]],  # K=3
            [[9, 7, 11], [13, 10, 9], [8, 7, 8], [0, 0, 0]]      # K=4
        ]
        
        # Cost[k][s][j]
        self.Cost = [
            # Supplier 1, 2, 3, 4
            [[2, 2, 2], [2.5, 2.5, 2.5], [3, 3, 3], [2.8, 2.8, 2.8]],  # K=1
            [[5, 5, 5], [4.5, 4.5, 4.5], [0, 0, 0], [0, 0, 0]],        # K=2
            [[3, 3, 3], [2.8, 2.8, 2.8], [3.5, 3.5, 3.5], [3.2, 3.2, 3.2]],  # K=3
            [[6, 6, 6], [5.5, 5.5, 5.5], [7, 7, 7], [0, 0, 0]]         # K=4
        ]

        # Usage Rate (UR): How much raw material is used per activity
        self.UR = [[2 for _ in range(self.NUM_raw_mat)] for _ in range(self.NUM_act)]

        # Predecessor relationships (a, b): activity a is a predecessor of activity b
        # Activities are numbered from 1 to 23 (convert to 0-22 for zero-indexed arrays)
        self.Pred = [
            (1, 2), (1, 3), (1, 4), (2, 4), (3, 4),
            (1, 5), (2, 5), (3, 5), (4, 5),
            (1, 6), (2, 6), (3, 6), (4, 6), (5, 6),
            (1, 7), (2, 7), (3, 7), (4, 7), (5, 7),
            (1, 8), (2, 8), (3, 8), (4, 8), (5, 8),
            (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8,9),
            (1, 10), (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10),
            (1, 11), (2, 11), (3, 11), (4, 11), (5, 11), (6, 11), (7, 11), (8, 11), (9, 11), (10, 11),
            (1, 12), (2, 12), (3, 12), (4, 12), (5, 12), (6, 12), (7, 12), (8, 12), (9, 12), (10, 12),
            (1, 13), (2, 13), (3, 13), (4, 13), (5, 13), (6, 13), (7, 13), (8, 13), (9, 13), (10, 13),
            (1, 14), (2, 14), (3, 14), (4, 14), (5, 14), (6, 14), (7, 14), (8, 14), (9, 14), (10, 14),
            (1, 15), (2, 15), (3, 15), (4, 15), (5, 15), (6, 15), (7, 15), (8, 15), (9, 15), (10, 15),
            (1, 16), (2, 16), (3, 16), (4, 16), (5, 16), (6, 16), (7, 16), (8, 16), (9, 16), (10, 16),
            (1, 17), (2, 17), (3, 17), (4, 17), (5, 17), (6, 17), (7, 17), (8, 17), (9, 17), (10, 17),
            (1, 18), (2, 18), (3, 18), (4, 18), (5, 18), (6, 18), (7, 18), (8, 18), (9, 18), (10, 18),
            (1, 19), (2, 19), (3, 19), (4, 19), (5, 19), (6, 19), (7, 19), (8, 19), (9, 19), (10, 19),
            (1, 20), (2, 20), (3, 20), (4, 20), (5, 20), (6, 20), (7, 20), (8, 20), (9, 20), (10, 20),
            (1, 21), (2, 21), (3, 21), (4, 21), (5, 21), (6, 21), (7, 21), (8, 21), (9, 21), (10, 21),
            (11, 21), (12, 21), (13, 21), (14, 21), (15, 21), (16, 21), (17, 21), (18, 21), (19, 21), (20, 21),
            (1, 22), (2, 22), (3, 22), (4, 22), (5, 22), (6, 22), (7, 22), (8, 22), (9, 22), (10, 22),
            (11, 22), (12, 22), (13, 22), (14, 22), (15, 22), (16, 22), (17, 22), (18, 22), (19, 22), (20, 22),
            (21, 23), (22, 23)
        ]
        # Convert to 0-based indexing
        self.Pred = [(a-1, b-1) for (a, b) in self.Pred]
        
    def get_all_data(self):
        """Return a dictionary with all model data"""
        return {
            'NUM_project': self.NUM_project,
            'NUM_raw_mat': self.NUM_raw_mat,
            'NUM_act': self.NUM_act,
            'NUM_sup': self.NUM_sup,
            'NUM_order': self.NUM_order,
            'Quantity': self.Quantity,
            'Capacity': self.Capacity,
            'Target': self.Target,
            'Duration': self.Duration,
            'Penalty': self.Penalty,
            'Delivery_Time': self.Delivery_Time,
            'Cost': self.Cost,
            'UR': self.UR,
            'Pred': self.Pred
        }

    def get_project_names(self):
        """Return a list of project names"""
        return [f'Project {j+1}' for j in range(self.NUM_project)]
    
    def get_raw_material_names(self):
        """Return a list of raw material names"""
        return [f'Material {k+1}' for k in range(self.NUM_raw_mat)]
    
    def get_supplier_names(self):
        """Return a list of supplier names"""
        return [f'Supplier {s+1}' for s in range(self.NUM_sup)]
    
    def get_activity_names(self):
        """Return a list of activity names"""
        return [f'Activity {i+1}' for i in range(self.NUM_act)]
