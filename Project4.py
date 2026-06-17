import numpy as np
import matplotlib.pyplot as plt

# USER INPUTS


R = float(input("Enter Resistance R (Ω): "))
L = float(input("Enter Inductance L (H): "))
C = float(input("Enter Capacitance C (F): "))
V = float(input("Enter Supply Voltage (V): "))

# CALCULATIONS

f = np.logspace(1, 5, 1000)  # 10 Hz to 100 kHz

omega = 2 * np.pi * f

# Series RLC Impedance
Z = R + 1j * (omega * L - 1 / (omega * C))

Z_mag = np.abs(Z)

# Resonant Frequency
f0 = 1 / (2 * np.pi * np.sqrt(L * C))

# Quality Factor
Q = (1 / R) * np.sqrt(L / C)

# Bandwidth
BW = R / (2 * np.pi * L)

# Cutoff Frequencies
f1 = f0 - BW / 2
f2 = f0 + BW / 2

# Current Response
I = V / Z_mag

# Phase Angle
phase = np.angle(Z, deg=True)

# RESULTS

print("\n========== RLC CIRCUIT ANALYSIS ==========")

print(f"Resonant Frequency (f0) : {f0:.2f} Hz")
print(f"Quality Factor (Q)      : {Q:.2f}")
print(f"Bandwidth (BW)          : {BW:.2f} Hz")
print(f"Lower Cutoff Frequency  : {f1:.2f} Hz")
print(f"Upper Cutoff Frequency  : {f2:.2f} Hz")

print("\nAt Resonance:")
print(f"Impedance = {R:.2f} Ω")
print(f"Current   = {V/R:.2f} A")

# IMPEDANCE PLOT

plt.figure(figsize=(10,5))

plt.semilogx(f, Z_mag, linewidth=2)

plt.axvline(
    f0,
    color='red',
    linestyle='--',
    label=f'Resonance = {f0:.2f} Hz'
)

plt.xlabel("Frequency (Hz)")
plt.ylabel("Impedance Magnitude |Z| (Ω)")
plt.title("RLC Series Circuit - Impedance Response")
plt.grid(True)
plt.legend()

plt.show()

# CURRENT RESPONSE

plt.figure(figsize=(10,5))

plt.semilogx(f, I, linewidth=2)

plt.axvline(
    f0,
    color='red',
    linestyle='--',
    label=f'Resonance = {f0:.2f} Hz'
)

plt.xlabel("Frequency (Hz)")
plt.ylabel("Current (A)")
plt.title("Current vs Frequency")
plt.grid(True)
plt.legend()

plt.show()

# PHASE RESPONSE


plt.figure(figsize=(10,5))

plt.semilogx(f, phase, linewidth=2)

plt.axhline(
    0,
    color='red',
    linestyle='--',
    label='Resonance (0°)'
)

plt.xlabel("Frequency (Hz)")
plt.ylabel("Phase Angle (Degrees)")
plt.title("Phase Angle vs Frequency")
plt.grid(True)
plt.legend()

plt.show()