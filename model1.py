from mip import Model, xsum, minimize, BINARY, INTEGER, OptimizationStatus
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import plot_gantt_chart, plot_resource_usage, plot_project_delays, plot_supplier_allocation
from model_data import ModelData

def create_and_solve_model():
    """
    Creates and solves the infrastructure project management optimization model
    based on the specifications in Model 1.docx
    """
    # Load model data
    data = ModelData()
    
    # Big-M value
    M = 1000000

    # Creating the MIP model
    m = Model("infrastructure_project_management", solver_name='cbc')

    # Decision Variables

    # Start Times (ST) and Finish Times (FT) for each activity and project
    ST = [[
        m.add_var(var_type=INTEGER, name=f'ST_{i+1}_{j+1}', lb=0)
        for j in range(data.NUM_project)
    ] for i in range(data.NUM_act)]

    FT = [[
        m.add_var(var_type=INTEGER, name=f'FT_{i+1}_{j+1}', lb=0)
        for j in range(data.NUM_project)
    ] for i in range(data.NUM_act)]

    # Order Time (OT) variables for each order, material, supplier and project
    OT = [[[[
        m.add_var(var_type=INTEGER, name=f'OT_{o+1}_{k+1}_{s+1}_{j+1}', lb=0)
        for j in range(data.NUM_project)]
        for s in range(data.NUM_sup)]
        for k in range(data.NUM_raw_mat)]
        for o in range(data.NUM_order)
    ]

    # x[o][k][s][j]: Quantity ordered for order o, raw mat k, supplier s, project j
    x = [[[[
        m.add_var(var_type=INTEGER, name=f'x_{o+1}_{k+1}_{s+1}_{j+1}', lb=0)
        for j in range(data.NUM_project)]
        for s in range(data.NUM_sup)]
        for k in range(data.NUM_raw_mat)]
        for o in range(data.NUM_order)
    ]

    # S[o][k][s][j]: Binary variable indicating if order o, raw mat k, supplier s is used for project j
    S = [[[[
        m.add_var(var_type=BINARY, name=f'S_{o+1}_{k+1}_{s+1}_{j+1}')
        for j in range(data.NUM_project)]
        for s in range(data.NUM_sup)]
        for k in range(data.NUM_raw_mat)]
        for o in range(data.NUM_order)
    ]

    # q[k][s][j]: Total quantity from raw material k, supplier s for project j
    q = [[[
        m.add_var(var_type=INTEGER, name=f'q_{k+1}_{s+1}_{j+1}', lb=0)
        for j in range(data.NUM_project)]
        for s in range(data.NUM_sup)]
        for k in range(data.NUM_raw_mat)
    ]

    # TD[j]: Time delay for project j
    TD = [m.add_var(var_type=INTEGER, name=f'TD_{j+1}', lb=0) for j in range(data.NUM_project)]

    # CT[j]: Completion time for project j
    CT = [m.add_var(var_type=INTEGER, name=f'CT_{j+1}', lb=0) for j in range(data.NUM_project)]

    # Cmax: Maximum completion time across all projects
    Cmax = m.add_var(var_type=INTEGER, name='Cmax', lb=0)

    # Objective Function: Minimize total penalties due to delays
    m.objective = minimize(xsum(data.Penalty[j] * TD[j] for j in range(data.NUM_project)))

    # Constraints

    # 1. Project completion time: CT[j] == FT[last_activity][j] for all j
    last_activity = data.NUM_act - 1  # Last activity (index 22 for activity 23)
    for j in range(data.NUM_project):
        m += CT[j] == FT[last_activity][j], f"completion_time_proj_{j+1}"

    # 2. Constraint for maximum completion time: Cmax >= CT[j] for all j
    for j in range(data.NUM_project):
        m += Cmax >= CT[j], f"Cmax_constraint_PROJ_{j+1}"

    # 3. Supplier capacity constraints: sum(q[k][s][j] for j) <= Capacity[k][s] for all k, s
    for k in range(data.NUM_raw_mat):
        for s in range(data.NUM_sup):
            if data.Capacity[k][s] > 0:  # Only add constraint if supplier has capacity for this material
                m += xsum(q[k][s][j] for j in range(data.NUM_project)) <= data.Capacity[k][s], \
                    f"capacity_constraint_k_{k+1}_s_{s+1}"

    # 4. Quantity constraints: sum(x[o][k][s][j] for o) == q[k][s][j] for all k, s, j
    for k in range(data.NUM_raw_mat):
        for s in range(data.NUM_sup):
            for j in range(data.NUM_project):
                m += xsum(x[o][k][s][j] for o in range(data.NUM_order)) == q[k][s][j], \
                    f"quantity_constraint_k_{k+1}_s_{s+1}_j_{j+1}"

    # 5. Demand constraints: sum(q[k][s][j] for s) >= Quantity[k][j] for all k, j
    for k in range(data.NUM_raw_mat):
        for j in range(data.NUM_project):
            m += xsum(q[k][s][j] for s in range(data.NUM_sup)) >= data.Quantity[k][j], \
                f"demand_constraint_k_{k+1}_j_{j+1}"

    # 6. Big-M Constraints: x[o][k][s][j] <= M * S[o][k][s][j] for all o, k, s, j
    for o in range(data.NUM_order):
        for k in range(data.NUM_raw_mat):
            for s in range(data.NUM_sup):
                for j in range(data.NUM_project):
                    if data.Capacity[k][s] > 0:  # Only add constraint for valid supplier-material combinations
                        m += x[o][k][s][j] <= M * S[o][k][s][j], \
                            f"BigM_x_S_constraint_o_{o+1}_k_{k+1}_s_{s+1}_j_{j+1}"

    # 7. Activity duration constraints: FT[i][j] == ST[i][j] + Duration[i][j] for all i, j
    for i in range(data.NUM_act):
        for j in range(data.NUM_project):
            m += FT[i][j] == ST[i][j] + data.Duration[i][j], f"FT_constraint_i_{i+1}_j_{j+1}"

    # 8. Precedence constraints: For each (a, b) in Pred, ST[b] >= FT[a] for all j
    for (a, b) in data.Pred:
        for j in range(data.NUM_project):
            m += ST[b][j] >= FT[a][j], f"precedence_constraint_a_{a+1}_b_{b+1}_proj_{j+1}"

    # 9. Time delay constraints: TD[j] >= CT[j] - Target[j] for all j
    for j in range(data.NUM_project):
        m += TD[j] >= CT[j] - data.Target[j], f"time_delay_constraint_proj_{j+1}"
        m += TD[j] >= 0, f"non_negative_delay_proj_{j+1}"  # Ensure non-negative delay

    # 10. Material arrival constraints: Ensure materials arrive before activities start
    for i in range(data.NUM_act):
        for j in range(data.NUM_project):
            for k in range(data.NUM_raw_mat):
                for s in range(data.NUM_sup):
                    for o in range(data.NUM_order):
                        if data.Capacity[k][s] > 0:  # Only for valid supplier-material combinations
                            m += ST[i][j] >= OT[o][k][s][j] + data.Delivery_Time[k][s][j] - M * (1 - S[o][k][s][j]), \
                                f"material_arrival_constraint_i_{i+1}_j_{j+1}_k_{k+1}_s_{s+1}_o_{o+1}"

    # 11. Ensure that all S[o][k][s][j] variables for orders with x[o][k][s][j]=0 are also 0
    for o in range(data.NUM_order):
        for k in range(data.NUM_raw_mat):
            for s in range(data.NUM_sup):
                for j in range(data.NUM_project):
                    if data.Capacity[k][s] > 0:
                        m += S[o][k][s][j] <= x[o][k][s][j], \
                            f"zero_order_constraint_o_{o+1}_k_{k+1}_s_{s+1}_j_{j+1}"

    # Solving the model
    print("Optimizing the model...")
    m.optimize(max_seconds=300)  # Set a time limit of 300 seconds (5 minutes)

    results = {}
    
    # Process results
    if m.status == OptimizationStatus.OPTIMAL or m.status == OptimizationStatus.FEASIBLE:
        status_str = "Optimal" if m.status == OptimizationStatus.OPTIMAL else "Feasible"
        print(f"Status: {status_str} solution found")
        print(f"Objective value (Total Penalty Cost): {m.objective_value}")
        
        # Extract solution values
        results['objective_value'] = m.objective_value
        results['status'] = status_str
        
        # Extract project completion times and delays
        results['completion_times'] = [CT[j].x for j in range(data.NUM_project)]
        results['delays'] = [TD[j].x for j in range(data.NUM_project)]
        results['penalties'] = [data.Penalty[j] * TD[j].x for j in range(data.NUM_project)]
        results['total_penalty'] = sum(results['penalties'])
        
        # Extract activity start and finish times
        start_times = [[ST[i][j].x for j in range(data.NUM_project)] for i in range(data.NUM_act)]
        finish_times = [[FT[i][j].x for j in range(data.NUM_project)] for i in range(data.NUM_act)]
        results['start_times'] = start_times
        results['finish_times'] = finish_times
        
        # Extract material allocations
        material_allocations = [[[[x[o][k][s][j].x for j in range(data.NUM_project)] 
                               for s in range(data.NUM_sup)] 
                              for k in range(data.NUM_raw_mat)] 
                             for o in range(data.NUM_order)]
        results['material_allocations'] = material_allocations
        
        # Extract supplier assignments
        supplier_assignments = [[[[S[o][k][s][j].x for j in range(data.NUM_project)] 
                               for s in range(data.NUM_sup)] 
                              for k in range(data.NUM_raw_mat)] 
                             for o in range(data.NUM_order)]
        results['supplier_assignments'] = supplier_assignments
        
        # Store raw data for visualization
        results['raw_data'] = data.get_all_data()
        
    else:
        print(f"Status: {m.status}")
        results['status'] = f"No solution found: {m.status}"
    
    return results

if __name__ == "__main__":
    # Solve the model and get results
    results = create_and_solve_model()
    
    if 'objective_value' in results:
        print("\nResults Summary:")
        print(f"Total Penalty Cost: {results['total_penalty']}")
        
        for j in range(results['raw_data']['NUM_project']):
            print(f"\nProject {j+1}:")
            print(f"  Completion Time: {results['completion_times'][j]}")
            print(f"  Target Date: {results['raw_data']['Target'][j]}")
            print(f"  Delay: {results['delays'][j]} days")
            print(f"  Penalty: {results['penalties'][j]} NIS")
        
        # Generate visualization charts
        plot_gantt_chart(results)
        plot_resource_usage(results)
        plot_project_delays(results)
        plot_supplier_allocation(results)
    
    print("\nModel execution completed.")
