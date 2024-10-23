# Basic Restaurant Reservation System with CSV File Handling

This is a command-line application designed to manage restaurant reservations efficiently using a First-In-First-Out (FIFO) queue system. It allows restaurant staff to add, view, update, and cancel reservations while ensuring that all data is persistently stored in a CSV file. The system processes reservations by maintaining customer details, party size, and reservation time. It loads reservations from a CSV file on startup and saves updates automatically, ensuring data integrity across sessions.

## Features

- **Add Reservations**: Staff can add a customer's reservation, including name, party size, and reservation time.
- **View Reservations**: Displays all reservations, sorted by reservation time for easy management.
- **Update Reservations**: Modify customer details, party size, or reservation time.
- **Cancel Reservations**: Remove reservations by selecting the reservation index.
- **Persistent Storage**: Automatically saves changes to a CSV file and reloads them when the program restarts.

## How It Works

1. **Add a Reservation**: When a new reservation is added, it's appended to the queue, and the CSV file is immediately updated.
2. **View Reservations**: Lists all reservations in the system, sorted by time, showing the name, party size, and time.
3. **Update a Reservation**: Allows staff to change details for any reservation in the system.
4. **Cancel a Reservation**: Removes a reservation from the queue and updates the CSV file.
5. **Exit**: Saves all current data and safely exits the program.
