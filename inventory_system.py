"""
A simple JSON-based inventory management system.

This module allows users to add, remove, and query item quantities,
and persist the inventory data to a JSON file.
"""

import json
import sys
from datetime import datetime


class InventoryManager:
    """Manages inventory data, handling loading, saving, and updates."""

    def __init__(self, default_file="inventory.json"):
        """
        Initializes the InventoryManager.

        Args:
            default_file (str): The default JSON file to use for load/save.
        """
        self.stock_data = {}
        self.default_file = default_file
        # This log is now part of the class, not a mutable default arg
        self.logs = []

    def add_item(self, item: str, qty: int):
        """
        Adds a specified quantity of an item to the inventory.

        Args:
            item (str): The name of the item to add.
            qty (int): The positive quantity to add.
        """
        if not isinstance(item, str) or not item:
            print(f"Error: Item name '{item}' must be a non-empty string.")
            return

        if not isinstance(qty, int) or qty <= 0:
            print(f"Error: Quantity '{qty}' must be a positive integer.")
            return

        self.stock_data[item] = self.stock_data.get(item, 0) + qty
        log_entry = f"{datetime.now()}: Added {qty} of {item}"
        self.logs.append(log_entry)
        print(log_entry)

    def remove_item(self, item: str, qty: int):
        """
        Removes a specified quantity of an item from the inventory.

        Checks for item existence and sufficient stock before removal.

        Args:
            item (str): The name of the item to remove.
            qty (int): The positive quantity to remove.
        """
        if not isinstance(item, str) or not item:
            print(f"Error: Item name '{item}' must be a non-empty string.")
            return

        if not isinstance(qty, int) or qty <= 0:
            print(f"Error: Quantity '{qty}' must be a positive integer.")
            return

        if item not in self.stock_data:
            print(f"Error: Item '{item}' not found in inventory.")
            return

        if self.stock_data[item] < qty:
            print(f"Error: Not enough stock for '{item}'. "
                  f"Have {self.stock_data[item]}, need {qty}.")
            return

        # Only perform the action if all checks pass
        self.stock_data[item] -= qty
        log_entry = f"{datetime.now()}: Removed {qty} of {item}"
        self.logs.append(log_entry)
        print(log_entry)

        # Clean up item if stock is zero
        if self.stock_data[item] == 0:
            del self.stock_data[item]
            print(f"Info: '{item}' is now out of stock and has been removed.")

    def get_qty(self, item: str) -> int:
        """
        Gets the current quantity of a specific item.

        Args:
            item (str): The name of the item to query.

        Returns:
            int: The quantity of the item, or 0 if not found.
        """
        return self.stock_data.get(item, 0)

    def load_data(self, file: str = None):
        """
        Loads inventory data from a JSON file.
        Overwrites current in-memory stock_data.
        Args:
            file (str, optional): The file to load from.
                                  Uses default if None.
        """
        if file is None:
            file = self.default_file

        try:
            # Use 'with' for safe file handling and specify encoding
            with open(file, "r", encoding="utf-8") as f:
                self.stock_data = json.load(f)
            print(f"Data successfully loaded from {file}")
        except FileNotFoundError:
            print(f"Warning: File '{file}' not found. Starting with empty inventory.")
            self.stock_data = {}
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from '{file}'.")
            sys.exit(1)  # Exit if the data file is corrupt
        except IOError as e:
            print(f"Error loading file '{file}': {e}")
            sys.exit(1)

    def save_data(self, file: str = None):
        """
        Saves the current inventory data to a JSON file.

        Args:
            file (str, optional): The file to save to.
                                  Uses default if None.
        """
        if file is None:
            file = self.default_file

        try:
            # Use 'with' for safe file handling and specify encoding
            with open(file, "w", encoding="utf-8") as f:
                json.dump(self.stock_data, f, indent=4)
            print(f"Data successfully saved to {file}")
        except IOError as e:
            print(f"Error saving file '{file}': {e}")

    def print_data(self):
        """Prints a formatted report of all items and their quantities."""
        print("\n--- Items Report ---")
        if not self.stock_data:
            print("Inventory is empty.")
        else:
            for item, qty in self.stock_data.items():
                # Use f-string for modern string formatting
                print(f"{item} -> {qty}")
        print("--------------------")

    def check_low_items(self, threshold: int = 5) -> list:
        """
        Gets a list of items with stock below a given threshold.

        Args:
            threshold (int): The stock level to check against.

        Returns:
            list: A list of item names that are below the threshold.
        """
        return [item for item, qty in self.stock_data.items()
                if qty < threshold]


# The 'if __name__ == "__main__":' block ensures this code
# only runs when the script is executed directly, not when imported.
if __name__ == "__main__":

    # 1. Initialize the manager
    inventory = InventoryManager("inventory.json")

    # 2. (Optional) Load previous data if it exists
    inventory.load_data()
    inventory.print_data()

    # 3. Perform operations
    inventory.add_item("apple", 10)
    inventory.add_item("banana", 15)

    # 4. Handle invalid operations gracefully
    print("\n--- Testing Invalid Cases ---")
    inventory.add_item("apple", -5)       # Fails (negative quantity)
    inventory.add_item(123, 10)           # Fails (invalid item type)
    inventory.remove_item("orange", 1)    # Fails (item not found)
    inventory.remove_item("banana", 20)   # Fails (insufficient stock)
    print("-----------------------------\n")

    # 5. Perform valid removal
    inventory.remove_item("apple", 3)
    inventory.remove_item("banana", 15)  # This will remove the item completely

    # 6. Check stock
    print(f"Current apple stock: {inventory.get_qty('apple')}")
    print(f"Current banana stock: {inventory.get_qty('banana')}")

    # 7. Check for low items
    # 'apple' will be low (qty 7), but 'banana' is gone (qty 0)
    inventory.add_item("grape", 3)
    print(f"Low items (threshold 5): {inventory.check_low_items(5)}")

    # 8. Print final report and save
    inventory.print_data()
    inventory.save_data()

    # 9. Removed the dangerous 'eval' call
    print("\nScript finished safely.")
    