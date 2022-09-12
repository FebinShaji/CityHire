import smtplib

def sendEmail(scooterId, Date, Duration, Location, recipient):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login('cityhirebookings@gmail.com', 'CityHire123')

        subject = "Booking Notification"
        body = f"""Thank you for travel with CityHire, your booking is:
Scooter {scooterId} on {Date} for {Duration} at {Location}"""

        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail('cityhirebookings@gmail.com', recipient, msg)

# def sendGuestRejected(scooterId, Date, Duration, Location, recipient):
#     with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
#         smtp.ehlo()
#         smtp.starttls()
#         smtp.ehlo()

#         smtp.login('cityhirebookings@gmail.com', 'CityHire12345')

#         subject = "Booking Notification"
#         body = f"""Thank you for booking with CityHire, your booking
# of {scooterId} on {Date} for {Duration} at {Location} has unfortunatley been rejected."""

#         msg = f'Subject: {subject}\n\n{body}'

#         smtp.sendmail('cityhirebookings@gmail.com', recipient, msg)

def sendGuestPending(Date, Duration, Location, recipient):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login('cityhirebookings@gmail.com', 'CityHire123')

        subject = "Booking Notification"
        body = f"""Thank you for booking with CityHire, your booking
        for {Date} for {Duration} at {Location} is currently being reviewed"""

        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail('cityhirebookings@gmail.com', recipient, msg)

def sendIssuePending(scooterId, recipient):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login('cityhirebookings@gmail.com', 'CityHire123')

        subject = "Isusse Confirmation"
        body = f"""Thank you for your feedback, your issue with sooter {scooterId} is being reviewed."""

        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail('cityhirebookings@gmail.com', recipient, msg)

def sendIssueComplete(scooterId, recipient):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login('cityhirebookings@gmail.com', 'CityHire123')

        subject = "Issue Rectified"
        body = f"""Thank you for your feedback, the issue with sooter {scooterId} has been rectified."""


        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail('cityhirebookings@gmail.com', recipient, msg)

# sendEmail(1,'Monday', 60, 'Leeds', 'schofield.tom@hotmail.com')