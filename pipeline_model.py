
import math
import matplotlib.pyplot as plt
import sys


# Darcy–Weisbach Head Loss equation
def HEADLOSS(f, L, v, D, g=9.81):
    return (f * L * v**2) / (2 * g * D)

#the dictionary for material properties
materials_properties = {
    "PVC": {"epsilon": 0.0015e-3, "cost": 20, "degrade_rate": 0.0000e-3},
    "HDPE": {"epsilon": 0.01e-3, "cost": 25, "degrade_rate": 0.0001e-3},
    "Ductile Iron": {"epsilon": 0.26e-3, "cost": 40, "degrade_rate": 0.02e-3},
    "Steel": {"epsilon": 0.045e-3, "cost": 35, "degrade_rate": 0.03e-3},
    "Concrete": {"epsilon": 0.3e-3, "cost": 60, "degrade_rate": 0.05e-3},
    "Galvanized Steel": {"epsilon": 0.15e-3, "cost": 30, "degrade_rate": 0.04e-3}
}

#the dictionary for fluid properties
fluids_properties = {
    "water_0C":  {"rho": 999.8,  "mu": 1.792e-3, "Pv": 611},
    "water_10C": {"rho": 999.7,  "mu": 1.307e-3, "Pv": 1228},
    "water_20C": {"rho": 998.1,  "mu": 1.002e-3, "Pv": 2340},
    "water_40C": {"rho": 992.2,  "mu": 6.53e-4, "Pv": 7380},
    "water_60C": {"rho": 983.2,  "mu": 4.66e-4, "Pv": 19950},
    "water_80C": {"rho": 971.8,  "mu": 3.55e-4, "Pv": 47330},

    "oil_light_20C":  {"rho": 860, "mu": 0.030,   "Pv": 5},
    "oil_light_40C":  {"rho": 850, "mu": 0.008,   "Pv": 20},
    "oil_light_60C":  {"rho": 840, "mu": 0.0045,  "Pv": 40},

    "oil_medium_20C": {"rho": 875, "mu": 0.265,   "Pv": 10},
    "oil_medium_40C": {"rho": 860, "mu": 0.040,   "Pv": 35},
    "oil_medium_60C": {"rho": 845, "mu": 0.018,   "Pv": 70},
}


fluids_menu = {
    1: "water_0C",
    2: "water_10C",
    3: "water_20C",
    4: "water_40C",
    5: "water_60C",
    6: "water_80C",
    7: "oil_light_20C",
    8: "oil_light_40C",
    9: "oil_light_60C",
    10: "oil_medium_20C",
    11: "oil_medium_40C",
    12: "oil_medium_60C"
}
user_choice_of_fluid = int(input("""
==================== FLUID SELECTION ====================

  WATER (by temperature)
    1 → Water @ 0°C
    2 → Water @ 10°C
    3 → Water @ 20°C
    4 → Water @ 40°C
    5 → Water @ 60°C
    6 → Water @ 80°C

  LIGHT OIL (ISO-type, Diesel, kerosene, light crude)
    7 → Light Oil @ 20°C
    8 → Light Oil @ 40°C
    9 → Light Oil @ 60°C

  MEDIUM OIL (SAE-type, Heavy crude, lubricating oil)
    10 → Medium Oil @ 20°C
    11 → Medium Oil @ 40°C
    12 → Medium Oil @ 60°C

=========================================================
"""))

fluid = fluids_menu.get(user_choice_of_fluid)

if fluid is None:
    print("Invalid choice")
    exit()
else:
    print("You have selected", fluid)    

# Extract fluid properties
RHO = fluids_properties[fluid]["rho"]
mu = fluids_properties[fluid]["mu"]
P_VAP = fluids_properties[fluid]["Pv"]

menu = {
    1: "PVC",
    2: "HDPE",
    3: "Ductile Iron",
    4: "Steel",
    5: "Concrete",
    6: "Galvanized Steel"
}

user_choice = int(input("""
==================== MATERIAL SELECTION ====================

Choose material:
1 → PVC
2 → HDPE
3 → Ductile Iron
4 → Steel
5 → Concrete
6 → Galvanized Steel
=========================================================

Enter number: """))

material = menu.get(user_choice)

if material is None:
    print("Invalid choice")
    exit()
else:
    print("You have selected", material)


epsilon_material = materials_properties[material]["epsilon"]
cost_material = materials_properties[material]["cost"]
decay_material = materials_properties[material]["degrade_rate"]

L = float(input("Enter pipe length (m): "))
v = float(input("Enter velocity (m/s): "))
D = float(input("Enter pipe diameter (m): "))



#The model is restricted to fully turbulent flow (Re > 4000). Laminar and transitional cases are not evaluated.
def Re(RHO, v, D, mu):
    return (RHO * v * D) / mu

Re_value = Re(RHO, v, D, mu)

if Re_value > 4000:
    print("Turbulent flow, matches assumptions")
