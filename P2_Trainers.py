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


def check_trainer(trainer_id, connection):
	try:
		cursor = connection.cursor()

		# Query to check if the provided ID belongs to a trainer
		select_query = """
		SELECT COUNT(*) FROM Staff
		WHERE staffID = %s AND role = 'Trainer'
		"""
		cursor.execute(select_query, (trainer_id,))
		count = cursor.fetchone()[0]

		return count == 1

	except psycopg2.Error as err:
		print("Error checking trainer ID")
		print(err)

	finally:
		if cursor:
			cursor.close()


# Trainer Profile View function
def trainer_view(trainer_id, connection):
	try:
		cursor = connection.cursor()

		print("Trainer Profile View")

		# Ask for member's first name and last name
		first_name = input("Enter member's first name: ").upper()
		last_name = input("Enter member's last name: ").upper()

		# Fetch member details
		select_query = """
		SELECT * FROM Members
		WHERE firstName = %s AND lastName = %s
		"""
		cursor.execute(select_query, (first_name, last_name))
		member_details = cursor.fetchone()

		if member_details:
			print("Member Details:")
			print(f"Member ID: {member_details[0]}")
			print(f"First Name: {member_details[1]}")
			print(f"Last Name: {member_details[2]}")
			print(f"Email: {member_details[3]}")
			print(f"Address: {member_details[4]}")
			print(f"Phone Number: {member_details[5]}")
			print(f"Credit Card: {member_details[6]}")

			# Fetch personal information
			select_personal_query = """
			SELECT * FROM PersonalInfo
			WHERE memberID = %s
			"""
			cursor.execute(select_personal_query, (member_details[0],))
			personal_info = cursor.fetchone()

			print("\nPersonal Information:")
			print(f"Fitness Goal: {personal_info[1]}")
			print(f"Initial Weight: {personal_info[2]} kg")
			print(f"Current Weight: {personal_info[3]} kg")
			print(f"Initial VO2Max: {personal_info[4]}")
			print(f"Current VO2Max: {personal_info[5]}")
			print(f"Initial BMI: {personal_info[6]}")
			print(f"Current BMI: {personal_info[7]}")

			# Fetch exercises
			select_exercise_query = """
			SELECT name, description
			FROM Exercise
			WHERE memberID = %s
			"""
			cursor.execute(select_exercise_query, (member_details[0],))
			exercises = cursor.fetchall()

			print("\nExercise Routines:")
			for exercise in exercises:
				print(f"Name: {exercise[0]}")
				print(f"Description: {exercise[1]}")
				print()

		else:
			print("Member not found.")

	except psycopg2.Error as err:
		print("Error viewing member profile")
		print(err)

	finally:
		if cursor:
			cursor.close()


