import tkinter as tk
import re
from tkinter import filedialog
import datetime
import csv
import os
import configparser

config = configparser.ConfigParser()
filename = 'printer.csv'

# retrieve values
config.read('config.ini')
material_price_per_m = float(config['DEFAULT']['material_price_per_m'])
electricity_cost_per_hour = float(config['DEFAULT']['electricity_cost_per_hour'])
printer_consumption = float(config['DEFAULT']['printer_consumption'])
print_price = float(config['DEFAULT']['print_price'])

# Create a Tkinter window
root = tk.Tk()
root.geometry("600x400")
root.columnconfigure([0, 1, 2, 3], minsize=100)
root.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], minsize=30)
root.title("Cost Calculator")

# Define the function to open a file dialog
def open_file_dialog(material_cost_label, print_time_label, filament_used_label, electricity_cost_label, total_cost_label, filament_weight_label):
    # Open the file dialog
    file_path = filedialog.askopenfilename(filetypes=[("G-Code Files", "*.gcode")])
    # Check if a file was selected
    if file_path:
        # Display the selected file
        file_label.config(text=file_path)
        with open(file_path, "r") as file:
            gcode = file.read()
        # Extract the relevant information from the G-Code
        match = re.search(";Filament used: (\d+\.\d+)m", gcode)
        if match:
            filament_used = float(match.group(1))
        else:
                file_label.config(text="Invalid G-Code file")

        match = re.search(";TIME:(\d+)", gcode)
        if match:
            print_time = int(match.group(1)) / 3600 # convert seconds to minutes
        else:
                file_label.config(text="Invalid G-Code file")

        # Variables
        filament_weight = 1000 / 335 * filament_used #1000g / 335m * filament used
        material_cost = filament_used * material_price_per_m
        electricity_cost = print_time * electricity_cost_per_hour * printer_consumption
        print_cost = print_time * print_price
        cost = material_cost + electricity_cost + print_cost
        total_cost = cost * 1.3 #30% profit margin

        # TODO - fix base_name
        base_name = os.path.splitext(file_path)[0]
        now = datetime.datetime.now()
    
    header = ["Label", "Date", "Printing time", "Filament weight", "Filament used", "Material cost", "Electricity cost", "Total cost"]
   
    if not os.path.exists(filename):
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)

    data = [base_name, now, print_time, filament_weight, filament_used, material_cost, electricity_cost, total_cost]

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)

    # Update the labels
    print_time_label.config(text=f"Printing time: {print_time:.2f} hours")
    print_time_label.grid(row=1, column=0, sticky="w")

    filament_weight_label.config(text=f"Filament weigth: {filament_weight:.2f} g")
    filament_weight_label.grid(row=2, column=0, sticky="w")

    filament_used_label.config(text=f"Filament used: {filament_used:.2f} m")
    filament_used_label.grid(row=3, column=0, sticky="w")

    material_cost_label.config(text=f"Material cost: {material_cost:.2f} €")
    material_cost_label.grid(row=4, column=0, sticky="w")

    electricity_cost_label.config(text=f"Electricity cost : {electricity_cost:.2f} €")
    electricity_cost_label.grid(row=5, column=0, sticky="w")

    total_cost_label.config(text=f"Total cost: {total_cost:.2f} €")
    total_cost_label.grid(row=6, column=0, sticky="w")

# Create a button to open the file dialog


file_label = tk.Label(root, text="No file selected")
file_label.grid(row=0, column=0, sticky="w")

print_time_label = tk.Label(root, text="Printing time: ")
print_time_label.grid(row=1, column=0, sticky="w")

filament_weight_label = tk.Label(root, text="Filament weight: ")
filament_weight_label.grid(row=2, column=0, sticky="w")

filament_used_label = tk.Label(root, text="Filament used: ")
filament_used_label.grid(row=3, column=0, sticky="w")

material_cost_label = tk.Label(root, text="Material cost: ")
material_cost_label.grid(row=4, column=0, sticky="w")

electricity_cost_label = tk.Label(root, text="Electricity: ")
electricity_cost_label.grid(row=5, column=0, sticky="w")

total_cost_label = tk.Label(root, text="Total cost: ")
total_cost_label.grid(row=6, column=0, sticky="w")

filament_used_button = tk.Button(root, text="Open file", command=lambda: open_file_dialog(material_cost_label, print_time_label, filament_used_label, electricity_cost_label, total_cost_label, filament_weight_label))
filament_used_button.grid(row=7, column=0, sticky="w")

root.mainloop()




