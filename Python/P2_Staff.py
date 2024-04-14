import psycopg2
from psycopg2 import sql
from datetime import datetime

# Connect to the database
def connect():
	try:
		connection = psycopg2.connect(
			dbname="P2",
			user="postgres",
			password="p",
			host="localhost",
			port="5432"
		)
		return connection
	except psycopg2.Error as err:
		print("Unable to connect to the database")
		print(err)
		return None


def room_booking_management(connection):
	while True:
		print("\nRoom Booking Management")
		print("1. View Room Bookings")
		print("2. Cancel Room Booking")
		print("Q. Quit")

		choice = input("Please select your option: ")

		if choice == '1':
			print("")
			view_room_bookings(connection)
		elif choice == '2':
			print("")
			cancel_room_booking(connection)
		elif choice.upper() == 'Q':
			print("")
			break
		else:
			print("Incorrect input. Please select again.")


def view_room_bookings(connection):
	try:
		cursor = connection.cursor()

		# Query to fetch all room bookings
		select_query = """
		SELECT * FROM BookedRoom
		"""
		cursor.execute(select_query)
		room_bookings = cursor.fetchall()

		if room_bookings:
			print("\nRoom Bookings:")
			for booking in room_bookings:
				print(f"Room ID: {booking[0]}, Date: {booking[1]}, Start Time: {booking[2]}, End Time: {booking[3]}")
		else:
			print("No room bookings found.")

	except psycopg2.Error as err:
		print("Error viewing room bookings")
		print(err)

	finally:
		if cursor:
			cursor.close()


def cancel_room_booking(connection):
	try:
		cursor = connection.cursor()

		# Fetching booked rooms to display
		select_booked_rooms_query = """
		SELECT roomID, date, startTime, endTime
		FROM BookedRoom
		"""
		cursor.execute(select_booked_rooms_query)
		booked_rooms = cursor.fetchall()

		if booked_rooms:
			print("\nBooked Rooms:")
			for room in booked_rooms:
				print(f"Room ID: {room[0]}, Date: {room[1]}, Start Time: {room[2]}, End Time: {room[3]}")
		else:
			print("No rooms are currently booked.")

		room_id = input("\nEnter Room ID to cancel booking: ")
		date = input("Enter Date (YYYY-MM-DD) to cancel booking: ")
		start_time = input("Enter Start Time (HH:MM) to cancel booking: ")

		# Fetching the session ID associated with the room booking
		select_session_query = """
		SELECT sessionID FROM TrainingSession
		WHERE roomID = %s AND date = %s AND startTime = %s
		"""
		cursor.execute(select_session_query, (room_id, date, start_time))
		session_id = cursor.fetchone()

		if session_id:
			session_id = session_id[0]
			# Deleting member sessions associated with the session ID
			delete_member_session_query = """
			DELETE FROM MemberSession
			WHERE sessionID = %s
			"""
			cursor.execute(delete_member_session_query, (session_id,))
			
			# Deleting the session from TrainingSession table
			delete_session_query = """
			DELETE FROM TrainingSession
			WHERE sessionID = %s
			"""
			cursor.execute(delete_session_query, (session_id,))
			connection.commit()

			print("\nRoom booking and associated class canceled successfully!")
		else:
			print("\nNo class associated with this room booking.")

		# Deleting room booking based on Room ID, Date, and Start Time
		delete_query = """
		DELETE FROM BookedRoom
		WHERE roomID = %s AND date = %s AND startTime = %s
		"""
		cursor.execute(delete_query, (room_id, date, start_time))
		connection.commit()

		print("Room booking canceled successfully!")

	except psycopg2.Error as err:
		print("Error canceling room booking")
		print(err)

	finally:
		if cursor:
			cursor.close()



def add_class_schedule(connection):
	try:
		cursor = connection.cursor()

		print("\nAdding Class Schedule")

		# Prompt user for input
		room_id = input("Enter room ID: ")
		session_type = input("Enter session type: ")
		date = input("Enter date (YYYY-MM-DD): ")
		start_time = input("Enter start time (HH:MM): ")
		end_time = input("Enter end time (HH:MM): ")
		trainer_id = input("Enter trainer ID: ")

		# Insert the new class schedule into the database
		insert_query = """
		INSERT INTO TrainingSession (roomID, sessionType, date, startTime, endTime, trainerID)
		VALUES (%s, %s, %s, %s, %s, %s)
		"""
		cursor.execute(insert_query, (room_id, session_type, date, start_time, end_time, trainer_id))
		connection.commit()

		print("")
		print("Class schedule added successfully!")
		print("")

	except psycopg2.Error as e:
		print("Error adding class schedule:", e)

	finally:
		if cursor:
			cursor.close()


