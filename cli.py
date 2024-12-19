import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Buyer, Item

DATABASE_URL = "sqlite:///buyers.db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    # Initialize Database
    Base.metadata.create_all(engine)
    print("Database Initialized")

def create_buyer():
    # Create new buyer
    name = input("Enter Buyer name: ")
    email = input("Enter Buyer email: ")
    buyer = Buyer(name=name, email=email)
    session.add(buyer)
    session.commit()
    print(f"Buyer '{name}' created with ID {buyer.id}")

def update_buyer():
    buyer_id = int(input("Enter Buyer ID to update: "))
    buyer = session.get(Buyer, buyer_id)
    if not buyer:
        print(f"Buyer with ID {buyer_id} does not exist.")
        return
    buyer.name = input(f"Enter new name for buyer (current: {buyer.name}): ") or buyer.name
    buyer.email = input(f"Enter new email for Buyer (current: {buyer.email}): ") or buyer.email
    session.commit()
    print(f"Buyer ID {buyer_id} updated successfully")

def delete_buyer():
    buyer_id = int(input("Enter Buyer ID to delete: "))
    buyer = session.get(Buyer, buyer_id)

    if not buyer:
        print(f"Buyer with ID {buyer_id} does not exist.")
        return
    session.delete(buyer)
    session.commit()
    print(f"Buyer ID {buyer_id} deleted successfully.")

def create_item():
    name = input("Enter item name: ")
    price = int(input("Enter item price: "))
    buyer_id = int(input("Enter Buyer ID: "))
    buyer = session.get(Buyer, buyer_id)
    if not buyer:
        print(f"Buyer with ID {buyer_id} does not exist")
        return
    item = Item(name=name, price=price, buyer_id=buyer_id)
    session.add(item)
    session.commit()
    print(f"Item '{name}' created with ID {item.id} and assigned to Buyer ID {buyer_id}")

def update_item():
    item_id = int(input("Enter Item ID to update: "))
    item = session.get(Item, item_id)

    if not item:
        print(f"Item with ID {item_id} does not exist")
        return
    item.name = input(f"Enter new name for item (current: {item.name}): ") or item.name
    item.price = input(f"Enter new price for item (current: {item.price}): ") or item.price
    new_buyer_id = input(f"Enter new Buyer ID for item (current: {item.buyer_id}): ") or item.buyer_id
    if new_buyer_id:
        new_buyer = session.get(Buyer, int(new_buyer_id))
        if not new_buyer:
            print(f"Buyer with ID {new_buyer_id} does not exist. Skipping Buyer update.")
        else:
            item.buyer_id = new_buyer_id
    session.commit()
    print(f"Item ID {item_id} updated successfully")

def delete_item():
    item_id = int(input("Enter Item ID to delete: "))
    item = session.get(Item, item_id)
    if not item:
        print(f"Item with ID {item_id} does not exist")
        return
    session.delete(item)
    session.commit()
    print(f"Item ID {item_id} deleted successfully")

def assign_item():
    item_id = int(input("Enter Item ID: "))
    buyer_id = int(input("Enter the new Buyer ID: "))
    item = session.get(Item, item_id)
    buyer = session.get(Buyer, buyer_id)

    if not item or not buyer:
        print("Invalid Item ID or Buyer ID.")
        return
    item.buyer_id = buyer_id
    session.commit()
    print("Item assigned to Buyer successfully")

def list_buyers():
    buyers = session.query(Buyer).all()
    if not buyers:
        print("No Buyers found.")
    for buyer in buyers:
        print(buyer)

def list_items():
    items = session.query(Item).all()
    if not items:
        print("No Items found.")
    for item in items:
        print(item)

def view_items_by_buyer():
    buyer_id = int(input("Enter Buyer ID to view items: "))
    buyer = session.get(Buyer, buyer_id)
    if not buyer:
        print(f"Buyer with ID {buyer_id} does not exist")
        return
    items = buyer.items
    if not items:
        print(f"No items found for Buyer with ID {buyer_id}")
        return
    print(f"Items belonging to Buyer '{buyer.name}' (ID {buyer_id}):")
    for item in items:
        print(item)

def main_menu():
    print("\nWelcome to the Application. What would you like to do?")
    print("1. Create Buyer")
    print("2. Update Buyer")
    print("3. Delete Buyer")
    print("4. Create Item")
    print("5. Update Item")
    print("6. Delete Item")
    print("7. Assign Item to Buyer")
    print("8. List Buyers")
    print("9. List Items")
    print("10. View Items by Buyer")
    print("11. Exit")
    while True:
      
        choice = input("Enter your choice: ")

        if choice == "1":
            create_buyer()
        elif choice == "2":
            update_buyer()
        elif choice == "3":
            delete_buyer()
        elif choice == "4":
            create_item()
        elif choice == "5":
            update_item()
        elif choice == "6":
            delete_item()
        elif choice == "7":
            assign_item()
        elif choice == "8":
            list_buyers()
        elif choice == "9":
            list_items()
        elif choice == "10":
            view_items_by_buyer()
        elif choice == "11":
            print("Exiting.......")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    init_db()
    main_menu()
