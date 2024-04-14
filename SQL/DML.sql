-- Members Table
INSERT INTO Members (firstName, lastName, email, address, phoneNumber, cc)
VALUES
	('DIDA', 'SANTOS', 'dida@example.com', 'Milan, Italy', '+1234567890', '1234567890123456'),
	('CAFU', 'DA SILVA', 'cafu@example.com', 'Milan, Italy', '+1234567891', '1234567890123457'),
	('PAOLO', 'MALDINI', 'maldini@example.com', 'Milan, Italy', '+1234567892', '1234567890123458'),
	('ALESSANDRO', 'NESTA', 'nesta@example.com', 'Milan, Italy', '+1234567893', '1234567890123459'),
	('RONALDO', 'NAZARIO', 'ronaldo@example.com', 'Milan, Italy', '+1234567894', '1234567890123460'),
	('GENNARO', 'GATTUSO', 'gattuso@example.com', 'Milan, Italy', '+1234567895', '1234567890123461'),
	('ANDREA', 'PIRLO', 'pirlo@example.com', 'Milan, Italy', '+1234567896', '1234567890123462'),
	('CLARENCE', 'SEEDORF', 'seedorf@example.com', 'Milan, Italy', '+1234567897', '1234567890123463'),
	('FILIPPO', 'INZAGHI', 'inzaghi@example.com', 'Milan, Italy', '+1234567898', '1234567890123464'),
	('ALBERTO', 'GILARDINO', 'gilardino@example.com', 'Milan, Italy', '+1234567899', '1234567890123465'),
	('MAREK', 'JANKULOVSKI', 'jankulovski@example.com', 'Milan, Italy', '+1234567800', '1234567890123466'),
	('RICARDO', 'KAKA', 'kaka@example.com', 'Milan, Italy', '+1234567801', '1234567890123467'),
	('HERNAN', 'CRESPO', 'crespo@example.com', 'Milan, Italy', '+1234567802', '1234567890123468'),
	('DANIELE', 'BONERA', 'bonera@example.com', 'Milan, Italy', '+1234567803', '1234567890123469'),
	('CHRISTIAN', 'ABBIATI', 'abbiati@example.com', 'Milan, Italy', '+1234567804', '1234567890123470');


-- PersonalInfo Table
INSERT INTO PersonalInfo (memberID, targetDate, age, height, fitnessGoal, initWeight, currWeight, initVO2Max, currVO2Max, initBMI, currBMI, sex)
VALUES
	(1, '2024-03-01', 45, 186, 'Lose Weight', 90, 85, 40, 42, 25.5, 24.8, 'M'),
	(2, '2024-03-05', 39, 174, 'Gains Muscle', 75, 80, 45, 48, 27.3, 26.5, 'M'),
	(3, '2024-03-10', 50, 187, 'Lose Weight', 85, 85, 42, 42, 24.2, 24.2, 'M'),
	(4, '2024-03-15', 42, 182, 'Gains Muscle', 80, 78, 38, 40, 23.5, 24.0, 'M'),
	(5, '2024-03-20', 35, 182, 'Improve Cardiovascular Endurance', 78, 75, 48, 50, 29.1, 30.2, 'M'),
	(6, '2024-03-25', 38, 175, 'Gains Muscle', 76, 78, 43, 45, 25.5, 26.8, 'M'),
	(7, '2024-03-30', 33, 180, 'Improve Cardiovascular Endurance', 82, 80, 50, 52, 30.9, 31.7, 'M'),
	(8, '2024-04-01', 48, 185, 'Lose Weight', 88, 82, 38, 40, 24.0, 24.9, 'M'),
	(9, '2024-04-05', 40, 178, 'Gains Muscle', 73, 76, 45, 48, 28.3, 29.5, 'M'),
	(10, '2024-04-10', 47, 184, 'Improve Cardiovascular Endurance', 87, 85, 40, 42, 23.6, 24.1, 'M'),
	(11, '2024-04-15', 41, 179, 'Gains Muscle', 79, 82, 42, 45, 25.6, 26.7, 'M'),
	(12, '2024-04-20', 36, 181, 'Gains Muscle', 77, 80, 44, 46, 26.0, 27.0, 'M'),
	(13, '2024-04-25', 49, 183, 'Improve Cardiovascular Endurance', 89, 88, 38, 42, 22.8, 23.5, 'M'),
	(14, '2024-04-30', 44, 188, 'Gains Muscle', 91, 90, 46, 48, 25.5, 26.2, 'M'),
	(15, '2024-05-01', 37, 177, 'Improve Cardiovascular Endurance', 84, 82, 40, 42, 25.5, 25.9, 'M');


