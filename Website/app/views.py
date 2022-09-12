from calendar import month
from faulthandler import dump_traceback_later
from multiprocessing import managers
from pyexpat import model
from sqlite3 import Date
from flask import render_template, flash, request, redirect, url_for, session
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import null
from sqlalchemy.sql.elements import Null
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
from send_email import *
from .forms import *
from .models import *
from app import db, models
from sqlalchemy.sql import functions
from datetime import datetime
# import logging
import os
from werkzeug.datastructures import MultiDict
from datetime import timedelta



# Homepage
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

# Logout user
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    print("Logout successful")
    return render_template('home.html')

# Login user
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    global result
    result = {}
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')

        user = models.User.query.filter_by(username=username).first()
        if (user == None):
            flash('Incorrect username or password entered')
            print("Incorrect username or password entered")
            result = {"code": -1, "message": "Incorrect username or password entered"}


            return redirect(url_for('login'))
        elif (check_password_hash(user.password, password) == False):
            flash('Incorrect username or password entered')
            print("Incorrect username or password entered")
            result = {"code": -1, "message": "Incorrect username or password entered"}

            return redirect(url_for('login'))
        else:
            users = models.User.query.filter_by(username = username).all()

            user = users[0]
            session['user'] = user.id
            session['role'] = user.role

            result = {"code": 0, "message": "Login successful"}

            print("Login successful")

            if user.role == 3:
                return redirect(url_for('viewGuestBooking'))
            if user.role == 4:
                return redirect(url_for('statistics'))

            return redirect(url_for('dashboard'))
    return render_template('login.html', title='Log In', form=form)

# Register a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    global result
    result = {}
    print('registration started')
    if request.method == 'POST':
        firstName = request.form.get('FirstName')
        surName = request.form.get('Surname')
        email = request.form.get('Email')
        mobileNum = request.form.get('Number')
        username = request.form.get('Username')
        password = request.form.get('Password')
        confirm_password = request.form.get('Confirm_Password')
        userRoleBox = form.Type.data
        role = 0

        if userRoleBox == "Normal":
            role = 0
        if userRoleBox == "Student":
            role = 1
        if userRoleBox == "Over 60":
            role = 2

        print('got info')
        print(password)
        print(confirm_password)

        checkUser = models.User.query.filter_by(email=email).first()

        if checkUser:
            flash('Account with this email address already exists')
            print("Account with this email address already exists")
            result = {"code": -1, "message": "Account with this email address already exists"}

            return redirect(url_for('register', methods=['GET', 'POST']))

        else:            
            user = User(role=role, username=username, password=generate_password_hash(
            password, method='pbkdf2:sha256'), firstName=firstName, surName=surName, mobileNum=mobileNum,
            email=email)
            db.session.add(user)
            db.session.commit()

            print("Login successful")

            result = {"code": 0, "message": "Login successful"}

            return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Dashboard for customers
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    global result
    result = {}
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))
    form = AddCardDetails()
    if request.method == 'POST':
        user = models.User.query.get(session.get('user'))
        CardNumber = request.form.get('CardNumber')
        ExpiryDate = request.form.get('ExpiryDate')
        CVV = request.form.get('CVV')
        user.cardNum = CardNumber
        user.expireDate = ExpiryDate
        user.cvv = CVV
        db.session.commit()
        flash("Card details saved successfully!")
        print("Card details saved successfully!")
        result = {"code":0, "message":"Card details saved successfully!"}

        return redirect(url_for('home'))
    return render_template('dashboard.html', title='Dashboard', form=form)

# Allows user to change their password
@app.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
    global result
    result = {}
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))
    form = ChangePassword()
    if request.method == 'POST':
        user = models.User.query.get(session.get('user'))
        NewPassword = request.form.get('NewPassword')
        Confirm_NewPassword = request.form.get('Confirm_NewPassword')
        if NewPassword == Confirm_NewPassword:
            user.password = generate_password_hash(NewPassword, method='pbkdf2:sha256')
            db.session.commit()
            flash("Password changed successfully!")
            print("The password has been changed")
            result = {"code": 0, "message": "Password changed successfully!"}

            return redirect(url_for('dashboard'))
        else:
            flash("The passwords don't match!", 'error')
            print("The passwords don't match!")
            result = {"code": -1, "message": "The passwords don't match!"}
            return redirect(url_for('changepassword'))
    return render_template('changepassword.html', title='Change Password', form=form)