def trainer_schedule(trainer_id, connection):
	try:
		cursor = connection.cursor()

		print("Schedule Management")
		print("1. Schedule Personal Training Session")
		print("2. Schedule Group Fitness Class")
		print("Q. Quit")

		choice = input("Please select your option: ")

		if choice == '1':
			# Personal Training Session
			date = input("Enter date (YYYY-MM-DD): ")
			start_time = input("Enter start time (HH:MM): ")
			end_time = input("Enter end time (HH:MM): ")

			# Check if the room is one of the private rooms
			select_query = """
			SELECT roomID
			FROM Room
			WHERE roomType LIKE 'Private Room%' AND availability = true
			"""
			cursor.execute(select_query)
			private_rooms = cursor.fetchall()

			if private_rooms:
				available_private_rooms = []
				for room_id in private_rooms:
					# Check if the room is available during the specified date and time
					check_query = """
					SELECT COUNT(*)
					FROM TrainingSession
					WHERE roomID = %s AND date = %s AND (
						(startTime <= %s AND endTime >= %s) OR 
						(startTime <= %s AND endTime >= %s) OR
						(startTime >= %s AND endTime <= %s)
					)
					"""
					cursor.execute(check_query, (room_id[0], date, start_time, start_time, end_time, end_time, start_time, end_time))
					count = cursor.fetchone()[0]

					# If count is 0, the room is available
					if count == 0:
						available_private_rooms.append(room_id[0])

				if available_private_rooms:
					print("Available Private Training Rooms:")
					for i, room_id in enumerate(available_private_rooms, 1):
						print(f"{i}. Room {room_id}")

					room_choice = int(input("Select the room for the training session: "))
					if 1 <= room_choice <= len(available_private_rooms):
						room_id = available_private_rooms[room_choice - 1]
						session_type = "Personal Training Session"

						# Insert into TrainingSession table
						insert_query = """
						INSERT INTO TrainingSession (roomID, sessionType, date, startTime, endTime, trainerID)
						VALUES (%s, %s, %s, %s, %s, %s)
						RETURNING sessionID
						"""
						cursor.execute(insert_query, (room_id, session_type, date, start_time, end_time, trainer_id))
						session_id = cursor.fetchone()[0]

						connection.commit()
						print("Personal Training Session scheduled successfully!")
					else:
						print("Invalid room choice.")
				else:
					print("No available private rooms for the selected date and time.")
			else:
				print("No private rooms available.")


		elif choice == '2':
			# Group Fitness Class
			date = input("Enter date (YYYY-MM-DD): ")
			start_time = input("Enter start time (HH:MM): ")
			end_time = input("Enter end time (HH:MM): ")

			# Check if suitable rooms (only Cardio Room or Gym Room) are available for group sessions
			select_query = """
			SELECT roomID, roomType
			FROM Room
			WHERE roomType IN ('Cardio Room', 'Gym Room') AND availability = true
			"""
			cursor.execute(select_query)
			group_rooms = cursor.fetchall()

			if group_rooms:
				available_group_rooms = []
				for room_id, room_type in group_rooms:
					# Check if the room is available during the specified date and time
					check_query = """
					SELECT COUNT(*)
					FROM TrainingSession
					WHERE roomID = %s AND date = %s AND (
						(startTime <= %s AND endTime >= %s) OR 
						(startTime <= %s AND endTime >= %s) OR
						(startTime >= %s AND endTime <= %s)
					)
					"""
					cursor.execute(check_query, (room_id, date, start_time, start_time, end_time, end_time, start_time, end_time))
					count = cursor.fetchone()[0]

					# If count is 0, the room is available
					if count == 0:
						available_group_rooms.append((room_id, room_type))

				if available_group_rooms:
					print("Available Rooms for Group Fitness Class:")
					for i, (room_id, room_type) in enumerate(available_group_rooms, 1):
						print(f"{i}. Room {room_id} ({room_type})")

					room_choice = int(input("Select the room for the group fitness class: "))
					if 1 <= room_choice <= len(available_group_rooms):
						room_id, room_type = available_group_rooms[room_choice - 1]

						# Determine session type based on room type
						session_type = "Cardio Session" if room_type == "Cardio Room" else "Gym Session"

						# Insert into TrainingSession table
						insert_query = """
						INSERT INTO TrainingSession (roomID, sessionType, date, startTime, endTime, trainerID)
						VALUES (%s, %s, %s, %s, %s, %s)
						RETURNING sessionID
						"""
						cursor.execute(insert_query, (room_id, session_type, date, start_time, end_time, trainer_id))
						session_id = cursor.fetchone()[0]

						connection.commit()
						print("Group Fitness Class scheduled successfully!")
						print("")
					else:
						print("Invalid room choice.")
						print("")
				else:
					print("No available rooms for the selected date and time.")
					print("")
			else:
				print("No suitable rooms available for group fitness classes.")
				print("")


		elif choice.lower() == 'q':
			return	# Quit option

		else:
			print("Invalid choice. Please select again.")

	except psycopg2.Error as err:
		print("Error managing schedule")
		print(err)

	finally:
		if cursor:
			cursor.close()


# Trainers menu
def main_menu(connection):
	while True:
		trainer_id = input("Please enter your trainer ID: ")

		# Check if the provided ID belongs to a trainer
		if check_trainer(trainer_id, connection):
			while True:
				print("Welcome to the Health and Fitness Club Management System!")
				print("1. Schedule Management")
				print("2. Member Profile View")
				print("Q. Quit")
				print("")

				choice = input("Please select your option: ")

				if choice == '1':
					# Call function for schedule management
					print("")
					trainer_schedule(trainer_id, connection)
				elif choice == '2':
					# Call function for member profile view
					print("")
					trainer_view(trainer_id, connection)
				elif choice.upper() == 'Q':
					print("")
					print("Goodbye!")
					connection.close()	# Close connection before exiting
					return
				else:
					print("Incorrect input. Please try again.")
		else:
			print("Invalid trainer ID. Please try again.")


# Example usage:
if __name__ == "__main__":
	connection = connect()
	if connection:
		main_menu(connection)