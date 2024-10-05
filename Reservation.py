import csv
import os
from datetime import datetime

# Constants for CSV file path
CSV_FILE = 'reservations.csv'

class Reservation:
    def __init__(self, name, party_size, reservation_time):
        self.name = name
        self.party_size = party_size
        self.reservation_time = reservation_time

    def __str__(self):
        return f"{self.name}, Party Size: {self.party_size}, Time: {self.reservation_time}"

class ReservationQueue:
    def __init__(self):
        self.queue = []
        self.load_reservations()

    def load_reservations(self):
        """Load reservations from the CSV file into the queue."""
        if os.path.exists(CSV_FILE):
            try:
                with open(CSV_FILE, mode='r', newline='') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) == 3:
                            name, party_size, reservation_time = row
                            self.queue.append(Reservation(name, party_size, reservation_time))
            except Exception as e:
                print(f"Error loading reservations: {e}")
        else:
            print(f"{CSV_FILE} not found, starting with an empty queue.")

    def view_reservations(self):
        """Display all current reservations sorted by reservation time."""
        if not self.queue:
            print("No reservations available.")
        else:
            # Sort reservations by datetime before displaying
            sorted_queue = sorted(self.queue, key=lambda res: datetime.strptime(res.reservation_time, '%m-%d-%Y %H:%M'))
            
            for idx, reservation in enumerate(sorted_queue, start=1):
                print(f"{idx}. {reservation}")


    def add_reservation(self, name, party_size, reservation_time):
        """Add a reservation to the queue."""
        try:
            party_size = int(party_size)  # Validate party size as an integer
            self.queue.append(Reservation(name, party_size, reservation_time))
            print(f"Reservation added for {name} (Party Size: {party_size}) at {reservation_time}.")
            self.save_reservations()  # Save immediately after adding
        except ValueError:
            print("Error: Party size must be a number.")

    def view_reservations(self):
        """Display all current reservations sorted by reservation time."""
        if not self.queue:
            print("No reservations available.")
        else:
            # Sort reservations by datetime before displaying
            sorted_queue = sorted(self.queue, key=lambda res: datetime.strptime(res.reservation_time, '%m-%d-%Y %H:%M'))
            
            for idx, reservation in enumerate(sorted_queue, start=1):
                print(f"{idx}. {reservation}")

    def cancel_reservation(self):
        """Cancel the first reservation in the queue (FIFO)."""
        if not self.queue:
            print("No reservations to cancel.")
        else:
            canceled = self.queue.pop(0)
            print(f"Canceled reservation for {canceled.name} (Party Size: {canceled.party_size}) at {canceled.reservation_time}.")
            self.save_reservations()  # Save after canceling

    def update_reservation(self, index):
        """Update an existing reservation based on index."""
        if 0 <= index < len(self.queue):
            reservation = self.queue[index]
            print(f"Updating reservation for {reservation.name}")
            
            # Get new details
            name = input(f"Enter new name (or press Enter to keep '{reservation.name}'): ") or reservation.name
            party_size = input(f"Enter new party size (or press Enter to keep '{reservation.party_size}'): ") or reservation.party_size
            reservation_time = input(f"Enter new reservation time (MM-DD-YYYY HH:MM) (or press Enter to keep '{reservation.reservation_time}'): ") or reservation.reservation_time
            
            try:
                party_size = int(party_size)  # Validate party size as an integer
                # Validate date/time format
                datetime.strptime(reservation_time, '%m-%d-%Y %H:%M')
                self.queue[index] = Reservation(name, party_size, reservation_time)
                print(f"Reservation updated for {name} (Party Size: {party_size}) at {reservation_time}.")
                self.save_reservations()  # Save immediately after updating
            except ValueError as e:
                print(f"Error: {e}")
        else:
            print("Invalid reservation index.")

    def exit_program(self):
        """Save reservations to CSV and exit the program."""
        print("Reservations saved. Exiting program.")
        exit()

def main():
    queue = ReservationQueue()

    while True:
        print("\n--- Restaurant Reservation System ---")
        print("1. Add Reservation")
        print("2. View Reservations")
        print("3. Cancel Reservation")
        print("4. Update Reservation")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter customer name: ")
            party_size = input("Enter party size: ")
            reservation_time = input("Enter reservation time (MM-DD-YYYY HH:MM): ")
            try:
                # Validate the reservation time
                datetime.strptime(reservation_time, '%m-%d-%Y %H:%M')
                queue.add_reservation(name, party_size, reservation_time)
            except ValueError:
                print("Error: Invalid date/time format. Use MM-DD-YYYY HH:MM.")
        elif choice == '2':
            queue.view_reservations()
        elif choice == '3':
            queue.cancel_reservation()
        elif choice == '4':
            queue.view_reservations()
            if queue.queue:
                try:
                    index = int(input("Enter the reservation number to update: ")) - 1
                    queue.update_reservation(index)
                except ValueError:
                    print("Error: Please enter a valid number.")
            else:
                print("No reservations to update.")
        elif choice == '5':
            queue.exit_program()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