# Allows a customer to create an issue
@ app.route('/createissue', methods=['GET', 'POST'])
def createissue():
    global result
    result = {}
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))
    form=CreateIssue()
    if request.method == 'POST':
        ScooterID=request.form.get('ScooterID')
        Complaint=request.form.get('Complaint')
        dateMade=datetime.now()
        issue=Issue(scooterId=ScooterID,
                    issueText=Complaint, dateMade=dateMade, Prio = 2, pending = True, completed = False, customerId = session.get('user'))
        db.session.add(issue)
        db.session.commit()
        user = models.User.query.get(session.get('user'))
        sendIssuePending(ScooterID, user.email)
        flash('Successfully created issue.', 'success')
        print("Successfully created issue.")
        result = {"code": 0, "message": "Successfully created issue."}
        return redirect(url_for('dashboard'))
    return render_template('createissue.html', title='Create an Issue', form=form)

# Allows user to view map and available scooters
@ app.route('/mapUnselected', methods=['GET', 'POST'])
def mapUnselected():
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))

    return render_template('mapUnselectedWithNav.html', title='Display Map')

# Allows users to view available scooters in a location 
@ app.route('/viewScooters/<id>', methods=['GET', 'POST'])
def viewScooters(id):
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))

    if(id == "void"):
        form=LocationSelect()
    else:
        location=models.Location.query.get(id)
        print(location.LocationName)
        form=LocationSelect(formdata=MultiDict(
            {'LocationBox': location.LocationName}))
    scooters=None
    if request.method == 'POST':
        location=models.Location.query.filter_by(
            LocationName=form.LocationBox.data).first()
        scooters=models.Scooter.query.filter_by(
            locationID=location.id).filter_by(available=True).all()
    if(id != "void"):
        location=models.Location.query.filter_by(
            LocationName=form.LocationBox.data).first()
        scooters=models.Scooter.query.filter_by(
            locationID=location.id).filter_by(available=True).all()
    return render_template('viewScooters.html', title='View Scooters', form=form, Scooters=scooters)

# Allows users to book a scooter
@ app.route('/book/<id>', methods=['GET', 'POST'])
def book_ride(id):
    global result
    result = {}
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))
    form=CreateBooking()
    if request.method == 'POST':
        ratesAll = models.Rates.query.all()
        rates = ratesAll[len(ratesAll)-1]

        priceBefore = 0

        user = models.User.query.get(session.get('user'))
        duration = form.durationBox.data
        print(duration)
        if duration == "1hr":
            formattedDuration = timedelta(hours=1)
            priceBefore = rates.hourlyRate

        elif duration == "4hr":
            formattedDuration = timedelta(hours=4)
            priceBefore = rates.fourHourRate


        elif duration == "day":
            formattedDuration = timedelta(days=1)
            priceBefore = rates.dailyRate


        elif duration == "week":
            formattedDuration = timedelta(weeks=1)
            priceBefore = rates.weeklyRate

        price = priceBefore
        if user.role == 1:
            price = priceBefore * 0.9
        if user.role == 2:
            price = priceBefore * 0.8

        if form.useKnown.data == True:
            if user.cardNum == None:
                flash("No card data saved")
                result = {"code": -1, "message": "No card data saved"}
                return redirect("/book/" + id)
            flash("Saved card data used")
        else:

            if form.CardNumber.data == "":
                flash("No card number given")
                print("No card number given")
                result = {"code": -1, "message": "No card number given"}

                return redirect("/book/" + id)
            if form.CVV.data == "":
                flash("No card CVV given")
                print("No card CVV given")
                result = {"code": -1, "message": "No card CVV given"}

                return redirect("/book/" + id)
            if form.ExpiryDate.data == "":
                flash("No card ExpiryDate given")
                print("No card ExpiryDate given")
                result = {"code": -1, "message": "No card ExpiryDate given"}

                return redirect("/book/" +id)


        # flashString = "Charged £" + str(price)
        # flash(flashString)
        # scooter = models.Scooter.query.get(id)
        scooter = models.Scooter.query.get(id)


        if(scooter.currentBookingID != None):
            flash("Scooter allready in use")
            return redirect("/book/" +id)

        if(scooter.currentGuestBookingID != None):
            flash("Scooter allready in use")
            return redirect("/book/" +id)

        if(scooter.available != True):
            flash("Scooter allready in use")
            return redirect("/book/" +id)

        flashString = "Charged £" + str(price)
        flash(flashString)

        booking  = models.Booking( dateMade = datetime.now(), scooterId = id, locationID = scooter.locationID, customerId = user.id, duration = datetime.now()+formattedDuration, expired = False, cost = price)
        db.session.add(booking)
        # add payment logic

        #email logic
        location = models.Location.query.get(scooter.locationID)
        sendEmail(id, Date = datetime.now(), Duration = duration, Location = location.LocationName, recipient=user.email)

        # update scooter
        scooter.available = False
        scooter.currentBookingID = booking.id
        scooter.currentGuestBookingID = None

        db.session.add(scooter)
        db.session.commit()

        flash('Booking Successful')
        print("Booking Successful")
        result = {"code": 0, "message": "Booking successful!"}

        return redirect(url_for('viewBookings'))
    return render_template('book.html', title='Booking', form=form, id=id)

