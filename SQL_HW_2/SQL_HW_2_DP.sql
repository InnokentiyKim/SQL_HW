CREATE TABLE IF NOT EXISTS employee (
	id SERIAL PRIMARY KEY,
	employee_name VARCHAR(30) NOT NULL,
	department VARCHAR(40) NOT NULL
	);
	
create table if not exists chief (
	id SERIAL PRIMARY KEY,
	employee_id INTEGER UNIQUE REFERENCES employee(id),
	chief_id INTEGER REFERENCES employee(id)
	);