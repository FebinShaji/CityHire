Group Members:
Zheng Luk                sc20zrl
Shan-E-Haider Devraj     ed19sehd
Jiaqi Xie                sc20jx2
Robert Dennis            sc20rmd
Tom Schofield            ed19ts3
Febin Shaji              ed192fs
Shruti Rajesh Naik       sc20srn


About this project:
This project is about a scooter booking website. Providing a user-friendly interface and a variety of features to users, including extend bookings, raise complaints, etc


Customer role:


Customers can book a scooter as a logged in user. They can create a new account if they have not. Customers are first guided to a map, showing the places that they can book a scooter. They can click on the desired location and book the scooter after providing the card payment details. Customers will then receive an email confirmation to confirm their booking. If the customer wishes to extend the time of booking, they can extend through the website by paying. They can also submit a complaint.


Employee role:


Includes all features of the Customer role. Allow viewing complaints made by the user and book for non-registered customers.


Manager role:


Allow prioritizing complaints, viewing statistics, configuring and viewing scooters.

It is also deployed at http://ed19ts3.pythonanywhere.com

How to use:
    How to use flask:
    1. Create a virtual environment
    2. Install the additional packages listed in requirement.txt
    3. clone the repo from https://gitlab.com/university-of-leeds5/comp2913-gp
    4. move into your virtual environment
    5. cd into the repo then into Website
    6. run "python -m flask run"
    * need to downgrade MarkupSafe to version 2.0.1 and WTForms 2.3.3
    
    How to access manager role:
    1. Login with the username: manager and password: 123


    How to access employee role:
    1. Login with the username: employee and password: 123


    How to access Customer role:
    1. Login with the username: tom and password: 123