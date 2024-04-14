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


# Member menu function
def member_menu(member_id, connection):
	print(f"Welcome Member ID: {member_id}")
	print("1. Profile Management")
	print("2. Dashboard Display")
	print("3. Schedule Management")
	print("Q. Quit")

	choice = input("Please select your option: ")
	print("")

	if choice == '1':
		manage_profile(member_id, connection)  # Pass connection parameter
	elif choice == '2':
		display_dashboard(member_id, connection)
	elif choice == '3':
		manage_schedule(member_id, connection)
	elif choice.upper() == 'Q':
		print("")
	else:
		print("Invalid choice. Please select again.")


def check_member(member_id, connection):
	try:
		cursor = connection.cursor()

		# Query to check if the provided member ID exists in the Members table
		select_query = """
		SELECT COUNT(*) FROM Members
		WHERE memberID = %s
		"""
		cursor.execute(select_query, (member_id,))
		count = cursor.fetchone()[0]

		return count == 1

	except psycopg2.Error as err:
		print("Error checking member ID")
		print(err)

	finally:
		if cursor:
			cursor.close()


# User Registration function
def register_user(connection):
	try:
		cursor = connection.cursor()

		# Gather member details
		first_name = input("Enter your first name: ").upper()
		last_name = input("Enter your last name: ").upper()
		email = input("Enter your email: ")
		address = input("Enter your address: ")
		phone_number = input("Enter your phone number: ")
		cc = input("Enter your credit card number: ")

		# Inserting member details into the Members table
		insert_query = """
		INSERT INTO Members (firstName, lastName, email, address, phoneNumber, cc)
		VALUES (%s, %s, %s, %s, %s, %s)
		RETURNING memberID
		"""
		cursor.execute(insert_query, (first_name, last_name, email, address, phone_number, cc))
		member_id = cursor.fetchone()[0]

		# Gather personal information
		target_date = input("Enter target date (YYYY-MM-DD): ")
		age = input("Enter your age: ")
		height = input("Enter your height (in cm): ")
		fitness_goal = input("Enter your fitness goal: ")
		init_weight = input("Enter your initial weight (in kg): ")
		sex = input("Enter your sex (M/F): ").upper()

		# Inserting personal information into the PersonalInfo table
		insert_personal_query = """
		INSERT INTO PersonalInfo (memberID, targetDate, age, height, fitnessGoal, initWeight, sex)
		VALUES (%s, %s, %s, %s, %s, %s, %s)
		"""
		cursor.execute(insert_personal_query, (member_id, target_date, age, height, fitness_goal, init_weight, sex))

		# VO2Max and BMI are null, because the member just registered...

		# Create an empty entry in the Exercise table
		insert_exercise_query = """
		INSERT INTO Exercise (memberID, difficulty, name, description)
		VALUES (%s, NULL, NULL, NULL)
		"""
		cursor.execute(insert_exercise_query, (member_id,))

		connection.commit()

		print("User registered successfully!")

	except psycopg2.Error as err:
		print("Error registering user")
		print(err)

	finally:
		if cursor:
			cursor.close()


