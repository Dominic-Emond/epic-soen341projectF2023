Create DATABASE epic_soen341;
USE epic_soen341;

Create table Broker (
	Id INT auto_increment primary key,
    First_Name TEXT,
    Last_Name TEXT,
    Email_Address TEXT,
    Username TEXT,
    Pass TEXT
);

Create Table Client (
	Id INT auto_increment primary key,
    First_Name TEXT,
    Last_Name TEXT,
    Type TEXT,
    Username TEXT,
    Pass TEXT
);

Create Table Property (
	Id INT auto_increment primary key,
    Broker_Id INT,
    Address TEXT,
    Price DECIMAL
);

Alter TABLE Property
ADD Constraint fk_broker
FOREIGN KEY (Broker_Id)
References Broker(Id);

Create Table Image (
	Id INT auto_increment primary key,
    Property_Id INT,
    Image BLOB
);

Alter TABLE Image
ADD CONSTRAINT fk_property
FOREIGN KEY (Property_Id)
References Property(Id);