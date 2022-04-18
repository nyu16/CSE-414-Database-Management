CREATE TABLE Vehicle(
	licensePlate VARCHAR(10),
	ssn INT REFERENCES Person(ssn),
	name VARCHAR(100) REFERENCES InsuranceCo(name),
	year INT,
	maxLiability REAL,
	PRIMARY KEY(licensePlate, name, ssn)
);

CREATE TABLE Truck(
	licensePlate VARCHAR(10) REFERENCES Vehicle(licensePlate),
	ssn INT REFERENCES ProfessionalDriver(ssn),
	capacity INT,
	PRIMARY KEY (licensePlate, ssn)
);

CREATE TABLE Car( 
	licensePlate VARCHAR(10) REFERENCES Vehicle(licensePlate),
	make VARCHAR(100),
	PRIMARY KEY (licensePlate)
);

CREATE TABLE Person(
	name VARCHAR(100),
	ssn INT PRIMARY KEY
);

CREATE TABLE Driver(
	name VARCHAR(100) REFERENCES Person(name),
	ssn INT REFERENCES Person(ssn),
	driverID INT,
	PRIMARY KEY(ssn)
);

CREATE TABLE InsuranceCo(
	phone INT,
	name VARCHAR(100) PRIMARY KEY
);

CREATE TABLE NonProfessionalDriver(
	ssn INT REFERENCES Driver(ssn),
	PRIMARY KEY(ssn)
);

CREATE TABLE ProfessionalDriver(
	medicalHistory VARCHAR(100),
	ssn INT REFERENCES Driver(ssn),
	PRIMARY KEY(ssn)
);

CREATE TABLE Drives(
	ssn INT REFERENCES NonProfessionalDriver(ssn),
	licensePlate VARCHAR(10) REFERENCES Car(licensePlate),
	PRIMARY KEY(ssn, licensePlate)
);

/*
b: I have represented the relation "insures" by table vehicle references name from InsuranceCo table, and by adding another column, maxLiability.
   The reason for such action is that the relation between vehicle and InsuranceCo was 1 to many (or N). Therefore, table vehicle should contain
   a single column from InsuranceCo. 

c: Operates reltion was 1(ProfessionalDriver) to many(Truck) whereas drives was many(NonProfessionalDriver) to many(Car). Thus, the Truck table
   contained a foreign key referenced from the ProfessionalDriver table whereas a seperate table was created to reference both primary keys from
   the Car table and the NonProfessional Driver table.
*/