"""Extension++: menu-driven cinema with a running sales summary."""


def calculate_discount(price, is_member):
    """Return 10%  of price for members, otherwise zero."""
    return price * 0.10 if is_member else 0.0 # returns a float


def get_age():
    while True: # although while true runs infinitely, return breaks the loop
        try:
            age = int(input("Age: ")) # input string converted into integer
            if age >= 0: return age # return age breaks the loop
        except ValueError:
            pass
        print("Please enter a non-negative whole-number age.")


def get_price():
    while True:
        try:
            price = float(input("Ticket price (£): ")) # input string converted to float
            if 0 <= price < float("inf"):
                return price # breaks loop
        except ValueError:
            pass
        print("Please enter a valid, non-negative price.")


def get_membership():
    while True:
        answer = input("Member? (yes/no): ").strip().lower() # input string
        if answer in ("yes", "no"):
            return answer == "yes" # breaks loop
        print("Please answer yes or no.")


def add_customer(receipts):
    print("\n------ ADD CUSTOMER ------")
    name = input("Customer name: ").strip() # input string
    age = get_age()
    price = get_price()
    is_member = get_membership()
    discount = calculate_discount(price, is_member)
    final_price = price - discount
    
    receipts.append({
        "name": name,
        "age": age,
        "price": price,
        "is_member": is_member,
        "discount": discount,
        "final_price": final_price
    })
    print("\n------ CINEMA RECEIPT ------")
    print(f"Customer: {name} | Age: {age} | Member: {is_member}")
    print(f"Original ticket price: £{price:.2f}")
    print(f"Member discount: £{discount:.2f}")
    print(f"Amount paid: £{final_price:.2f}")


def view_summary(receipts):
    print("\n------ BOOKING SUMMARY ------")
    if not receipts:
        print("No customers have been added yet.")
        return # cancels function before doing anything below if receipts is empty
    
    total_sales = sum(receipt["final_price"] for receipt in receipts)
    average_price = total_sales / len(receipts) # Average amount paid per ticket
    number_of_members = sum(receipt["is_member"] for receipt in receipts)
    oldest_customer = max(receipts, key=lambda receipt: receipt["age"])

    print(f"Tickets sold: {len(receipts)}")
    print(f"Total sales: £{total_sales:.2f}")
    print(f"Average ticket price paid: £{average_price:.2f}")
    print(f"Number of members: {number_of_members}")
    print(f"Oldest customer: {oldest_customer['name']} ({oldest_customer['age']})")


def main():
    receipts = [] # even though receipts is defined very late, main()  is always running until the program stops, so it still works
    while True:
        print("\n========== PYTHON CINEMA ==========")
        print("1. Add customer")
        print("2. View summary")
        print("3. Exit")
        choice = input("Choose 1, 2 or 3: ").strip() # input string, which is why the numbers in the next few lines are quoted

        if choice == "1": # choice is a string which is why this is quoted
            add_customer(receipts)
        elif choice == "2": # same here
            view_summary(receipts)
        elif choice == "3": # and here
            print("Goodbye! Thank you for using Python Cinema.")
            return receipts # break here cancels the main() function, ending the script. I think return also works
        else:
            print("Invalid option. please enter 1, 2 or 3.")

if __name__ == "__main__":
    main() # perfect 100 lines of code lol
