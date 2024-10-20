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

    def save_reservations(self):
        """Save current reservations to the CSV file."""
        try:
            with open(CSV_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                for reservation in self.queue:
                    writer.writerow([reservation.name, reservation.party_size, reservation.reservation_time])
            print("Reservations saved successfully.")
        except Exception as e:
            print(f"Error saving reservations: {e}")

    def view_reservations(self):
        """Display all current reservations sorted by reservation time."""
        if not self.queue:
            print("No reservations available.")
        else:
            # Sort reservations by datetime before displaying
            self.sorted_queue = sorted(self.queue, key=lambda res: datetime.strptime(res.reservation_time, '%m-%d-%Y %H:%M'))
            for idx, reservation in enumerate(self.sorted_queue, start=1):
                print(f"{idx}. {reservation}")

    def add_reservation(self, name, party_size, reservation_time):
        """Add a reservation to the queue."""
        try:
            party_size = int(party_size)
            if party_size <= 0:
                raise ValueError("Party size must be a positive number.")
            self.queue.append(Reservation(name, party_size, reservation_time))
            print(f"Reservation added for {name} (Party Size: {party_size}) at {reservation_time}.")
            self.save_reservations()  # Save immediately after adding
        except ValueError as e:
            print(f"Error: {e}")

    def cancel_reservation(self, index):
        """Cancel a reservation based on its index in the sorted list."""
        try:
            # Adjust the index to 0-based for sorted list usage
            reservation = self.sorted_queue[index - 1]  
            print(f"Canceled reservation for {reservation.name} (Party Size: {reservation.party_size}) at {reservation.reservation_time}.")
            # Remove the reservation from both the sorted queue and the original queue
            self.queue.remove(reservation)
            self.save_reservations()  # Save after canceling
        except IndexError:
            print("Invalid reservation index.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def update_reservation(self, index):
        """Update an existing reservation based on its index in the sorted list."""
        try:
            # Access the reservation from the sorted list
            reservation = self.sorted_queue[index - 1]  # Adjusting index to 0-based
            print(f"Updating reservation for {reservation.name}")

            # Get new details with validation
            name = input(f"Enter new name (or press Enter to keep '{reservation.name}'): ") or reservation.name

            # Loop to validate party size
            while True:
                party_size_input = input(f"Enter new party size (or press Enter to keep '{reservation.party_size}'): ") or reservation.party_size
                try:
                    party_size = int(party_size_input)
                    if party_size <= 0:
                        raise ValueError("Party size must be a positive number.")
                    break  # Exit loop if valid
                except ValueError:
                    print("Invalid input. Please enter a valid positive number for party size.")

            # Loop to validate reservation time
            while True:
                reservation_time_input = input(f"Enter new reservation time (MM-DD-YYYY HH:MM) (or press Enter to keep '{reservation.reservation_time}'): ") or reservation.reservation_time
                try:
                    # Validate the reservation time
                    datetime.strptime(reservation_time_input, '%m-%d-%Y %H:%M')
                    break  # Exit loop if valid
                except ValueError:
                    print("Error: Invalid date/time format. Use MM-DD-YYYY HH:MM.")

            # Update the reservation in the sorted list
            updated_reservation = Reservation(name, party_size, reservation_time_input)

            # Find the reservation in the original queue and update it there as well
            original_index = self.queue.index(reservation)
            self.queue[original_index] = updated_reservation

            print(f"Reservation updated for {name} (Party Size: {party_size}) at {reservation_time_input}.")

            # Sort the queue by reservation time after updating
            self.queue.sort(key=lambda res: datetime.strptime(res.reservation_time, '%m-%d-%Y %H:%M'))
            self.save_reservations()  # Save immediately after updating
        except IndexError:
            print("Invalid reservation index.")

    def exit_program(self):
        """Save reservations to CSV and exit the program."""
        self.save_reservations()  # Ensure all changes are saved
        print("Exiting program.")
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
            
            # Loop to validate party size
            while True:
                party_size = input("Enter party size (numbers only): ")
                try:
                    party_size = int(party_size)
                    if party_size <= 0:
                        raise ValueError("Party size must be a positive number.")
                    break  # Exit loop if valid
                except ValueError:
                    print("Invalid input. Please enter a valid positive number for party size.")

            # Loop to validate reservation time
            while True:
                reservation_time = input("Enter reservation time (MM-DD-YYYY HH:MM): ")
                try:
                    datetime.strptime(reservation_time, '%m-%d-%Y %H:%M')
                    break  # Exit loop if valid
                except ValueError:
                    print("Error: Invalid date/time format. Use MM-DD-YYYY HH:MM.")

            queue.add_reservation(name, party_size, reservation_time)
        elif choice == '2':
            queue.view_reservations()
        elif choice == '3':
            queue.view_reservations()  # Show reservations before canceling
            while True:
                try:
                    index = int(input("Enter the reservation number to cancel: "))
                    queue.cancel_reservation(index)
                    break  # Exit loop if valid input
                except ValueError:
                    print("Invalid input. Please enter a valid reservation number.")
        elif choice == '4':
            queue.view_reservations()  # Show reservations before updating
            while True:
                try:
                    index = int(input("Enter the reservation number to update: "))
                    queue.update_reservation(index)
                    break  # Exit loop if valid input
                except ValueError:
                    print("Invalid input. Please enter a valid reservation number.")
        elif choice == '5':
            queue.exit_program()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
