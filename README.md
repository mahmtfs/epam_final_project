[![Coverage Status](https://coveralls.io/repos/github/mahmtfs/epam_final_project/badge.svg?branch=master)](https://coveralls.io/github/mahmtfs/epam_final_project?branch=master)

# Departments project

---
The project is essentially a Flask web application for managing departments and employees.
It uses PostgreSQl to manage data, but technically it can use any database supported by SQLAlchemy. 
The connection between front-end and back-end is done with REST-API.

With this application you can:

* interact with database
* create, read, update and delete departments, employees and requests (special models created for communication between regular users and admins)
* search departments, employees and requests by name
* count average salary among all employees in every department
* make REST-API requests
* logging every step for checking errors

---

Main libraries used:

1. Flask-SQLAlchemy - to add support for SQLAlchemy ORM
2. Flask-Admin - to make a comfortable admin panel
3. Flask-Migrate - for handling database migrations

---

# Requirements

---

This project requires modules as: Flask, SQLAlchemy and others mentioned in [requerements.txt](https://github.com/mahmtfs/epam_final_project/blob/master/requirements.txt).
To download everything from there you can type:

```commandline
pip install -r requirements.txt
```

# Instalation

---

### To install current project you can click on the button "Code" and download it with

```commandline
git clone git@github.com:mahmtfs/epam_final_project.git
```

# Running the application
Before running the application make sure that you have installed everything from requirements.txt (it is explained in the section "Requirements")

To run this application you should go to the directory of this project 
with command **cd** and run appication using **gunicorn** that was in
requirements.txt

```commandline
cd epam_final_project     
gunicorn -c gunicorn.py.ini rest:app
```

If it doesn't work for you can run application with:

```commandline
python rest.py
```

# Making REST-API requests

---

To make REST-API requests check out all the available endpoints.
However, they require a JWT-token to be passed for access, so make sure you log in first
(to do this you have to pass POST request to http://127.0.0.1:5000/api-login with credentials in json format).

Here are all api endpoints with their methods:

* http://127.0.0.1:5000/api_login methods: GET, POST
    * log in to the application
* http://127.0.0.1:5000/api_register methods: GET, POST
    * register to the application
---
* http://127.0.0.1:5000/emps methods: GET
    * list all employees
* http://127.0.0.1:5000/emp/<emp_id> methods: GET
    * get an employee with **emp_id**
* http://127.0.0.1:5000/emp/<email> methods: GET
    * get an employee with **email**
* http://127.0.0.1:5000/emp methods: POST
    * create an emloyee
* http://127.0.0.1:5000/emp/<emp_id> methods: PATCH
    * update an employee with **emp_id**
* http://127.0.0.1:5000/emp/<emp_id> methods: DELETE
    * delete an employee with **emp_id**
* http://127.0.0.1:5000/emps/search/<que> methods: GET
    * get an employee by searching with query **que**
---
* http://127.0.0.1:5000/deps methods: GET
    * list all departments
* http://127.0.0.1:5000/dep/<dep_id> methods: GET
    * get a department with **dep_id**
* http://127.0.0.1:5000/dep/<title> methods: GET
    * get a department with **title**
* http://127.0.0.1:5000/dep methods: POST
    * create a department
* http://127.0.0.1:5000/dep/<dep_id> methods: PATCH
    * update a department with **dep_id**
* http://127.0.0.1:5000/dep/<dep_id> methods: DELETE
    * delete a department with **dep_id**
* http://127.0.0.1:5000/deps/search/<que> methods: GET
    * get a department by searching with query **que**
---
* http://127.0.0.1:5000/reqs methods: GET
    * list all requests
* http://127.0.0.1:5000/req/<req_id> methods: GET
    * get a request with **req_id**
* http://127.0.0.1:5000/req methods: POST
    * create a request
* http://127.0.0.1:5000/req/<req_id> methods: PATCH
    * update a request with **req_id**

### To make a request to http://127.0.0.1:5000/api_login you need to add credentials in json format:

```commandline
{
    "email": "email@email.com"
    "password": "password"
}
```

### To make a request to http://127.0.0.1:5000/api_register you need to add data in json format:

```commandline
{
	"firstname": "firstname"
	"lastname": "lastname"
	"email": "email@email.com"
	"password": "password"
	"dep_title": "department title"
	"birth_date": "1981-11-11"
}
```

### To make GET, POST, and DELETE requests for employees you need to make this json object:

```commandline
{
    "token": "token"
}
```

### To make PATCH requests for employees you need to make this json object:

```commandline
{
    "token": "token"
    //not necessary
    "password": "new password"
    "department_id": "new department id"
    "salary": "new salary"
}
```

### To make GET, POST, and DELETE requests for departments you need to make this json object:

```commandline
{
    "token": "token"
}
```

### To make PATCH requests for departments you need to make this json object:

```commandline
{
    "token": "token"
    //not necessary
    "title": "new title"
}
```

# Running tests

To run tests to see if everything works correct you can write in terminal:

```commandline
pytest
```
