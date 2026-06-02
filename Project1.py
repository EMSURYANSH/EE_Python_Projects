import numpy as np
import matplotlib.pyplot as plt

# User Inputs
Vm = float(input("Enter Peak Voltage (Vm in Volts): "))
Im = float(input("Enter Peak Current (Im in Amperes): "))
pf = float(input("Enter Power Factor (0 to 1): "))
freq = float(input("Enter Frequency (Hz): "))

print("Load Types:")
print("1 - Resistive")
print("2 - Inductive")
print("3 - Capacitive")

Load = int(input("Enter Load Type (1-3): "))

# Validate PF
if pf < 0 or pf > 1:
    print("Power Factor must be between 0 and 1.")
    exit()

# Calculate phase angle
phi = np.degrees(np.arccos(pf))

# Time axis (2 cycles)
t = np.linspace(0, 2/freq, 1000)

# Voltage waveform (reference)
V = Vm * np.sin(2 * np.pi * freq * t)

# Current waveform according to load type
if Load == 1:
    I = Im * np.sin(2 * np.pi * freq * t)
    load_name = "Resistive"

elif Load == 2:
    I = Im * np.sin(2 * np.pi * freq * t - np.radians(phi))
    load_name = "Inductive (Current Lags)"

elif Load == 3:
    I = Im * np.sin(2 * np.pi * freq * t + np.radians(phi))
    load_name = "Capacitive (Current Leads)"

else:
    print("Invalid Load Type!")
    exit()

# Plotting
plt.figure(figsize=(10, 5))

plt.plot(
    t * 1000,
    V,
    label=f'Voltage (Vm = {Vm} V)',
    linewidth=2
)

plt.plot(
    t * 1000,
    I * (Vm / Im) * 0.4,
    label=f'Current (Im = {Im} A)',
    linewidth=2
)

plt.title(
    f'AC Waveforms | {load_name} | PF = {pf} | Phase Angle = {phi:.2f}°'
)

plt.xlabel('Time (ms)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.legend()

plt.show()