def update_class_schedule(connection):
	try:
		cursor = connection.cursor()

		print("\nUpdating Class Schedule")

		# Prompt user for input
		session_id = input("Enter session ID to update: ")
		room_id = input("Enter new room ID (press Enter to keep current): ")
		session_type = input("Enter new session type (press Enter to keep current): ")
		date = input("Enter new date (YYYY-MM-DD) (press Enter to keep current): ")
		start_time = input("Enter new start time (HH:MM) (press Enter to keep current): ")
		end_time = input("Enter new end time (HH:MM) (press Enter to keep current): ")
		trainer_id = input("Enter new trainer ID (press Enter to keep current): ")

		# Check for conflicts with existing sessions
		if date and start_time and end_time:
			# Construct SQL query to check for conflicts
			conflict_query = """
			SELECT sessionID
			FROM TrainingSession
			WHERE roomID = %s
				AND date = %s
				AND ((startTime <= %s AND endTime > %s)
					OR (startTime < %s AND endTime >= %s)
					OR (startTime >= %s AND endTime <= %s))
				AND sessionID != %s
			"""
			cursor.execute(conflict_query, (room_id, date, start_time, start_time, end_time, end_time, start_time, end_time, session_id))
			conflicting_sessions = cursor.fetchall()

			if conflicting_sessions:
				print("Error: Schedule conflicts with existing sessions.")
				return

		# Construct the SQL UPDATE query
		update_query = """
		UPDATE TrainingSession
		SET roomID = COALESCE(%s, roomID),
			sessionType = COALESCE(%s, sessionType),
			date = COALESCE(%s, date),
			startTime = COALESCE(%s, startTime),
			endTime = COALESCE(%s, endTime),
			trainerID = COALESCE(%s, trainerID)
		WHERE sessionID = %s
		"""
		cursor.execute(update_query, (room_id, session_type, date, start_time, end_time, trainer_id, session_id))
		connection.commit()

		print("")
		print("Class schedule updated successfully!")
		print("")

	except psycopg2.Error as e:
		print("Error updating class schedule:", e)

	finally:
		if cursor:
			cursor.close()


def delete_class_schedule(connection):
	try:
		cursor = connection.cursor()

		print("\nDeleting Class Schedule")

		# Prompt user for input
		session_id = input("Enter session ID to delete: ")

		# Check if the session exists
		select_query = "SELECT * FROM TrainingSession WHERE sessionID = %s"
		cursor.execute(select_query, (session_id,))
		session = cursor.fetchone()

		if not session:
			print("Error: Session ID not found.")
			return

		# Delete member entries for the session
		delete_member_session_query = "DELETE FROM MemberSession WHERE sessionID = %s"
		cursor.execute(delete_member_session_query, (session_id,))

		# Delete the session
		delete_query = "DELETE FROM TrainingSession WHERE sessionID = %s"
		cursor.execute(delete_query, (session_id,))
		connection.commit()
		
		print("")
		print("Class schedule deleted successfully!")
		print("")

	except psycopg2.Error as e:
		print("Error deleting class schedule:", e)

	finally:
		if cursor:
			cursor.close()


