from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Integer) # 0 for customer 1 for manager, 2 for student, 3 for senior
    weeklyHours = db.Column(db.Integer)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    firstName = db.Column(db.String(20))
    surName = db.Column(db.String(20))
    mobileNum = db.Column(db.String(11))
    email = db.Column(db.String(100))
    cardNum = db.Column(db.String(16))  # Null if manager
    expireDate = db.Column(db.String(5)) # 01/22  # Null if manager
    cvv  = db.Column(db.String(3)) # Null if manager

class Scooter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    available = db.Column(db.Boolean)
    currentBookingID = db.Column(db.Integer,db.ForeignKey('booking.id'))
    currentGuestBookingID = db.Column(db.Integer,db.ForeignKey('guest_book.id'))
    # currentGuestBookingID = db.Column(db.Integer)

    locationID = db.Column(db.Integer,db.ForeignKey('location.id'))

class Rates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hourlyRate = db.Column(db.Float)
    fourHourRate = db.Column(db.Float)
    dailyRate = db.Column(db.Float)
    weeklyRate = db.Column(db.Float)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    LocationName = db.Column(db.String(50))
    totalBookings = db.Column(db.Integer)
    bookingThisMonth = db.Column(db.Integer)
    bookingsPCM = db.Column(db.Float)


class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issueText = db.Column(db.String(500))
    devComments = db.Column(db.String(500))
    pending = db.Column(db.Boolean)
    completed = db.Column(db.Boolean)
    # toBeActedOn = db.Column(db.Boolean)
    customerId = db.Column(db.Integer,db.ForeignKey('user.id'))
    employeeId = db.Column(db.Integer,db.ForeignKey('user.id'))
    scooterId = db.Column(db.Integer,db.ForeignKey('scooter.id')) # null if not a scooter related problem
    dateMade = db.Column(db.DateTime) # to work out priority
    Prio = db.Column(db.Integer)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scooterId = db.Column(db.Integer,db.ForeignKey('scooter.id')) # null if not a scooter related problem
    locationID = db.Column(db.Integer,db.ForeignKey('location.id'))
    dateMade = db.Column(db.DateTime)
    customerId = db.Column(db.Integer,db.ForeignKey('user.id'))
    duration = db.Column(db.DateTime)
    expired = db.Column(db.Boolean)
    cost = db.Column(db.Float)


class GuestBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scooterId = db.Column(db.Integer,db.ForeignKey('scooter.id')) # null if not a scooter related problem
    cost = db.Column(db.Float)
    firstName = db.Column(db.String(20))
    surName = db.Column(db.String(20))
    email = db.Column(db.String(100))
    cardNum = db.Column(db.String(16))
    expireDate = db.Column(db.String(5))
    cvv  = db.Column(db.String(3))
    locationID = db.Column(db.Integer,db.ForeignKey('location.id'))
    dateMade = db.Column(db.DateTime)
    duration = db.Column(db.DateTime)
    booked = db.Column(db.Boolean)
    expired = db.Column(db.Boolean)


