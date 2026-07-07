import requests
import matplotlib.pyplot as plt
import calendar

print("===== SOLAR OUTPUT ESTIMATOR =====\n")

city = input("Enter City Name: ")

lat = float(input("Enter Latitude: "))
lon = float(input("Enter Longitude: "))

panel_power = float(input("Enter Panel Rating (kW): "))
num_panels = int(input("Enter Number of Panels: "))
system_efficiency = float(input("Enter System Efficiency (0-1): "))
tariff = float(input("Enter Electricity Rate (₹/kWh): "))

url = (
    f"https://power.larc.nasa.gov/api/temporal/monthly/point"
    f"?parameters=ALLSKY_SFC_SW_DWN"
    f"&community=RE"
    f"&longitude={lon}"
    f"&latitude={lat}"
    f"&format=JSON"
    f"&start=2022"
    f"&end=2022"
)

response = requests.get(url)

if response.status_code != 200:
    print("Error fetching data.")
    exit()

data = response.json()

irr = data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]

months = list(irr.keys())[:12]

peak_sun_hours = [irr[m] for m in months]

days = [calendar.monthrange(2022, i + 1)[1] for i in range(12)]

monthly_energy = []

for psh, d in zip(peak_sun_hours, days):
    energy = (
        panel_power
        * num_panels
        * psh
        * system_efficiency
        * d
    )
    monthly_energy.append(energy)

annual_energy = sum(monthly_energy)

daily_average = annual_energy / 365

co2_saved = annual_energy * 0.82       # kg CO₂/year

money_saved = annual_energy * tariff

print("\n========== RESULTS ==========\n")

print(f"City                 : {city}")
print(f"Annual Energy        : {annual_energy:.2f} kWh")
print(f"Average Daily Energy : {daily_average:.2f} kWh/day")
print(f"CO₂ Saved            : {co2_saved:.2f} kg/year")
print(f"Money Saved          : ₹{money_saved:.2f}/year")

print("\nMonthly Energy Output\n")

month_names = ["Jan","Feb","Mar","Apr","May","Jun",
               "Jul","Aug","Sep","Oct","Nov","Dec"]

print("-------------------------------------")
print("Month\tEnergy (kWh)")
print("-------------------------------------")

for m,e in zip(month_names,monthly_energy):
    print(f"{m}\t{e:.2f}")

plt.figure(figsize=(11,6))

plt.bar(
    month_names,
    monthly_energy,
    color="orange",
    edgecolor="black"
)

plt.title(f"Monthly Solar Energy Output - {city}")
plt.xlabel("Month")
plt.ylabel("Energy (kWh)")
plt.grid(axis="y")
plt.show()