-- Exercise Table
INSERT INTO Exercise (memberID, difficulty, name, description)
VALUES
	(1, 3, 'Soccer Drills', 'Dribbling, Passing, Shooting, Agility Ladder, Cone Drills'),
	(2, 4, 'Agility Training', 'Speed Ladder Drills, Cone Drills, Shuttle Runs, Side Steps, Jumping Drills'),
	(3, 2, 'Endurance Run', 'Interval Running, Sprint Intervals, Long Distance Running, Fartlek Training'),
	(4, 3, 'Strength and Stability', 'Squats, Lunges, Deadlifts, Bosu Ball Exercises, Stability Ball Leg Curls'),
	(5, 4, 'Plyometric Power', 'Box Jumps, Jump Squats, Lateral Bounds, Single Leg Bounds, Tuck Jumps'),
	(6, 3, 'Ball Control', 'Inside Foot Dribbling, Outside Foot Dribbling, Juggling, Ball Manipulation Drills'),
	(7, 5, 'High Intensity Interval Training (HIIT)', 'Sprint Intervals, Burpees, Jump Squats, Shuttle Runs, High Knees'),
	(8, 2, 'Dynamic Stretching', 'Leg Swings, Arm Circles, Walking Lunges, Leg Kicks, Arm Swings'),
	(9, 4, 'Explosive Power', 'Medicine Ball Throws, Power Cleans, Box Jumps, Plyometric Push-ups, Kettlebell Swings'),
	(10, 3, 'Agility and Coordination', 'Cone Drills, Agility Ladder Drills, Hurdle Jumps, Shuttle Runs, Quick Feet Drills'),
	(11, 4, 'Strength and Conditioning', 'Barbell Squats, Deadlifts, Bench Press, Pull-ups, Shoulder Press'),
	(12, 3, 'Leg Strength', 'Leg Press, Leg Extensions, Leg Curls, Calf Raises, Step-ups'),
	(13, 5, 'Soccer-specific Conditioning', 'Interval Runs, Sprint Repeats, Hill Sprints, Circuit Training, Shuttle Runs'),
	(14, 3, 'Functional Training', 'TRX Rows, Stability Ball Exercises, Cable Exercises, Kettlebell Swings, Medicine Ball Throws'),
	(15, 4, 'Core Stability', 'Planks, Russian Twists, Medicine Ball Throws, Cable Woodchops, Hanging Leg Raises');


-- Room Table
INSERT INTO Room (roomType, capacity, availability)
VALUES
	('Cardio Room', 5, true),
	('Gym Room', 5, true),
	('Private Room 1', 1, true),
	('Private Room 2', 1, true),
	('Private Room 3', 1, true);


-- BookedRoom Table
INSERT INTO BookedRoom (roomID, date, startTime, endTime)
VALUES
	(1, '2024-03-25', '12:00', '14:00'),	-- Cardio Room
	(3, '2024-03-25', '14:00', '16:00'),	-- Private Room
	(2, '2024-03-25', '16:00', '18:00');	-- Gym Room

	

