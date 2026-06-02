import numpy as np
import matplotlib.pyplot as plt

# INPUTS

kVA = float(input("Enter Transformer Rating (kVA): "))
Pi = float(input("Enter Iron Loss, Pi (W): "))
Pcu_fl = float(input("Enter Full Load Copper Loss, Pcu_fl (W): "))
pf = float(input("Enter Power Factor (0 to 1): "))
load_percent = float(input("Enter Operating Load (%): "))

# Convert load percentage to per-unit
x_load = load_percent / 100

# EFFICIENCY CURVE DATA

x_curve = np.linspace(0.01, 1.25, 200)

output_curve = x_curve * kVA * 1000 * pf
losses_curve = Pi + (x_curve**2) * Pcu_fl

eta_curve = (
    output_curve /
    (output_curve + losses_curve)
) * 100

# OPERATING LOAD CALCULATIONS

output_load = x_load * kVA * 1000 * pf

copper_loss_load = (x_load**2) * Pcu_fl

losses_load = Pi + copper_loss_load

eta_load = (
    output_load /
    (output_load + losses_load)
) * 100

# EFFICIENCY TABLE

load_points = [25, 50, 75, 100, 125]

print("\n===== EFFICIENCY TABLE =====")
print(f"{'Load (%)':<12}{'Efficiency (%)':<15}")

for load in load_points:

    x_table = load / 100

    output_table = x_table * kVA * 1000 * pf

    losses_table = Pi + (x_table**2) * Pcu_fl

    eta_table = (
        output_table /
        (output_table + losses_table)
    ) * 100

    print(f"{load:<12}{eta_table:.2f}")

# MAXIMUM EFFICIENCY

x_max = np.sqrt(Pi / Pcu_fl)

if x_max > 1.25:
    x_max = 1.25

eta_max = (
    (x_max * kVA * 1000 * pf)
    /
    (
        x_max * kVA * 1000 * pf
        + Pi
        + (x_max**2) * Pcu_fl
    )
) * 100

# PLOT

plt.figure(figsize=(10, 6))

# Efficiency curve
plt.plot(
    x_curve * 100,
    eta_curve,
    linewidth=2,
    label="Efficiency Curve"
)

# Maximum efficiency point
plt.scatter(
    x_max * 100,
    eta_max,
    s=100,
    zorder=5,
    label=f"Maximum η = {eta_max:.2f}%"
)

# Operating load point
plt.scatter(
    load_percent,
    eta_load,
    s=100,
    zorder=5,
    label=f"η at {load_percent:.0f}% Load = {eta_load:.2f}%"
)

# Vertical line at operating load
plt.axvline(
    x=load_percent,
    linestyle='--',
    alpha=0.7,
    label=f'Operating Load ({load_percent:.0f}%)'
)

# Standard load points
standard_loads = np.array([25, 50, 75, 100, 125])

for load in standard_loads:

    x_std = load / 100

    eta_std = (
        (x_std * kVA * 1000 * pf)
        /
        (
            x_std * kVA * 1000 * pf
            + Pi
            + (x_std**2) * Pcu_fl
        )
    ) * 100

    plt.scatter(load, eta_std, s=40)

plt.xlabel("Load (%)")
plt.ylabel("Efficiency (%)")
plt.title(f"{kVA} kVA Transformer Efficiency Curve")
plt.grid(True)
plt.legend()

plt.show()

# RESULTS

print("\n===== TRANSFORMER PERFORMANCE =====")

print(f"Operating Load      : {load_percent:.2f}%")
print(f"Output Power        : {output_load:.2f} W")
print(f"Iron Loss           : {Pi:.2f} W")
print(f"Copper Loss         : {copper_loss_load:.2f} W")
print(f"Total Loss          : {losses_load:.2f} W")
print(f"Efficiency          : {eta_load:.2f}%")

print("\n===== MAXIMUM EFFICIENCY =====")

print(f"Maximum Efficiency  : {eta_max:.2f}%")
print(f"Occurs at Load      : {x_max * 100:.2f}%")

print("\nCondition for Maximum Efficiency:")
print("Iron Loss = Copper Loss")