# Allows users to view their current bookings
@ app.route('/viewBookings', methods=['GET', 'POST'])
def viewBookings():
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))
    userId=session.get('user')
    Bookings=models.Booking.query.filter_by(
        customerId=userId).order_by(Booking.dateMade.desc()).all()
    return render_template('viewBookings.html', title='View Bookings', Bookings=Bookings)

# Allows user to cancel their booking
@ app.route('/cancelBooking/<id>', methods=['GET', 'POST'])
def cancelBooking(id):
    global result
    result = {}
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))
    Booking=models.Booking.query.get(id)
    if(Booking):
        scooter = models.Scooter.query.get(Booking.scooterId)
        scooter.available = True
        scooter.currentBookingID = None
        db.session.delete(Booking)
        db.session.commit()
        print("Booking Deleted")
        result = {"code": 0, "message": "Booking Deleted"}
    return redirect(url_for('viewBookings'))

# Allows user to extend their booking
@ app.route('/extendBooking/<id>', methods=['GET', 'POST'])
def extendBooking(id):
    global result
    result = {}
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))
    booking = models.Booking.query.get(id)
    form = ExtendBooking()
    if request.method == 'POST':
        if(booking):
            user = models.User.query.get(session.get('user'))
            ratesAll = models.Rates.query.all()
            rates = ratesAll[len(ratesAll)-1]
            timeExtended = form.durationBox.data
            priceBefore = 0
            if timeExtended == "1hr":
                extendTime = timedelta(hours=1)
                priceBefore = rates.hourlyRate


            elif timeExtended == "4hrs":
                extendTime = timedelta(hours=4)
                priceBefore = rates.fourHourRate


            elif timeExtended == "day":
                extendTime = timedelta(days=1)
                priceBefore = rates.dailyRate


            elif timeExtended == "week":
                extendTime = timedelta(weeks=1)
                priceBefore = rates.weeklyRate



            price = priceBefore
            if user.role == 1:
                price = priceBefore * 0.9
            if user.role == 2:
                price = priceBefore * 0.8

            if(booking.duration > datetime.now()):
                booking.duration = booking.duration + extendTime
                booking.cost = booking.cost + price
                db.session.commit()
                flashString = "Charged £" + str(price)
                flash(flashString)
                print("Booking Extended")
                result = {"code": 0, "message": "Booking Extended"}
                return redirect(url_for('viewBookings'))
            else:
                flash("Cant extend a Booking that has ended")
                print("Cant extend a Booking that has ended")
                result = {"code": 0, "message": "Cant extend a Booking that has ended"}
                return redirect(url_for('viewBookings'))

        result = {"code": 0, "message": "No booking with this ID"}


    return render_template('extend.html', form = form, booking = booking)


# Allows an employee to view scooters and their status !!!
@ app.route('/viewScootersStatus', methods=['GET', 'POST'])
def viewScootersStatuse():
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))
    return render_template('viewScootersStatus.html', title='View Scooters Status')

# Allows employees to update a scooter status
@ app.route('/updateScooters', methods=['GET', 'POST'])
def update_scooters():
    if session.get('user') == None:
        flash("Need to Login to access")
        return redirect(url_for('home'))

    form=ScooterAvailability()
    scooters=models.Scooter.query.all()
    if request.method == 'POST':
        a=models.Scooter.query.get(request.form.get('submitButton'))
        if a.available == True:
            a.available=False
        else:
            a.available=True
        db.session.commit()
        print("Scooter Updated")
        return redirect(url_for('update_scooters'))
    return render_template('updateScooters.html', title='Update Scooters', scooters=scooters, form=form)