-- Staff Table
INSERT INTO Staff (firstName, lastName, email, address, phoneNumber, role)
VALUES
	('FRANCESCO', 'TOTTI', 'totti@example.com', '123 Main Street, Cityville', '123-456-7890', 'Receptionist'),
	('PELE', 'DA SILVA', 'pele@example.com', '456 Elm Street, Townsville', '234-567-8901', 'Receptionist'),
	('ZINEDINE', 'ZIDANE', 'zidane@example.com', '789 Oak Street, Villageton', '345-678-9012', 'Trainer'),
	('JOHAN', 'CRUYFF', 'cruyff@example.com', '901 Maple Avenue, Hamletville', '456-789-0123', 'Trainer'),
	('MICHEL', 'PLATINI', 'platini@example.com', '234 Pine Street, Countryside', '567-890-1234', 'Trainer'),
	('FRANZ', 'BECKENBAUER', 'beckenbauer@example.com', '567 Cedar Road, Suburbia', '678-901-2345', 'Manager');



-- Trainer Table
INSERT INTO Trainer (staffID, cert)
VALUES
	(3, 'Certification 1'),
	(4, 'Certification 2'),
	(5, 'Certification 3');



-- TrainingSession Table
INSERT INTO TrainingSession (roomID, sessionType, date, startTime, endTime, trainerID)
VALUES
	(1, 'Cardio Session', '2024-03-25', '2024-03-25 12:00:00', '2024-03-25 14:00:00', 3),
	(2, 'Gym Session', '2024-03-25', '2024-03-25 16:00:00', '2024-03-25 18:00:00', 5),
	(3, 'Private Session', '2024-03-25', '2024-03-25 14:00:00', '2024-03-25 16:00:00', 4);


-- MemberSession Table
INSERT INTO MemberSession (sessionID, memberID)
VALUES
	(1, 2),
	(1, 5),
	(1, 7),
	(1, 10),
	(2, 14),	-- Session 2 is full
	(2, 12),
	(2, 11),
	(2, 9),
	(2, 6),
	(3, 1);


-- Equipment Table
INSERT INTO Equipment (roomID, description, dateReported, status)
VALUES
	(1, 'Treadmill', '2024-04-13 08:00:00', 'Functional'),
	(1, 'Stationary Bike', '2024-04-13 08:00:00', 'Functional'),
	(1, 'Elliptical Machine', '2024-04-13 08:00:00', 'Functional'),
	(2, 'Dumbbells', '2024-04-13 08:00:00', 'Functional'),
	(2, 'Resistance Bands', '2024-04-13 08:00:00', 'Functional'),
	(3, 'Bench Press', '2024-04-13 08:00:00', 'Functional'),
	(3, 'Squat Rack', '2024-04-13 08:00:00', 'Functional');



-- BillingAndPayments Table
INSERT INTO BillingAndPayments (memberID, amount, dateNtime, transacType)
VALUES
	(1, 1250.00, '2024-03-25 14:30:00', 'MEMBERSHIP FEE'),
	(2, 1250.00, '2024-03-25 15:45:00', 'MEMBERSHIP FEE'),
	(3, 1250.00, '2024-03-25 17:00:00', 'MEMBERSHIP FEE'),
	(4, 1250.00, '2024-03-25 14:30:00', 'MEMBERSHIP FEE'),
	(5, 1250.00, '2024-03-25 15:45:00', 'MEMBERSHIP FEE'),
	(6, 1250.00, '2024-03-25 17:00:00', 'MEMBERSHIP FEE'),
	(7, 1250.00, '2024-03-25 14:30:00', 'MEMBERSHIP FEE'),
	(8, 1250.00, '2024-03-25 15:45:00', 'MEMBERSHIP FEE'),
	(9, 1250.00, '2024-03-25 17:00:00', 'MEMBERSHIP FEE'),
	(10, 1250.00, '2024-03-25 14:30:00', 'MEMBERSHIP FEE'),
	(11, 1250.00, '2024-03-25 15:45:00', 'MEMBERSHIP FEE'),
	(12, 1250.00, '2024-03-25 17:00:00', 'MEMBERSHIP FEE'),
	(13, 1250.00, '2024-03-25 14:30:00', 'MEMBERSHIP FEE'),
	(14, 95.00, '2024-03-25 14:30:00', 'SINGLE SESSION'),
	(15, 95.00, '2024-03-25 15:45:00', 'SINGLE SESSION');
