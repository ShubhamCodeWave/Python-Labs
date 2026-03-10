N = 3
appliances = [("Fan", 75, 10), ("Light", 20, 6), ("TV", 150, 4)]
total_units = 0

for appliance in appliances:
    name, wattage, hours = appliance
    units = (wattage * hours * 30) / 1000
    total_units += units
bill = total_units * 5
print(f"the totle bill: {bill:}")