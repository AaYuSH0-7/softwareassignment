# Global counter used to assign unique IDs to each requisition.
# KISS principle: A simple integer counter keeps things straightforward.
counter = 1000

class RequisitionSystem:
    def __init__(self):
        # Initializes with empty requisitions and counters
        # SRP (Single Responsibility Principle): Constructor only initializes values.
        self.requisitions = []
        self.approved = 0
        self.pending = 0
        self.not_approved = 0

    def staff_info(self):
        # SRP: This method focuses only on gathering staff information.
        date = input("Enter the date (DD/MM/YYYY): ")
        staff_id = input("Enter the Staff ID: ")
        name = input("Enter the Staff Name: ")
        return date, staff_id, name

    def requisitions_details(self):
        # DRY: The method prevents repetitive input logic.
        items = []
        total = 0
        while True:
            item = input("Enter item (or 'done'): ")
            if item.lower() == 'done':
                break
            try:
                price = float(input("Enter price: "))
                items.append((item, price))
                total += price
            except ValueError:
                print("Invalid price. Try again.")
        return items, total

    def requisition_approval(self, total):
        # KISS: A simple rule to determine status based on total price.
        return "Approved" if total < 500 else "Pending"

    def create_requisition(self):
        global counter
        date, staff_id, name = self.staff_info()
        items, total = self.requisitions_details()
        status = self.requisition_approval(total)

        # OCP (Open/Closed Principle): The logic is open for extension but closed for modification. 
        # We could add new approval rules without changing this method.
        if status == "Approved":
            ref = staff_id + str(counter)
            self.approved += 1
        else:
            ref = "N/A"
            self.pending += 1

        self.requisitions.append({
            'id': counter,
            'date': date,
            'staff_id': staff_id,
            'name': name,
            'items': items,
            'total': total,
            'status': status,
            'ref': ref
        })
        counter += 1

    def respond_requisition(self):
        for requisition in self.requisitions:
            if requisition['status'] == "Pending":
                print(f"Requisition {requisition['id']} for {requisition['name']} is pending.")
                choice = input("Approve or Not approved? ")
                # KISS: Simple condition blocks, easy to follow.
                if choice.lower() == 'approve':
                    requisition['status'] = "Approved"
                    requisition['ref'] = requisition['staff_id'] + str(requisition['id'])
                    self.approved += 1
                    self.pending -= 1
                elif choice.lower() == 'not approved':
                    requisition['status'] = "Not approved"
                    requisition['ref'] = "N/A"
                    self.not_approved += 1
                    self.pending -= 1

    def display_requisitions(self):
        # DRY: Centralized logic for displaying requisition details.
        for requisition in self.requisitions:
            print("\nRequisition Details")
            print(f"Date: {requisition['date']}")
            print(f"Staff ID: {requisition['staff_id']}")
            print(f"Staff Name: {requisition['name']}")
            print(f"Requisition ID: {requisition['id']}")
            print(f"Total: ${requisition['total']:.2f}")
            print(f"Status: {requisition['status']}")
            print(f"Approval Reference: {requisition['ref']}")

    def requisition_statistics(self):
        # DRY: Centralized logic for displaying statistics.
        print("\nStatistics")
        print(f"Total Requisitions: {len(self.requisitions)}")
        print(f"Approved: {self.approved}")
        print(f"Pending: {self.pending}")
        print(f"Not Approved: {self.not_approved}")


# MAIN PROGRAM
# KISS: Menu structure is simple and understandable.
rs = RequisitionSystem()
while True:
    print("\n1. Submit Requisition\n2. Display Requisitions\n3. Respond to Pending\n4. Show Statistics\n5. Exit")
    choice = input("Choose an option: ")

    if choice == '1':
        rs.create_requisition()
    elif choice == '2':
        rs.display_requisitions()
    elif choice == '3':
        rs.respond_requisition()
    elif choice == '4':
        rs.requisition_statistics()
    elif choice == '5':
        print("Exiting Requisition System.")
        break
    else:
        print("Invalid choice. Please try again.")