# Profile Management function
def manage_profile(member_id, connection):
	try:
		cursor = connection.cursor()

		# Fetch current member details
		select_query = """
		SELECT * FROM Members WHERE memberID = %s
		"""
		cursor.execute(select_query, (member_id,))
		member_details = cursor.fetchone()

		print("Current Member Details:")
		print(f"Member ID: {member_details[0]}")
		print(f"First Name: {member_details[1]}")
		print(f"Last Name: {member_details[2]}")
		print(f"Email: {member_details[3]}")
		print(f"Address: {member_details[4]}")
		print(f"Phone Number: {member_details[5]}")
		print(f"Credit Card: {member_details[6]}")

		print("\nWhat do you want to update?")
		print("1. Personal Information")
		print("2. Fitness Goals")
		print("3. Health Metrics (Current Weight, VO2Max, BMI)")
		print("Q. Quit")

		choice = input("Enter your choice: ")

		if choice == '1':
			# Update personal information
			first_name = input("Enter new first name: ").upper()
			last_name = input("Enter new last name: ").upper()
			email = input("Enter new email: ")
			address = input("Enter new address: ")
			phone_number = input("Enter new phone number: ")
			credit_card_number = input("Enter new credit card number: ")

			update_query = """
			UPDATE Members
			SET firstName = %s, lastName = %s, email = %s, address = %s, phoneNumber = %s, cc = %s
			WHERE memberID = %s
			"""
			cursor.execute(update_query, (first_name, last_name, email, address, phone_number, credit_card_number, member_id))
			connection.commit()

			print("Personal information updated successfully!")

		elif choice == '2':
			# Update fitness goals
			fitness_goal = input("Enter new fitness goal: ")

			update_query = """
			UPDATE PersonalInfo
			SET fitnessGoal = %s
			WHERE memberID = %s
			"""
			cursor.execute(update_query, (fitness_goal, member_id))
			connection.commit()

			print("Fitness goal updated successfully!")

		elif choice == '3':
			# Update health metrics
			curr_weight = input("Enter new current weight: ")
			curr_vo2max = input("Enter new current VO2Max: ")
			curr_bmi = input("Enter new current BMI: ")

			update_query = """
			UPDATE PersonalInfo
			SET currWeight = %s, currVO2Max = %s, currBMI = %s
			WHERE memberID = %s
			"""
			cursor.execute(update_query, (curr_weight, curr_vo2max, curr_bmi, member_id))
			connection.commit()

			print("Health metrics updated successfully!")

		elif choice.upper() == 'Q':
			print("Quitting profile management.")

		else:
			print("Invalid choice.")

	except psycopg2.Error as err:
		print("Error managing profile")
		print(err)

	finally:
		if cursor:
			cursor.close()


# Dashboard Display function
def display_dashboard(member_id, connection):
	try:
		cursor = connection.cursor()

		# Fetch exercise routines
		select_exercise_query = """
		SELECT name, description
		FROM Exercise
		WHERE memberID = %s
		"""
		cursor.execute(select_exercise_query, (member_id,))
		exercise_routines = cursor.fetchall()

		print("Exercise Routines:")
		for routine in exercise_routines:
			print(f"Name: {routine[0]}")
			print(f"Description: {routine[1]}")
			print()

		# Fetch health statistics
		select_health_query = """
		SELECT initWeight, currWeight, initVO2Max, currVO2Max, initBMI, currBMI
		FROM PersonalInfo
		WHERE memberID = %s
		"""
		cursor.execute(select_health_query, (member_id,))
		health_stats = cursor.fetchone()

		print("Health Statistics:")
		print(f"Initial Weight: {health_stats[0]} kg")
		print(f"Current Weight: {health_stats[1]} kg")
		print(f"Initial VO2Max: {health_stats[2]}")
		print(f"Current VO2Max: {health_stats[3]}")
		print(f"Initial BMI: {health_stats[4]}")
		print(f"Current BMI: {health_stats[5]}")

	except psycopg2.Error as err:
		print("Error displaying dashboard")
		print(err)

	finally:
		if cursor:
			cursor.close()


