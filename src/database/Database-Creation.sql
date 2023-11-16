Create DATABASE epic_soen341;
USE epic_soen341;

/* user table containing user information and permission */
Create table User (
	Id INT auto_increment primary key,
	First_Name VARCHAR(255) NOT NULL,
	Last_Name VARCHAR(255) NOT NULL,
	Username VARCHAR(255) NOT NULL,
	Password VARCHAR(255) NOT NULL,
	Email VARCHAR(255) NOT NULL,
	BrokerID INT(255),
	isBroker BOOLEAN, #enable broker permissions
	isClient BOOLEAN, #enable client permissions
	isSysAdmin BOOLEAN	#enable system administrator permissions
);

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
