from flask_wtf import Form
from wtforms import IntegerField
from wtforms import TextField, TextAreaField
from wtforms import DateTimeField
from wtforms import BooleanField
from wtforms import SelectField
from wtforms import PasswordField
from wtforms.validators import DataRequired
from wtforms.validators import length

"""
class BookingForm(Form):
    types = ["sit", "stand"]
    type = SelectField(u'Seeting Type', choices = types, validators = [DataRequired()])
    Ticket = IntegerField('Ticket Number', validators=[DataRequired()])
"""
class Login(Form):
    Username = TextField('Username', validators=[DataRequired(), length(max=20)])
    Password = TextField('Password', validators=[DataRequired(), length(max=20)])
    Remember = BooleanField('Remember')

class Register(Form):
    FirstName = TextField('FirstName', validators=[DataRequired(), length(max=30)])
    Surname = TextField('Surname', validators=[DataRequired(), length(max=30)])
    Email = TextField('Email', validators=[DataRequired(), length(max=20)])
    Number = IntegerField('Number', validators=[DataRequired(), length(max=11)])
    Username = TextField('Username', validators=[DataRequired(), length(max=20)])
    Password = PasswordField('Password', validators=[DataRequired(), length(max=20)])
    Confirm_Password = PasswordField('Confirm_Password', validators=[DataRequired(), length(max=20)])
    userTypes = ["Normal", "Student", "Over 60"]
    Type = SelectField('Type', choices = userTypes, validators = [DataRequired()])

class CreateIssue(Form):
    ScooterID = TextField('ScooterID', validators=[DataRequired(), length(max=5)])
    Complaint = TextAreaField('Complaint', validators=[DataRequired()])

class ChangePassword(Form):
    NewPassword = PasswordField('NewPassword', validators=[DataRequired(), length(max=20)])
    Confirm_NewPassword = PasswordField('Confirm_NewPassword', validators=[DataRequired(), length(max=20)])
    
class AddCardDetails(Form):
    CardNumber = PasswordField('CardNumber', validators=[DataRequired(), length(max=20)])
    ExpiryDate = PasswordField('ExpiryDate', validators=[DataRequired(), length(max=20)])
    CVV = PasswordField('CVV', validators=[DataRequired(), length(max=20)])

class LocationSelect(Form):
    location = ["Trinity centre", "Train station", "Merrion centre", "LGI hospital", "UoL Edge sports centre"]
    LocationBox = SelectField('Loaction', choices = location, validators = [DataRequired()])

class ExtendBooking(Form):
    durations = ["1hr", "4hrs", "day", "week"]
    durationBox = SelectField('Duration', choices = durations, validators = [DataRequired()])
    DiscountCode = TextField('Discount Code', validators=[length(max=20)])

class ScooterAvailability(Form):
    Complete = BooleanField('Complete')

class CreateBooking(Form):
    durations = ["1hr", "4hrs", "day", "week"]
    durationBox = SelectField('Duration', choices = durations, validators = [DataRequired()])
    CardNumber = PasswordField('CardNumber', validators=[length(max=20)])
    ExpiryDate = PasswordField('ExpiryDate', validators=[length(max=20)])
    CVV = PasswordField('CVV', validators=[length(max=20)])
    useKnown = BooleanField()

class ConfigureScooters(Form):
    HourlyRate = IntegerField('HourlyRate', validators=[DataRequired(), length(max=10)])
    FourHourRate = IntegerField('FourHourRate', validators=[DataRequired(), length(max=10)])
    DailyRate = IntegerField('DailyRate', validators=[DataRequired(), length(max=10)])
    WeeklyRate = IntegerField('WeeklyRate', validators=[DataRequired(), length(max=10)])

class Statistics(Form):
    timePeriods = ["1 Week", "1 Month", "1 Quarter", "1 Year"]
    timeBox = SelectField('timePeriods', choices = timePeriods, validators = [DataRequired()])
    location = ["Trinity centre", "Train station", "Merrion centre", "LGI hospital", "UoL Edge sports centre"]
    LocationBox = SelectField('Loaction', choices = location, validators = [DataRequired()])

class GuestBookings(Form):
    FirstName = TextField('FirstName', validators=[DataRequired(), length(max=30)])
    Surname = TextField('Surname', validators=[DataRequired(), length(max=30)])
    Email = TextField('Email', validators=[DataRequired(), length(max=20)])
    CardNumber = PasswordField('CardNumber', validators=[DataRequired(), length(max=20)])
    ExpiryDate = PasswordField('ExpiryDate', validators=[DataRequired(), length(max=20)])
    CVV = PasswordField('CVV', validators=[DataRequired(), length(max=20)])
    location = ["Trinity centre", "Train station", "Merrion centre", "LGI hospital", "UoL Edge sports centre"]
    LocationBox = SelectField('Loaction', choices = location, validators = [DataRequired()])
    durations = ["1hr", "4hrs", "day", "week"]
    durationBox = SelectField('Duration', choices = durations, validators = [DataRequired()])

class GuestBooked(Form):
    Complete = BooleanField('Complete')