# Schedule Management function
def manage_schedule(member_id, connection):
	try:
		cursor = connection.cursor()

		print("Schedule Management")
		print("1. Join Personal Training Session")
		print("2. Join Group Fitness Class")
		print("Q. Quit")

		choice = input("Please select your option: ")

		if choice == '1':
			# Personal Training Session (NOT Gym Session or Cardio Session)
			# Fetch available personal training sessions not attended by anyone
			select_personal_query = """
			SELECT sessionID, date, startTime
			FROM TrainingSession
			WHERE sessionType NOT IN ('Gym Session', 'Cardio Session') AND
				  sessionID NOT IN (
					  SELECT sessionID FROM MemberSession
				  )
			"""
			cursor.execute(select_personal_query)
			personal_sessions = cursor.fetchall()

			if personal_sessions:
				print("Available Personal Training Sessions:")
				for session in personal_sessions:
					print(f"Session ID: {session[0]}, Date: {session[1]}, Time: {session[2]}")

				session_id = input("Enter the session ID you want to join: ")
				session_id = int(session_id)

				if any(session_id == session[0] for session in personal_sessions):
					# Link session with member
					insert_member_session_query = """
					INSERT INTO MemberSession (sessionID, memberID)
					VALUES (%s, %s)
					"""
					cursor.execute(insert_member_session_query, (session_id, member_id))
					
					connection.commit()
					print("Personal Training Session joined successfully!")
				else:
					print("Invalid session ID. Please try again.")
			else:
				print("No available personal training sessions.")

		elif choice == '2':
			# Group Fitness Class
			# Fetch available group fitness classes (Gym Session or Cardio Session)
			select_group_query = """
			SELECT T.sessionID, T.date, T.startTime, R.roomID
			FROM TrainingSession T
			JOIN Room R ON T.roomID = R.roomID
			WHERE T.sessionType IN ('Gym Session', 'Cardio Session') AND
				  T.sessionID NOT IN (
					  SELECT sessionID FROM MemberSession WHERE memberID = %s
				  )
			"""
			cursor.execute(select_group_query, (member_id,))
			group_sessions = cursor.fetchall()

			if group_sessions:
				print("Available Group Fitness Classes:")
				for session in group_sessions:
					print(f"Session ID: {session[0]}, Date: {session[1]}, Time: {session[2]}, Room ID: {session[3]}")

				session_id = input("Enter the session ID you want to join: ")
				session_id = int(session_id)

				if any(session_id == session[0] for session in group_sessions):
					# Check if room has available capacity
					room_id = [session[3] for session in group_sessions if session[0] == session_id][0]
					select_capacity_query = """
					SELECT capacity
					FROM Room
					WHERE roomID = %s
					"""
					cursor.execute(select_capacity_query, (room_id,))
					room_capacity = cursor.fetchone()[0]

					# Check room capacity
					select_count_query = """
					SELECT COUNT(sessionID)
					FROM MemberSession
					WHERE sessionID = %s
					"""
					cursor.execute(select_count_query, (session_id,))
					session_count = cursor.fetchone()[0]

					if session_count < room_capacity:
						# Link session with member
						insert_member_session_query = """
						INSERT INTO MemberSession (sessionID, memberID)
						VALUES (%s, %s)
						"""
						cursor.execute(insert_member_session_query, (session_id, member_id))
						
						connection.commit()
						print("Group Fitness Class joined successfully!")
					else:
						print("The group fitness class is full. Please choose another session.")
				else:
					print("Invalid session ID. Please try again.")
			else:
				print("No available group fitness classes.")

		elif choice.upper() == 'Q':
			print("Quitting schedule management.")

		else:
			print("Invalid choice.")

	except psycopg2.Error as err:
		print("Error managing schedule")
		print(err)

	finally:
		if cursor:
			cursor.close()


# For members
def main_menu(connection):
	print("Welcome to the Health and Fitness Club Management System!")
	print("1. Existing Member")
	print("2. New Customer")
	print("Q. Quit")

	while True:
		choice = input("Please select your option: ")

		if choice == '1':  # Existing Member
			member_id = input("Please enter your member ID: ")
			if check_member(member_id, connection):
				print("")
				member_menu(member_id, connection)	  # Pass connection parameter
				break
			else:
				print("Member does not exist. Please try again.")
		elif choice == '2':	  # New Customer
			register_user(connection)
			break
		elif choice.upper() == 'Q':
			print("Goodbye!")
			break
		else:
			print("Incorrect input. Please select again.")


# Example usage:
if __name__ == "__main__":
	connection = connect()
	if connection:
		main_menu(connection)
		connection.close()
