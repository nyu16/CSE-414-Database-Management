CREATE TABLE Caregivers (
    Username VARCHAR(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Availabilities (
    Time DATE,
    Username VARCHAR(255) REFERENCES Caregivers,
    PRIMARY KEY (Time, Username)
);

CREATE TABLE Vaccines (
    VName VARCHAR(255),
    Doses INT,
    PRIMARY KEY (VName)
);

CREATE TABLE Patients (
    PUser VARCHAR(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (PUser)
);

CREATE TABLE Appointments (
    AppointmentID INT,
    App_time DATE,
    Username VARCHAR(255) REFERENCES Caregivers(Username),
    PUser VARCHAR(255) REFERENCES Patients(PUser),
    VName VARCHAR(255) REFERENCES Vaccines(VName),
    PRIMARY KEY (AppointmentID)
);