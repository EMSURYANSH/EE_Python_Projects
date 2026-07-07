import sys
import datetime
import requests
import matplotlib.pyplot as plt
import calendar

print("===== SOLAR OUTPUT ESTIMATOR =====\n")

def get_float(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = float(input(prompt))
            if min_val is not None and val < min_val:
                print(f"Value must be >= {min_val}. Try again.")
                continue
            if max_val is not None and val > max_val:
                print(f"Value must be <= {max_val}. Try again.")
                continue
            return val
        except ValueError:
            print("Please enter a valid number.")


def get_int(prompt, min_val=1):
    while True:
        try:
            val = int(input(prompt))
            if val < min_val:
                print(f"Value must be >= {min_val}. Try again.")
                continue
            return val
        except ValueError:
            print("Please enter a valid whole number.")


city = input("Enter City Name: ").strip() or "Unknown Location"

lat = get_float("Enter Latitude (-90 to 90): ", -90, 90)
lon = get_float("Enter Longitude (-180 to 180): ", -180, 180)

panel_power = get_float("Enter Panel Rating (kW): ", 0)
num_panels = get_int("Enter Number of Panels: ", 1)
system_efficiency = get_float("Enter System Efficiency (0-1): ", 0, 1)
tariff = get_float("Enter Electricity Rate (₹/kWh): ", 0)

# ---------------------------------------------------------
# FETCH IRRADIANCE DATA FROM NASA POWER
# Instead of a hardcoded old year, try the most recent year
# that should have complete monthly data, then fall back a
# year at a time if that year isn't available yet (NASA POWER
# monthly data typically lags real time by a few months).
# ---------------------------------------------------------

current_year = datetime.datetime.now().year
candidate_years = [current_year - 1, current_year - 2, current_year - 3]

month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

irr = None
used_year = None

for year in candidate_years:
    url = (
        f"https://power.larc.nasa.gov/api/temporal/monthly/point"
        f"?parameters=ALLSKY_SFC_SW_DWN"
        f"&community=RE"
        f"&longitude={lon}"
        f"&latitude={lat}"
        f"&format=JSON"
        f"&start={year}"
        f"&end={year}"
    )
    try:
        response = requests.get(url, timeout=15)
    except requests.exceptions.RequestException as e:
        print(f"Network error while trying {year} data: {e}")
        continue

    if response.status_code != 200:
        print(f"No data available for {year} (status {response.status_code}), trying an earlier year...")
        continue

    try:
        data = response.json()
        candidate_irr = data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
    except (KeyError, ValueError) as e:
        print(f"Unexpected response format for {year}: {e}")
        continue

    # Build explicit month keys instead of trusting dict ordering,
    # since the API also returns an "ANN" (annual average) key.
    expected_keys = [f"{year}{m:02d}" for m in range(1, 13)]
    if all(k in candidate_irr for k in expected_keys):
        irr = {k: candidate_irr[k] for k in expected_keys}
        used_year = year
        break
    else:
        print(f"Incomplete monthly data for {year}, trying an earlier year...")

if irr is None:
    print("\nCould not retrieve usable solar irradiance data after several attempts.")
    print("Check your internet connection, latitude/longitude, or try again later.")
    sys.exit(1)

print(f"\nUsing NASA POWER data for year: {used_year}\n")

peak_sun_hours = [irr[f"{used_year}{m:02d}"] for m in range(1, 13)]
days = [calendar.monthrange(used_year, i + 1)[1] for i in range(12)]

# ---------------------------------------------------------
# ENERGY CALCULATIONS
# ---------------------------------------------------------

monthly_energy = []
for psh, d in zip(peak_sun_hours, days):
    energy = panel_power * num_panels * psh * system_efficiency * d
    monthly_energy.append(energy)

annual_energy = sum(monthly_energy)
daily_average = annual_energy / 365

# Grid CO2 emission factor (kg CO2 per kWh). 0.82 was a commonly cited
# older figure; CEA's more recent CO2 Baseline Database reports lower
# combined-margin values for the Indian grid. Treat this as an editable
# assumption, not a fixed constant, since it changes as the grid mix shifts.
CO2_FACTOR = 0.82
co2_saved = annual_energy * CO2_FACTOR

money_saved = annual_energy * tariff

# ---------------------------------------------------------
# OUTPUT
# ---------------------------------------------------------

print("\n========== RESULTS ==========\n")
print(f"City                 : {city}")
print(f"Data Year Used       : {used_year}")
print(f"Annual Energy        : {annual_energy:.2f} kWh")
print(f"Average Daily Energy : {daily_average:.2f} kWh/day")
print(f"CO₂ Saved            : {co2_saved:.2f} kg/year (at {CO2_FACTOR} kg/kWh)")
print(f"Money Saved          : ₹{money_saved:.2f}/year")

print("\nMonthly Energy Output\n")
print("-------------------------------------")
print("Month\tEnergy (kWh)")
print("-------------------------------------")
for m, e in zip(month_names, monthly_energy):
    print(f"{m}\t{e:.2f}")

# ---------------------------------------------------------
# PLOT
# ---------------------------------------------------------

plt.figure(figsize=(11, 6))
plt.bar(month_names, monthly_energy, color="orange", edgecolor="black")
plt.title(f"Monthly Solar Energy Output - {city} ({used_year} data)")
plt.xlabel("Month")
plt.ylabel("Energy (kWh)")
plt.grid(axis="y")
plt.tight_layout()

output_file = "solar_output_chart.png"
plt.savefig(output_file, dpi=150)
print(f"\nChart saved as: {output_file}")

plt.show()