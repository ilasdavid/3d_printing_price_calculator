import re
import os
import datetime

# Constants
material_price_per_m = 0.06
electricity_cost_per_hour = 0.8
printer_consumption = 0.350
print_price = 1

filename = "dispenser.gcode"

base_name = os.path.splitext(filename)[0]
now = datetime.datetime.now()

# Read the G-Code file into a string
with open(filename, "r") as file:
    gcode = file.read()

# Extract the relevant information from the G-Code
match = re.search(";Filament used: (\d+\.\d+)m", gcode)
if match:
    filament_used = float(match.group(1))
else:
    print("Error: filament used not found in G-Code file")

match = re.search(";TIME:(\d+)", gcode)
if match:
    print_time = int(match.group(1)) / 3600 # convert seconds to minutes
else:
    print("Error: print time not found in G-Code file")

# Estimate the cost
material_cost = filament_used * material_price_per_m
electricity_cost = print_time * electricity_cost_per_hour * printer_consumption
filament_weight = 1000 / 335 * filament_used
print_cost = print_time * print_price
cost = material_cost + electricity_cost + print_cost
total_cost = cost * 1.3

print("Base name:", base_name)
print("Date and time:", now.strftime("%d-%m-%Y %H:%M:%S"))
print("Printing time:", print_time, "hours")
print("Filament weight:", filament_weight, "g")
print("Filament used:", filament_used, "m")
print("Material cost:", material_cost, "dollars")
print("Electricity cost:", electricity_cost, "dollars")
print("Total cost:", total_cost, "dollars")