import email
from http.client import FORBIDDEN
from flask import render_template, flash, request
from sqlalchemy import null
from app import app
from app import db, models
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from datetime import timedelta
import random


# def getUserInfo(id):
#     user = models.User.query.get(id)
#     return user

# def getScooterInfo(id):
#     scooter = models.Scooter.query.get(id)
#     return scooter

# def getLocationInfo(id):
#     location = models.Location.query.get(id)
#     return location

# def getAllScooters():
#     scooters = models.Scooter.query.all() # dont know if work yet
#     return scooters

# def getAllLoctaions():
#     locations = models.Location.query.all() # dont know if work yet
#     return locations

# def getScooterByUser(id):
#     booking = models.Booking.query.filter_by(customerId = id )
#     scooter = models.Scooter.query.filter_by(currentBookingID = booking.id )
#     return scooter


# def getScootersAtlocation(locationID):
#     scooters = 
#     return scooters



# p = models.User(role = False, firstName = "tom", surName = "schofield", 
# mobileNum = "876786768", email = "fkjvnflkbvnd", cardNum = "dkvfrjdhfolk",
# expireDate = "klcm", cvv = "ddd")

# db.session.add(p)
# db.session.commit()

# x = models.Issue.query.get(1)
# print(x)


def addAllLocations():
    deleteAllLocations()

    location1  = models.Location(LocationName = "Trinity centre", totalBookings = 0, 
    bookingThisMonth = 0)

    location2  = models.Location(LocationName = "Train station", totalBookings = 0, 
    bookingThisMonth = 0)

    location3  = models.Location(LocationName = "Merrion centre", totalBookings = 0, 
    bookingThisMonth = 0)

    location4  = models.Location(LocationName = "LGI hospital", totalBookings = 0, 
    bookingThisMonth = 0)

    location5  = models.Location(LocationName = "UoL Edge sports centre", totalBookings = 0, 
    bookingThisMonth = 0)

    db.session.add(location1)
    db.session.add(location2)
    db.session.add(location3)
    db.session.add(location4)
    db.session.add(location5)

    db.session.commit()
    locations = models.Location.query.all()

    # print(locations)

def deleteAllLocations():
    models.Location.query.delete()
    db.session.commit()

def addAllScooter():
    deleteAllScooters()

    # Scooter1  = models.Scooter(id = 100, available = True, locationID = 1)
    # db.session.add(Scooter1)

    # Scooter2  = models.Scooter(available = True, locationID = 1)
    # db.session.add(Scooter2)

    # Scooter3  = models.Scooter(available = True, locationID = 1)
    # db.session.add(Scooter3)
    
    # Scooter4  = models.Scooter(available = True, locationID = 1)
    # db.session.add(Scooter4)

    # Scooter5  = models.Scooter(available = True, locationID = 2)
    # db.session.add(Scooter5)

    # Scooter6  = models.Scooter(available = True, locationID = 2)
    # db.session.add(Scooter6)

    for i in range(20):
        if i < 10:
            id = 100 + i
        else:
            id = 200 + (i - 10)

        if i < 4:
            location = 1

        if i < 8 and i > 3:
            location = 2

        if i < 12 and i > 7:
            location = 3

        if i < 16 and i > 11:
            location = 4

        if i < 21 and i > 15:
            location = 5
        
        # print(location)

        Scooter  = models.Scooter(id = id, available = True, locationID = location)
        db.session.add(Scooter)


    db.session.commit()
    locations = models.Scooter.query.all()

    # print(locations)


def deleteAllScooters():
    models.Scooter.query.delete()
    db.session.commit()

def addEmployee():
    # deleteAllUser()
    User  = models.User(role = 3, username = "employee", 
    password = generate_password_hash("123", method='pbkdf2:sha256'))
    db.session.add(User)
    db.session.commit()

def addManager():
    # deleteAllUser()
    User  = models.User(role = 4, username = "manager", 
    password = generate_password_hash("123", method='pbkdf2:sha256'))
    db.session.add(User)
    db.session.commit()

def addCustomer():
    deleteAllUser()
    user = models.User(role=2, username="tom", password=generate_password_hash(
    "123", method='pbkdf2:sha256'), firstName="tom", surName="schofield", mobileNum="07788262432",
    email="tomschofield125@gmail.com")
    db.session.add(user)
    db.session.commit()

def addRates():
    # deleteAllUser()
    rate  = models.Rates(hourlyRate = 4, fourHourRate = 20, dailyRate = 49.99, weeklyRate = 100)
    db.session.add(rate)
    db.session.commit()

def deleteAllUser():
    models.User.query.delete()
    db.session.commit()

def deleteAllBookings():
    models.Booking.query.delete()
    db.session.commit()

def deleteAllIssues():
    models.Issue.query.delete()
    db.session.commit()

def makeTestBookings():
    deleteAllBookings()
    day = timedelta(days=1)
    minute = timedelta(minutes=3)
    year = timedelta(days=365)

    startTime = datetime.now() - year
    bookingDate = startTime
    bookings = random.randint(1,20)


    for i in range(365):
        bookings = bookings + random.randint(-5,5)
        if(bookings < 0):
            bookings = 1
        if(bookings > 20):
            bookings = 20   

        bookingDate = bookingDate + day
        lastbooking = bookingDate
        for b in range(bookings):
            lastbooking = lastbooking + minute
            #locId = random.randint(1,3)
            locId = 1
            booking  = models.Booking( dateMade = lastbooking, scooterId = 102, locationID = locId, customerId = 3, expired = True, cost = 4.50)
            db.session.add(booking)
    db.session.commit()


# def CheckBooking1():
#     booking = models.Booking.query.get(1)
#     if booking == None:


def FillDB():
    addRates()
    addCustomer()
    addEmployee()
    addManager()
    addAllLocations()
    addAllScooter()
    makeTestBookings()

def FillDBForTest():
    addRates()
    addCustomer()
    addEmployee()
    addManager()
    addAllLocations()
    addAllScooter()
    deleteAllBookings()
    
def creatTestBooking():
    x = timedelta(hours=1)
    booking  = models.Booking( dateMade = datetime.now(), scooterId = 102, locationID = 0, customerId = 3, expired = False, cost = 4.50, duration = datetime.now() + x, id = 2)
    db.session.add(booking)
    db.session.commit()

deleteAllIssues()
FillDB()


# addRates()
# addCustomer()
# addEmployee()
# addManager()
# addAllLocations()
# addAllScooter()
# makeTestBookings()


# bookings = models.Booking.query.all()
# print(bookings)

# ratesAll = models.Rates.query.all()
# rates = ratesAll[len(ratesAll)-1]

# print(rates)

# issues = models.Issue.query.all()
# issuesHigh = models.Issue.query.filter_by(pending=True).filter_by(Prio=1).filter_by(completed = False).all()
# issuesLow = models.Issue.query.filter_by(pending=True).filter_by(Prio=2).filter_by(completed = False).all()
# print(issues)
# user = models.User.query.filter_by(username="tom1").first()
# password=generate_password_hash("tom1", method='pbkdf2:sha256')
# print(password)
# print(user.password)
# print(check_password_hash(user.password, "tom1"))
# addAllLocations()

# addAllScooter()

# locations = models.Location.query.filter_by(LocationName = "Train station").all()
# location = locations[0]
# print(location)
# scooters = models.Scooter.query.filter_by(locationID = location.id).filter_by(available = True).all()
# print(scooters)