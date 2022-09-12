#from zoneinfo import available_timezones
from flask import render_template, flash, request
from app import app
from app import db, models

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
#     bookingId = booking.id
#     scooter = models.Scooter.query.filter_by(currentBookingID = bookingId)
#     return scooter


# def getScootersAtlocation(locationID):
#     scooters = 
#     return scooters



# p = models.User(role = False, firstName = "tom", surName = "schofield", 
# mobileNum = "876786768", email = "fkjvnflkbvnd", cardNum = "dkvfrjdhfolk",
# expireDate = "klcm", cvv = "ddd")


booking = models.Booking(customerId = 0)

booking = models.Scooter(available = False, currentBookingID = booking.id, locationID = 0)

db.session.add(booking)
db.session.add(booking)
db.session.commit()

x = getScooterByUser(0)
print(x)