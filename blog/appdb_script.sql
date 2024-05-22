create table ordersform (
	id integer PRIMARY KEY autoincrement,
	fname varchar(255) NOT NULL,
	email varchar(255),
	phone varchar(255),
	messages varchar(255),
	createdAt datetime,
	updatedAt datetime
);

create table logins (
	id integer PRIMARY KEY autoincrement,
	username varchar(255) NOT NULL UNIQUE,
	email varchar(255) NOT NULL UNIQUE,
	password varchar(255) NOT NULL UNIQUE
);