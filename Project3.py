import math

# USER INPUTS

P = float(input("Enter Load Power (kW): "))
pf_old = float(input("Enter Existing Power Factor: "))
pf_new = float(input("Enter Target Power Factor: "))
V = float(input("Enter Supply Voltage (V): "))
f = float(input("Enter Supply Frequency (Hz): "))
tariff = float(input("Enter Electricity Tariff (Rs/kWh): "))

# CALCULATIONS

theta1 = math.acos(pf_old)
theta2 = math.acos(pf_new)

Q_old = P * math.tan(theta1)
Q_new = P * math.tan(theta2)

Q_cap = Q_old - Q_new

Xc = (V**2) / (Q_cap * 1000)

C = (1 / (2 * math.pi * f * Xc)) * 1e6  # μF

I_old = (P * 1000) / (V * pf_old)
I_new = (P * 1000) / (V * pf_new)

current_reduction = ((I_old - I_new) / I_old) * 100

savings = tariff * P * (1/pf_old - 1/pf_new) * 720

# RESULTS

print("\n===== POWER FACTOR CORRECTION RESULTS =====")

print(f"Existing Reactive Power      : {Q_old:.2f} kVAR")
print(f"Target Reactive Power        : {Q_new:.2f} kVAR")
print(f"Reactive Power Compensated   : {Q_cap:.2f} kVAR")

print(f"\nRequired Capacitor Value     : {C:.2f} μF")

print(f"\nOld Current                  : {I_old:.2f} A")
print(f"New Current                  : {I_new:.2f} A")
print(f"Current Reduction            : {current_reduction:.2f}%")

print(f"\nEstimated Monthly Savings    : Rs. {savings:.2f}")