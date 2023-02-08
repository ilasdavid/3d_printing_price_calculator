import tkinter as tk
import re
from tkinter import filedialog
import datetime
import csv

material_price_per_m = 0.06
electricity_cost_per_hour = 0.8
printer_consumption = 0.350
print_price = 1

# Create a Tkinter window
root = tk.Tk()
root.geometry("400x200")
root.title("G-Code File Loader")

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

        filament_weight = 1000 / 335 * filament_used #1000g / 335m * filament used
        material_cost = filament_used * material_price_per_m
        electricity_cost = print_time * electricity_cost_per_hour * printer_consumption
        print_cost = print_time * print_price
        cost = material_cost + electricity_cost + print_cost
        total_cost = cost * 1.3 #30% profit margin

    with open('costs.csv', "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Filament used (g)", "Material cost ($)", "Print time (minutes)", "Electricity cost ($)", "Print cost ($)", "Total cost ($)"])
        writer.writerow([filament_weight, material_cost, print_time, electricity_cost, print_cost, total_cost])

    print_time_label.config(text=f"Printing time: {print_time:.2f} hours")
    filament_weight_label.config(text=f"Filament weigth: {filament_weight:.2f} g")
    filament_used_label.config(text=f"Filament used: {filament_used:.2f} m")
    material_cost_label.config(text=f"Material cost: {material_cost:.2f} €")
    electricity_cost_label.config(text=f"Electricity cost : {electricity_cost:.2f} €")
    total_cost_label.config(text=f"Total cost: {total_cost:.2f} €")


file_label = tk.Label(root, text="No file selected")
file_label.pack()

print_time_label = tk.Label(root, text="Printing time: ")
print_time_label.pack()

filament_weight_label = tk.Label(root, text="Filament weight: ")
filament_weight_label.pack()

filament_used_label = tk.Label(root, text="Filament used: ")
filament_used_label.pack()

material_cost_label = tk.Label(root, text="Material cost: ")
material_cost_label.pack()

electricity_cost_label = tk.Label(root, text="Electricity: ")
electricity_cost_label.pack()

total_cost_label = tk.Label(root, text="Total cost: ")
total_cost_label.pack()

filament_used_button = tk.Button(root, text="Open file", command=lambda: open_file_dialog(material_cost_label, print_time_label, filament_used_label, electricity_cost_label, total_cost_label, filament_weight_label))
filament_used_button.pack()

root.mainloop()