# Allows an employee to view and update scooters 
@ app.route('/viewAllScooters', methods=['GET', 'POST'])
def viewAllScooters():
    global result
    result = {}
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))
    manager = 0
    employee = 0
    role = session.get('role')
    if role == 3:
        employee = 1
    if role == 4:
        manager = 1
    form = ScooterAvailability()
    scooters = models.Scooter.query.all()

    if request.method == 'POST':
        a=models.Scooter.query.get(request.form.get('submitButton'))
        if a.available == True:
            a.available=False
        else:
            a.available=True
            a.currentGuestBookingID = None
            a.currentBookingID = None
        db.session.commit()
        print("Scooter Updated")
        result = {"code": 0, "message": "Scooter Updated"}
        return redirect(url_for('viewAllScooters'))
    return render_template('viewAllScooters.html', title='All Scooters', scooters=scooters, form=form, employee = employee, manager = manager)

# Allows employees to view all issues and 
# set the priority of an issue from high to love
@ app.route('/viewIssues', methods=['GET', 'POST'])
def viewIssues():
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))
    manager = 0
    employee = 0
    role = session.get('role')
    if role == 3:
        employee = 1
    if role == 4:
        manager = 1
    if role < 3:
        flash("Employee Access Only")
        return redirect(url_for('home'))

    issues = models.Issue.query.all()
    issuesHigh = models.Issue.query.filter_by(pending=True).filter_by(Prio=1).filter_by(completed = False).all()
    issuesLow = models.Issue.query.filter_by(pending=True).filter_by(Prio=2).filter_by(completed = False).all()
    return render_template('All_Issues.html', title='Issues', issues = issues, issuesHighPrio=issuesHigh, issuesLowPrio = issuesLow, employee = employee, manager = manager)

# Allows managers to view high priority issues
@ app.route('/viewPriorityIssues', methods=['GET', 'POST'])
def viewPriorityIssues():
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))
    manager = 0
    employee = 0
    role = session.get('role')
    if role == 3:
        employee = 1
    if role == 4:
        manager = 1
    if role != 4:
        flash("Manager Access Only")
        return redirect(url_for('home'))

    issues = models.Issue.query.filter_by(pending=True).filter_by(Prio=1).all()
    return render_template('viewPriorityIssues.html', title='High Priority Issues', issues=issues, employee = employee, manager = manager)

# Allows the employees to view past solved issues
@ app.route('/pastIssues', methods=['GET', 'POST'])
def pastIssues():
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))
    manager = 0
    employee = 0
    role = session.get('role')
    if role == 3:
        employee = 1
    if role == 4:
        manager = 1
    if role < 3:
        flash("Manager Access Only")
        return redirect(url_for('home'))
    
    issues = models.Issue.query.filter_by(pending=False).filter_by(Prio=1).filter_by(completed = True).all()
    return render_template('pastIssues.html', title='Past Issues', issues=issues, employee = employee, manager = manager)    

# Marks an issue as completed/solved
@ app.route('/MarkAsCompleted/<id>', methods=['GET', 'POST'])
def MarkAsCompleted(id):
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))
    role = session.get('role')
    if role != 4:
        flash("Manager Access Only")
        return redirect(url_for('home'))


    issue = models.Issue.query.get(id)
    issue.pending = False
    issue.completed = True
    db.session.commit()
    customer = models.User.query.get(issue.customerId)
    print("Issue Marked As Complete")
    sendIssueComplete(issue.scooterId, customer.email)
    return redirect(url_for('viewPriorityIssues'))

# Marks an issue as high priority
@ app.route('/increasePrio/<id>', methods=['GET', 'POST'])
def increasePrio(id):
    global result
    result = {}
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))
    role = session.get('role')
    if role < 3:
        flash("Employee Access Only")
        return redirect(url_for('home'))


    issue = models.Issue.query.get(id)
    issue.Prio = 1
    db.session.commit()
    print("Issue increasePrio Successful")
    result = {"code": 0, "message": "Issue increasePrio Successful"}
    return redirect(url_for('viewIssues'))

# Marks an issue as low priority
@ app.route('/decreasePrio/<id>', methods=['GET', 'POST'])
def decreasePrio(id):
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))
    role = session.get('role')
    if role < 3:
        flash("Employee Access Only")
        return redirect(url_for('home'))
    issue = models.Issue.query.get(id)
    issue.Prio = 2
    db.session.commit()
    print("Issue decreasePrio Successful")
    return redirect(url_for('viewIssues'))

