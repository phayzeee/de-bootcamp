from typing import Any, Counter


def displayInventory(inventory):
    print("Inventory: ")
    item_total = 0
    for k,v in inventory.items():
        print(k,v)
        item_total = item_total + v

    print("Total no of items: ", item_total)


stuff = {'rope': 1, 'torch': 6, 'gold coin': 42, 'dagger': 1, 'arrow': 12}
# displayInventory(stuff)

def invertDictionary(org: dict[str, int]) -> dict[int, str]:
    swapped = {value: key for key, value in org.items()}
    return swapped

student = {
    "Ali": 90,
    "Sara": 95
}
print(invertDictionary(org=student))

print(Counter("banana").most_common(2))