# Equipment Maintenance Monitoring function
def equipment_maintenance_monitoring(connection):
	try:
		cursor = connection.cursor()

		print("Equipment Maintenance Monitoring")
		print("1. Add New Equipment")
		print("2. Report Issue with Equipment")
		print("Q. Quit")

		while True:
			choice = input("Please select your option: ")

			if choice == '1':
				description = input("Enter description of the new equipment: ")
				room_id = input("Enter Room ID where the equipment is located: ")

				# Inserting new equipment into Equipment table
				insert_query = """
				INSERT INTO Equipment (description, status, roomID)
				VALUES (%s, 'Functional', %s)
				"""
				cursor.execute(insert_query, (description, room_id))
				connection.commit()

				print("New equipment added successfully!")
				print("")

			elif choice == '2':
				equip_id = input("Enter Equipment ID to report issue: ")
				status = input("Enter status (BROKEN, UNDER MAINTENANCE, FUNCTIONAL): ")
				status = status.upper()

				if status not in ["BROKEN", "UNDER MAINTENANCE", "FUNCTIONAL"]:
					print("")
					print("Invalid status. Please enter one of the following: BROKEN, UNDER MAINTENANCE, FUNCTIONAL")
					print("")
					continue

				# Updating equipment status
				update_query = """
				UPDATE Equipment
				SET status = %s
				WHERE equipID = %s
				"""
				cursor.execute(update_query, (status, equip_id))
				connection.commit()
				print("")
				print("Issue reported successfully!")
				print("")
			elif choice.upper() == 'Q':
				break
			else:
				print("Invalid input. Please select again.")

	except psycopg2.Error as err:
		print("Error in equipment maintenance monitoring")
		print(err)

	finally:
		if cursor:
			cursor.close()


# Class Schedule Updating function
def class_schedule_updating(connection):
	try:
		cursor = connection.cursor()

		print("\nClass Schedule Updating")
		print("1. Add Class Schedule")
		print("2. Update Class Schedule")
		print("3. Delete Class Schedule")
		print("Q. Quit")

		while True:
			choice = input("Please select your option: ")

			if choice == '1':  # Add Class Schedule
				print("")
				add_class_schedule(connection)
			elif choice == '2':	 # Update Class Schedule
				print("")
				update_class_schedule(connection)
			elif choice == '3':	 # Delete Class Schedule
				print("")
				delete_class_schedule(connection)
			elif choice.upper() == 'Q':
				break
			else:
				print("Invalid choice. Please try again.")

	except psycopg2.Error as err:
		print("Error in class schedule updating")
		print(err)

	finally:
		if cursor:
			cursor.close()


# Billing and Payment Processing function
def generate_bill(connection):
	try:
		cursor = connection.cursor()

		print("Generating Bill")

		# Prompt user for input
		member_id = input("Enter member ID: ")

		# Check if the member exists
		select_member_query = "SELECT * FROM Members WHERE memberID = %s"
		cursor.execute(select_member_query, (member_id,))
		member = cursor.fetchone()

		if not member:
			print("Error: Member ID not found.")
			return

		# Prompt user for bill amount
		amount_due = float(input("Enter amount due: "))

		# Prompt user for transaction type
		while True:
			transaction_type = input("Enter transaction type (Membership Fee / Single Session): ").strip().upper()
			if transaction_type in ["MEMBERSHIP FEE", "SINGLE SESSION"]:
				break
			else:
				print("Invalid transaction type. Please enter either 'Membership Fee' or 'Single Session'.")

		# Get current date and time
		current_datetime = datetime.now()

		# Insert bill into BillingAndPayments table
		insert_bill_query = """
		INSERT INTO BillingAndPayments (amount, dateNtime, transacType, memberID)
		VALUES (%s, %s, %s, %s)
		"""
		cursor.execute(insert_bill_query, (amount_due, current_datetime, transaction_type, member_id))
		connection.commit()

		print("Bill generated successfully!")
		print("")

	except psycopg2.Error as e:
		print("Error generating bill:", e)

	finally:
		if cursor:
			cursor.close()



# Staff menu
def main_menu(connection):
	try:
		cursor = connection.cursor()

		print("Welcome to the Health and Fitness Club Management System!")
		print("1. Room Booking Management")
		print("2. Equipment Maintenance Monitoring")
		print("3. Class Schedule Updating")
		print("4. Billing and Payment Processing")
		print("Q. Quit")

		while True:
			choice = input("Please select your option: ")

			if choice == '1':
				print("")
				room_booking_management(connection)
			elif choice == '2':
				print("")
				equipment_maintenance_monitoring(connection)
			elif choice == '3':
				print("")
				class_schedule_updating(connection)
			elif choice == '4':
				print("")
				generate_bill(connection)
			elif choice.upper() == 'Q':
				print("")
				print("Goodbye!")
				break
			else:
				print("Incorrect input. Please select again.")

	except psycopg2.Error as err:
		print("Error in main menu")
		print(err)

	finally:
		if cursor:
			cursor.close()


# Example usage:
if __name__ == "__main__":
	connection = connect()
	if connection:
		main_menu(connection)