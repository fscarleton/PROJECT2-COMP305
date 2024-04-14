-- Members table
CREATE TABLE Members (
	memberID SERIAL PRIMARY KEY,
	firstName VARCHAR(50),
	lastName VARCHAR(50),
	email VARCHAR(100),
	address VARCHAR(255),
	phoneNumber VARCHAR(15),
	cc VARCHAR(16)
);

-- PersonalInfo table
CREATE TABLE PersonalInfo (
	memberID INT PRIMARY KEY REFERENCES Members(memberID),
	targetDate DATE,
	age SMALLINT,
	height SMALLINT, -- in cm
	fitnessGoal VARCHAR(255),
	initWeight SMALLINT, -- in kg
	currWeight SMALLINT,
	initVO2Max SMALLINT,
	currVO2Max SMALLINT,
	initBMI DECIMAL(5, 2),
	currBMI DECIMAL(5, 2),
	sex CHAR(1)
);

-- Exercise table
CREATE TABLE Exercise (
	memberID INT PRIMARY KEY REFERENCES Members(memberID),
	difficulty SMALLINT, -- 1 to 5
	name VARCHAR(100),
	description TEXT
);

-- Room Table
CREATE TABLE Room (
	roomID SERIAL PRIMARY KEY,
	roomType VARCHAR(50),
	capacity INT,
	availability BOOLEAN
);

-- BookedRoom Table
CREATE TABLE BookedRoom (
	roomID INT,
	date DATE,
	startTime TIME,
	endTime TIME,
	PRIMARY KEY (roomID, date, startTime),
	FOREIGN KEY (roomID) REFERENCES Room(roomID)
);

-- Staff table
CREATE TABLE Staff (
	staffID SERIAL PRIMARY KEY,
	firstName VARCHAR(50),
	lastName VARCHAR(50),
	email VARCHAR(100),
	address VARCHAR(255),
	phoneNumber VARCHAR(15),
	role VARCHAR(100)
);

-- Trainer table
CREATE TABLE Trainer (
	staffID SERIAL PRIMARY KEY REFERENCES Staff(staffID),
	cert VARCHAR(100)
);

-- TrainingSession Table
CREATE TABLE TrainingSession (
	sessionID SERIAL PRIMARY KEY,
	roomID INT,
	sessionType VARCHAR(50),
	date DATE,
	startTime TIME,
	endTime TIME,
	trainerID INT,
	FOREIGN KEY (roomID) REFERENCES Room(roomID),
	FOREIGN KEY (trainerID) REFERENCES Staff(staffID)
);

-- MemberSession table
CREATE TABLE MemberSession (
	sessionID INT,
	memberID INT,
	PRIMARY KEY (sessionID, memberID),
	FOREIGN KEY (sessionID) REFERENCES TrainingSession(sessionID),
	FOREIGN KEY (memberID) REFERENCES Members(memberID)
);

-- Equipment table
CREATE TABLE Equipment (
	equipID SERIAL PRIMARY KEY,
	description TEXT,
	status VARCHAR(50),
	roomID INT,
	dateReported TIMESTAMP,
	FOREIGN KEY (roomID) REFERENCES Room(roomID)
);

-- BillingAndPayments table
CREATE TABLE BillingAndPayments (
	transID SERIAL PRIMARY KEY,
	amount DECIMAL(10, 2),
	dateNtime TIMESTAMP,
	transacType VARCHAR(50),
	memberID INT,
	FOREIGN KEY (memberID) REFERENCES Members(memberID)
);