# Allows the manager to configure scooter prices
@app.route('/configureScooter', methods=['GET', 'POST'])
def configureScooter():
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))
    role = session.get('role')
    if role != 4:
        flash("Manager Access Only")
        return redirect(url_for('home'))

    form = ConfigureScooters()
    scooters = models.Scooter.query.all()
    if request.method == 'POST':
        hourlyRate = request.form.get('hourlyRate')
        fourHourRate = request.form.get('fourHourRate')
        dailyRate = request.form.get('dailyRate')
        weeklyRate = request.form.get('weeklyRate')
        rates = models.Rates(hourlyRate=hourlyRate, fourHourRate=fourHourRate, dailyRate=dailyRate, weeklyRate=weeklyRate)
        db.session.add(rates)
        db.session.commit()
        print("configureScooter (rates) Successful")
    # return render_template('configureScooter.html', title='Configure Scooters', form=form, scooters=scooters, employee = employee, manager = manager)
    return render_template('configureScooter.html', title='Configure Scooters', form=form)

# # Allows the manager to view sales statistics
# @app.route('/statistics', methods=['GET', 'POST'])
# def statistics():
#     if session.get('user') == None:
#         flash("Need to Login to access")
#         print("Need to Login to access")
#         return redirect(url_for('home'))
#     if session.get('user') == None:
#         flash("Need to Login to access")
#         print("Need to Login to access")
#         return redirect(url_for('home'))
#     role = session.get('role')
#     if role != 4:
#         flash("Manager Access Only")
#         return redirect(url_for('home'))

#     now = datetime.now()

#     totalProfit = None
#     averagePricePerBooking = None
#     numBookings = None

#     form = Statistics()

#     if request.method == 'POST':
#         timePeriod  = form.timeBox.data
#         #timePeriods = ["1 Week", "1 Month", "1 Quarter", "1 Year"]
#         if timePeriod == "1 Week":
#             deltaTime = timedelta(weeks=1)
#         elif timePeriod == "1 Month":
#             deltaTime = timedelta(weeks = 4)
#         elif timePeriod == "1 Quarter":
#             deltaTime = timedelta(weeks= 12)
#         elif timePeriod == "1 Year":
#             deltaTime = timedelta(weeks=52)
        
#         displayEnd = now - deltaTime
#         location = models.Location.query.filter_by(LocationName = form.LocationBox.data).first()


#         # bookings =  models.Booking.query.filter_by(locationID = location.id).filter_by(dateMade = displayEnd).all()
#         bookings =  models.Booking.query.filter_by(locationID = location.id).all()
#         if bookings:
#             numBookings = 0
#             totalProfit = 0

#             for b in bookings:
#                 if b.dateMade > displayEnd:
#                     totalProfit = totalProfit + b.cost
#                     numBookings = numBookings + 1

#             averagePricePerBooking = totalProfit / numBookings

#     return render_template('statistics.html', title='statistics', form=form, numBookings=numBookings, totalProfit = totalProfit, averagePricePerBooking = averagePricePerBooking)

