# Paying Guest House Management System

## Table of Contents:
- [About the Application](#about-the-app)
- [Installation](#installation)
- [Directory Structure](#directory-structure)
- [Application Demo](#application-demo)
- [Contribution](#contribution)
- [License](#license)

## About the App: 
  This project aims to completely automate a Paying Guest House and Restaurant (PGHR), and reduce data redundancies and delays throughout the PGHR     Management. This would lead to a much more efficiently running hotel and a better experience for the customers.
  Below are the following functional objectives:
- Rooms Accommodation and Mess management by the admin. Easier Access to the backend data instead of scrolling through pages of the records (books).
- Allocation and Revoking of Rooms by the Admin.
- Customer accessing rooms for booking
- Customer can check their room details, raise tickets and check announcements posted by the admin
  - Eg. Announcement – Water won’t be available during a specific section of a day
  - Eg. Ticket – Room Cleaning
- Admin is provided with access to the billing software that can be used to bill customers of the attached restaurant. Admin access controls can be modified in such a way that a person can only access a particular section of the console only
- Landing Page that will act as a publicity objective where a customer can check out the rooms, mess, and locate the PGHR.

## Installation 
1. Clone the repo
```
git clone https://github.com/akhilsrinivasp/pg-management-system.git
cd pg-management-system
```
2. Create a Python Virtual Environment
```
python -m venv .env
source .env/bin/activate #for Linux/Mac Users
.env\Scripts\activate #for Windows Users
```
3. Use the requirements file to install the dependencies
```
#make sure the environment is activated
python -m pip install -r requirements.txt
```
4. Run the application:
```
flask run
```
or
```
python app.py
```

## Directory Structure:
```
|-pghr
|---config.py
|---controllers.py
|---database.py
|---models.py
|---temp.db
|-static
|---images
|---css
|-templates
|---admin
|-----announcement.html
|-----base.html
|-----booking.html
|-----dashboard.html
|-----mess_booking.html
|-----navbar.html
|-----room_booking.html
|-----ticket.html
|---customer
|-----announcement.html
|-----base.html
|-----booking.html
|-----dashboard.html
|-----navbar.html
|-----ticket.html
|---index
|-----base.html
|-----index_navbar.html
|-----index.html
|-----login.html
|-----signup.html
|-app.py
|-ReadMe.md
|-requirements.txt
```

## Application Demo

### Landing Page
![image](https://github.com/akhilsrinivasp/pg-management-system/assets/71825776/3dad41a5-6ec2-4028-971b-7d75e54c04cc)
![image](https://github.com/akhilsrinivasp/pg-management-system/assets/71825776/0a984bc4-a485-4507-8701-1e392bfdcac9)

### Admin Dashboard 
![image](https://github.com/akhilsrinivasp/pg-management-system/assets/71825776/8972e055-19de-460b-b29e-414a721bd560)
![image](https://github.com/akhilsrinivasp/pg-management-system/assets/71825776/274d8640-512e-45cb-ac73-4595aace259a)
![image](https://github.com/akhilsrinivasp/pg-management-system/assets/71825776/b876bb2a-b949-4538-8405-0363c0c4534a)
![image](https://github.com/akhilsrinivasp/pg-management-system/assets/71825776/c854ec21-6fbd-4ed4-a5b0-e5e76159b294)

### Customer Dashboard
![image](https://github.com/akhilsrinivasp/pg-management-system/assets/71825776/13f1d505-18cb-4936-9c85-8f8ea3b5c194)
![image](https://github.com/akhilsrinivasp/pg-management-system/assets/71825776/a2d3fee7-eb15-4331-b059-10a32eadfd99)
![image](https://github.com/akhilsrinivasp/pg-management-system/assets/71825776/989b7350-7ffd-43f1-9c56-8ad2027a9c9f)
![image](https://github.com/akhilsrinivasp/pg-management-system/assets/71825776/afd76a7b-7194-4ef6-b718-0fd701e645c4)

## Contribution
Contributions to the project are welcome! If you find any bugs, have feature suggestions, or want to improve the code, feel free to open an issue or submit a pull request.

## License
This project is licensed under the Apache License. Feel free to use, modify, and distribute the code according to the terms of the license.
