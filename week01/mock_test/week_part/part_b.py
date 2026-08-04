import json

def add_item(name, qty, inventory=[]):
    inventory.append({"name": name, "qty": qty})
    return inventory

def total_qty(inventory):
    total = 0
    for i in range(len(inventory)):
        total = total + inventory[i]["qty"]
    return total

def load_inventory(path):
    f = open(path)
    try:
        data = json.load(f)
    except:
        data = []
    return data

def price_report(inventory, prices):
    report = ""
    for item in inventory:
        if prices.get(item["name"]) == None:
            continue
        value = item["qty"] * float(prices[item["name"]])
        report = report + item["name"] + ": " + str(value) + "\n"
    return report

def unique_names(inventory):
    list = []
    for item in inventory:
        if not item["name"] in list:
            list.append(item["name"])
    return list


##CORRECTED VERSION

def add_item(name, qty, inventory=None):
    if inventory is None:
        inventory = []

    inventory.append({"name": name, "qty": qty})
    return inventory

def total_qty(inventory):
    total = 0

    for item in inventory:
        total += item["qty"]

    return total

def load_inventory(path):
    with open(path) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

    return data

def unique_names(inventory):
    names = []

    for item in inventory:
        if item["name"] not in names:
            names.append(item["name"])

    return names