# Allows the manager to view sales statistics
@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))
    role = session.get('role')
    if role != 4:
        flash("Manager Access Only")
        return redirect(url_for('home'))

    now = datetime.now()

    legend = 'Daily Bookings'
    legend1 ='Daily Revenue (£)'
    labels = []
    values = []
    values1 = []

    totalProfit = None
    averagePricePerBooking = None
    numBookings = None

    form = Statistics()

    if request.method == 'POST':
        timePeriod  = form.timeBox.data
        #timePeriods = ["1 Week", "1 Month", "1 Quarter", "1 Year"]
        if timePeriod == "1 Week":
            deltaTime = timedelta(weeks=1)
        elif timePeriod == "1 Month":
            deltaTime = timedelta(weeks = 4)
        elif timePeriod == "1 Quarter":
            deltaTime = timedelta(weeks= 12)
        elif timePeriod == "1 Year":
            deltaTime = timedelta(weeks=52)
        
        displayEnd = now - deltaTime
        location = models.Location.query.filter_by(LocationName = form.LocationBox.data).first()


        # bookings =  models.Booking.query.filter_by(locationID = location.id).filter_by(dateMade = displayEnd).all()
        bookings =  models.Booking.query.filter_by(locationID = location.id).all()
        if bookings:
            numBookings = 0
            totalProfit = 0
            dailyBookings = 0
            dailyRev = 0
            lastDay = 0
            first = 1

            for b in bookings:
                if b.dateMade > displayEnd:
                    if(first == 1):
                        lastDay = b.dateMade
                        dailyBookings = dailyBookings + 1
                        dailyRev = dailyRev + b.cost
                        first = 0
                    else:

                        if(b.dateMade.date() > (lastDay + timedelta(days=1)).date()):

                            while(lastDay.date() < b.dateMade.date()):
                                stringDate = lastDay.strftime('%m/%d/%Y')
                                labels.append(stringDate)
                                dailyBookings = 0
                                dailyRev = 0
                                values.append(dailyBookings)
                                values1.append(dailyRev)
                                lastDay = lastDay + timedelta(days=1)
                            
                            stringDate = b.dateMade.strftime('%m/%d/%Y')
                            labels.append(stringDate)
                            values.append(dailyBookings)
                            values1.append(dailyRev)
                            dailyBookings = 1
                            dailyRev = b.cost
                            lastDay = b.dateMade
                        
                        if(b.dateMade.date() == lastDay.date()):
                            dailyBookings = dailyBookings + 1
                            dailyRev = dailyRev + b.cost
                            lastDay = b.dateMade
                            


                        if(b.dateMade.date() == (lastDay + timedelta(days=1)).date()):
                            stringDate = b.dateMade.strftime('%m/%d/%Y')
                            labels.append(stringDate)
                            values.append(dailyBookings)
                            values1.append(dailyRev)
                            dailyBookings = 1
                            dailyRev = b.cost
                            lastDay = b.dateMade

                    totalProfit = totalProfit + b.cost
                    numBookings = numBookings + 1

            averagePricePerBooking = totalProfit / numBookings

    return render_template('statisticsChart.html', title='statistics', form=form, numBookings=numBookings, totalProfit = totalProfit, averagePricePerBooking = averagePricePerBooking,values=values, labels=labels, legend=legend, legend1 = legend1, values1=values1)
# Allows a user or employee to make a booking as a guest
@app.route('/guestBooking', methods=['GET', 'POST'])
def GuestBooking():
    form1 = GuestBookings()

    if request.method == 'POST':
        name = request.form.get('FirstName')
        surname = request.form.get('Surname')
        email = request.form.get('Email')
        cardnumber = request.form.get('CardNumber')
        expirydate = request.form.get('ExpiryDate')
        cvv = request.form.get('CVV')
        location = form1.LocationBox.data
        duration = form1.durationBox.data
        formattedDuration = 0
        priceBefore = 0
        ratesAll = models.Rates.query.all()
        rates = ratesAll[len(ratesAll)-1]

        if duration == "1hr":
            formattedDuration = timedelta(hours=1)
            priceBefore = rates.hourlyRate

        elif duration == "4hr":
            formattedDuration = timedelta(hours=4)
            priceBefore = rates.fourHourRate


        elif duration == "day":
            formattedDuration = timedelta(days=1)
            priceBefore = rates.dailyRate


        elif duration == "week":
            formattedDuration = timedelta(weeks=1)
            priceBefore = rates.weeklyRate

        
        locationObj=models.Location.query.filter_by(LocationName=location).first()
        
        guest = GuestBook(firstName=name, surName=surname, email=email, cardNum=cardnumber, expireDate=expirydate,
        cvv=cvv, locationID=locationObj.id, duration=datetime.now()+formattedDuration, booked=False, cost = priceBefore)
        db.session.add(guest)
        db.session.commit()
        flashString = "Charged £" + str(priceBefore)
        flash(flashString)
        print("guestBooking Successful")
        sendGuestPending(Date=datetime.now(), Duration=duration, Location=location, recipient=email)
        flash('Booking request has been sent to employee')
        return redirect('/')

    return render_template('guestBooking.html', form=form1)