else:
    print("WARNING: Laminar or transitional flow — Swamee–Jain not applicable. Results may be invalid.")
    print("Simulation terminated due to violated flow-regime assumptions.")
    sys.exit()



# Swamee–Jain friction factor is used, as a approxmation to the colebrook
#valid for RE > 4000
def swamee_jain(epsilon, D, Re_value):
    return 0.25 / (
        math.log10(
            (epsilon / (3.7 * D)) +
            (5.74 / (Re_value ** 0.9))
        )
    )**2


# Friction factor using Swamee–Jain
f = swamee_jain(epsilon_material, D, Re_value)

# Head loss
hl = HEADLOSS(f, L, v, D)


# Cost assumed in $/m. Values are placeholders for comparative analysis
# and do not represent actual industry pricing.
# Pipe material cost is assumed to scale nonlinearly with diameter (D^1.75),
# reflecting material, manufacturing, and handling effects.
# Labor cost is assumed equal for all materials and modeled as a constant $50/m,
# dependent only on pipe length.


labour_cost = 50 * L

pipe_cost = cost_material * L * (D ** 1.75)

total_cost = pipe_cost + labour_cost


# Linear roughness growth model is used 
def epsilon_over_time(epsilon_material, decay_material):
    epsilon_values = []
    for t in range(6):
        epsilon_new = epsilon_material + decay_material * t
        epsilon_values.append(epsilon_new)
    return epsilon_values

epsilon_list = epsilon_over_time(epsilon_material, decay_material)

print("\nEpsilon evolution:")
for t in range(len(epsilon_list)):
    print("Year", t, ": epsilon =", round(epsilon_list[t], 6))




    
def friction_factor_growth(epsilon_list, D, Re_value):
    friction_factor_values = []
    
    for epsilon in epsilon_list:
        f_new = swamee_jain(epsilon, D, Re_value)
        friction_factor_values.append(f_new)
        
    return friction_factor_values

# compute list of friction factors over time
friction_factor_list = friction_factor_growth(epsilon_list, D, Re_value)

print("\nFriction Factor Evolution:")
for t in range(len(friction_factor_list)):
    print("Year", t, ": friction factor =", round(friction_factor_list[t], 6))



def HEAD_LOSS_GROWTH(friction_factor_list, L, v, D, g=9.81):
    headloss_values = []
    
    for f in friction_factor_list:
        HL_new = HEADLOSS(f, L, v, D)
        headloss_values.append(HL_new)
        
    return headloss_values

HEADLOSS_list = HEAD_LOSS_GROWTH(friction_factor_list, L, v, D)

print("\nHEADLOSS Evolution:")
for t in range(len(HEADLOSS_list)):
    print("Year", t, ": HEAD LOSS =", round(HEADLOSS_list[t], 6))

# Cavitation Assumptions:
# - A free surface is assumed 
# - Pressure is referenced to atmospheric pressure
# - Vapor pressure comes from selected fluid
# - Cavitation threshold uses h_max = (P_atm - P_v) / (rho * g)
# - A factor of Saftey of 2.5 will be used

P_atm = 101325  # Pa (standard atmospheric pressure)
FOS = 2.5

g = 9.81  # m/s^2

# Compute maximum allowable head loss before cavitation
h_max = ((P_atm - P_VAP) / (RHO * g))
h_allow = h_max/FOS

print(f"Maximum allowable head loss before cavitation: {h_allow:.3f} m")

model_safe = True   # assume safe until proven otherwise

for t in range(len(HEADLOSS_list)):
    HL = HEADLOSS_list[t]
    if HL > h_allow:
        model_safe = False
        break  # one failure ruins everything

if not model_safe:
    print(" !!! WARNING: CAVITATION FAILURE !!!: Cavitation risk detected. Redesign required.")
else:
    print("MODEL SAFE: Based on assumptions and cavitation limits.")




print("\nRESULTS")
print("COSTS:")
print("  Labour Cost: $", round(labour_cost, 2))
print("  Pipe Cost:   $", round(pipe_cost, 2))
print("  Total Cost:  $", round(total_cost, 2))
print(f"Material: {material}")
print(f"Fluid Selected: {fluid}")
print(f"Reynolds number: {Re_value:.2e}")
print(f"Initial friction factor: {f:.5f}")
print(f"Intial Head loss: {hl:.3f} m")


# HEAD LOSS AGAINST TIME
years1 = list(range(len(HEADLOSS_list)))
HL = HEADLOSS_list

plt.plot(years1, HL, marker='o', linewidth=2)
plt.xlabel("Year")
plt.ylabel("Head Loss (m)")
plt.title("Head Loss Growth Over Time")
plt.grid(True)
plt.show()


# Friction factor AGAINST TIME

years2 = list(range(len(friction_factor_list)))
FF = friction_factor_list


plt.plot(years2, FF, marker='o', linewidth=2)
plt.xlabel("Year")
plt.ylabel("Friction Factor")
plt.title("Friction Factor Growth Over Time")
plt.grid(True)
plt.show()