# Allows employees to view guest bookings
@app.route('/viewGuestBookings', methods=['GET', 'POST'])
def viewGuestBooking():
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))
    role = session.get('role')
    if role < 3:
        flash("Employee Access Only")
        return redirect(url_for('home'))
    form = GuestBooked()
    guests = models.GuestBook.query.filter_by(booked=False).all()
    if request.method == 'POST':
        a = models.GuestBook.query.get(request.form.get('submitButton'))
        avScooters = models.Scooter.query.filter_by(available = True).filter_by(locationID = a.locationID).all()
        if len(avScooters) == 0 or avScooters == None:
            flash("No scooters currently avaiable at this location")
            return redirect('/viewGuestBookings')
        else:
            avScooters[0].available = False
            avScooters[0].currentBookingID = None
            avScooters[0].currentGuestBookingID = a.id
            a.scooterId = avScooters[0].id
            a.dateMade = datetime.now()
        locaction = models.Location.query.get( a.locationID)
        a.booked = True
        db.session.commit()
        sendEmail(a.scooterId, datetime.now(), a.duration, locaction.LocationName, a.email)
        return redirect('/viewGuestBookings')
    return render_template('viewGuestBookings.html', guests=guests, form=form)

# Resets all scooters
@app.route('/resetScooters', methods=['GET', 'POST'])
def resetScooters():
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))
    role = session.get('role')
    if role != 4:
        flash("Manager Access Only")
        return redirect(url_for('home'))
        
    allGenericBooking = []

    allBookings = models.Booking.query.filter_by(expired = False).all()
    allGuestBookings = models.GuestBook.query.filter_by(expired = False).filter_by(booked = True).all()

    allGenericBooking.append(allBookings)
    allGenericBooking.append(allGuestBookings)
    # expiredBokoings = []

    bookingCount = 0

    for bookingList in allGenericBooking:
        for booking in bookingList:
            if(booking.duration < datetime.now()):
                bookingCount = bookingCount + 1
                booking.expired = True
                scooter = models.Scooter.query.get(booking.scooterId)
                scooter.available = True
                scooter.currentBookingID = None
                scooter.currentGuestBookingID = None
                db.session.commit()
    

    if(len(allGenericBooking[0]) == 0 and len(allGenericBooking[1]) == 0):
        flash("No bookings to reset")
    else:
        if(bookingCount > 0):
            flash("Bookings reset")
        else:
            flash("No booking expired yet")


                
    return redirect(url_for('viewAllScooters'))

# @app.route("/chartTest")
# def chart():
#     legend = 'Daily Bookings'
#     legend1 ='Daily Revenue (£)'
#     labels = []
#     values = []
#     values1 = []

#     now = datetime.now()

#     deltaTime = timedelta(weeks=12)

#     displayEnd = now - deltaTime
#     location = models.Location.query.get(1)
#     bookings =  models.Booking.query.filter_by(locationID = location.id).all()

#     if bookings:
#         numBookings = 0
#         totalProfit = 0
#         dailyBookings = 0
#         dailyRev = 0
#         lastDay = 0
#         first = 1

#         for b in bookings:
#             if b.dateMade > displayEnd:
#                 if(first == 1):
#                     lastDay = b.dateMade
#                     dailyBookings = dailyBookings + 1
#                     dailyRev = dailyRev + b.cost
#                     first = 0
#                 else:

#                     if(b.dateMade.date() > (lastDay + timedelta(days=1)).date()):

#                         while(lastDay.date() < b.dateMade.date()):
#                             stringDate = lastDay.strftime('%m/%d/%Y')
#                             labels.append(stringDate)
#                             dailyBookings = 0
#                             dailyRev = 0
#                             values.append(dailyBookings)
#                             values1.append(dailyRev)
#                             lastDay = lastDay + timedelta(days=1)
                        
#                         stringDate = b.dateMade.strftime('%m/%d/%Y')
#                         labels.append(stringDate)
#                         values.append(dailyBookings)
#                         values1.append(dailyRev)
#                         dailyBookings = 1
#                         dailyRev = b.cost
#                         lastDay = b.dateMade
                    
#                     if(b.dateMade.date() == lastDay.date()):
#                         dailyBookings = dailyBookings + 1
#                         dailyRev = dailyRev + b.cost
#                         lastDay = b.dateMade
                        


#                     if(b.dateMade.date() == (lastDay + timedelta(days=1)).date()):
#                         stringDate = b.dateMade.strftime('%m/%d/%Y')
#                         labels.append(stringDate)
#                         values.append(dailyBookings)
#                         values1.append(dailyRev)
#                         dailyBookings = 1
#                         dailyRev = b.cost
#                         lastDay = b.dateMade

#                 totalProfit = totalProfit + b.cost
#                 numBookings = numBookings + 1




#     return render_template('chartTest.html', values=values, labels=labels, legend=legend, legend1 = legend1, values1=values1)