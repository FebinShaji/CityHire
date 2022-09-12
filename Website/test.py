import unittest
from app import app, views, models
import json
import flask_testing
import databaseCreation as dc


class LoginTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.testing = True
        self.client = app.test_client()


    def tearDown(self):
        pass

    def test_correct_username_password(self):
        response = app.test_client().post('/login', data={
            "Username": "tom",
            "Password": "123"
            })
        # print(views.user)
        assert views.result["message"] == "Login successful"
        assert views.result["code"] == 0

    def test_invaild_username(self):
        response = app.test_client().post('/login', data={
            "Username": "tommm",
            "Password": "123"
            })
        assert views.result["message"] == "Incorrect username or password entered"
        assert views.result["code"] == -1

    def test_invaild_password(self):
        response = app.test_client().post('/login', data={
            "Username": "tom",
            "Password": "111"
            })
        assert views.result["message"] == "Incorrect username or password entered"
        assert views.result["code"] == -1


class RegisterTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_successful_register(self): 
        response = app.test_client().post('/register', data={
            "FirstName" : "Febin",
            "Surname" : "Shaji",
            "Email" : "febin@gmail.com",
            "Number" : "07456345678",
            "Username" : "Febin123",
            "Password" : "Depr33",
            "Confirm_Password" : "Depr33"
        })
        assert views.result["message"] == "Login successful"
        # assert views.result["message"] == "Account with this email address already exists"
        # assert views.result["code"] == -1
        assert views.result["code"] == 0

    def test_exist_email_or_username(self): # acctally test_successful_register 
        response = app.test_client().post('/register', data={
            "FirstName": "Febin",
            "Surname": "Shaji",
            "Email": "febin@gmail.com",
            "Number": "07456345678",
            "Username": "Febin123",
            "Password": "Depr33",
            "Confirm_Password": "Depr33"
        })
        assert views.result["message"] == "Account with this email address already exists"
        # assert views.result["message"] == "Login successful"
        assert views.result["code"] == -1
        # assert views.result["code"] == 0


    # def test_incorrect_format_email(self):
    #     response = app.test_client().post('/register', data={
    #         "firstName" : "Febin",
    #         "surName" : "Shaji",
    #         "email" : "febin@gmail.com",
    #         "mobileNum" : "07456345678",
    #         "username" : "Febin123",
    #         "password" : "Depr33",
    #         "confirm_password" : "Depr33"
    #     })
    #     assert response.status_code == 200
    #     assert "User submits an incorrect format for an email" in response.data
    #
    # def test_incorrect_number(self):
    #     response = app.test_client().post('/register', data={
    #         "firstName" : "Febin",
    #         "surName" : "Shaji",
    #         "email" : "febin@gmail.com",
    #         "mobileNum" : "34testincorrect",
    #         "username" : "Febin123",
    #         "password" : "Depr33",
    #         "confirm_password" : "Depr33"
    #     })
    #     assert response.status_code == 200
    #     assert "User submits an incorrect format for a phone number" in response.data
    #
    # def test_empty_fields(self):
    #     response = app.test_client().post('/register', data={})
    #     assert response.status_code == 200
    #     assert "User submits empty fields" in response.data


class ChangePasswordTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_successful_change_password(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 1
                lSess['role'] = 2
            response = lTestClient.post('/changepassword', data={
                "NewPassword": "456",
                "Confirm_NewPassword": "456"
            })
            response = lTestClient.post('/changepassword', data={
                "NewPassword": "123",
                "Confirm_NewPassword": "123"
            })
            assert views.result["message"] == "Password changed successfully!"
            assert views.result["code"] == 0

    # def test_empty_fields(self):
    #     response = app.test_client().post('/dashboard', data={
    #         "NewPassword" : "",
    #         "Confirm_NewPassword" : ""
    #     })
    #     assert response.status_code == 200
    #     assert "User submits empty fields" in response.data

    # def test_current_password(self):
    #     response = app.test_client().post('/dashboard', data={
    #         "NewPassword" : "Depr33",
    #         "Confirm_NewPassword" : "Depr33"
    #     })
    #     assert response.status_code == 200
    #     assert "Users submits their current password" in response.data

    def test_different_password(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 1
                lSess['role'] = 2
            response = lTestClient.post('/changepassword', data={
                "NewPassword": "123",
                "Confirm_NewPassword": "456"
            })
            assert views.result["message"] == "The passwords don't match!"
            assert views.result["code"] == -1


class AddCardDetailsTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_successful_add_card_details(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 1
                lSess['role'] = 2
            response = lTestClient.post('/dashboard', data={
                "CardNumber": "1234567890123456",
                "ExpiryDate": "07/23",
                "CVV": "123"
            })
            assert views.result["message"] == "Card details saved successfully!"
            assert views.result["code"] == 0


class BookingTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_successful_booking(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 1
                lSess['role'] = 2
                lSess['scooter'] = 100
                # views.duration = "1hr"
            response = lTestClient.post('/book/100', data={
                "durationBox" : "1hr",
                "CardNumber": "1234567890123456",
                "ExpiryDate": "07/23",
                "CVV": "123"
            })
            assert views.result["message"] == "Booking successful!"
            assert views.result["code"] == 0


class ExtendBookingTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.testing = True
        self.client = app.test_client()
        booking = models.Booking.query.get(1)
        if booking == None:
            dc.creatTestBooking()


    def tearDown(self):
        pass

    def test_extend_booking(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 1
                lSess['role'] = 2
                lSess['scooter'] = 100
                # views.duration = "1hr"
            response = lTestClient.post('/extendBooking/2', data={
                "durationBox" : "1hr"
            })
            assert views.result["message"] == "Booking Extended"
            assert views.result["code"] == 0


class CancelBookingTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.testing = True
        self.client = app.test_client()
        booking = models.Booking.query.get(1)
        if booking == None:
            dc.creatTestBooking()

    def tearDown(self):
        pass

    def test_cancel_booking(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 1
                lSess['role'] = 2
                lSess['scooter'] = 100
                # views.duration = "1hr"
            response = lTestClient.post('/cancelBooking/1')
            assert views.result["message"] == "Booking Deleted"
            assert views.result["code"] == 0


class CreateIssueTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.testing = True
        self.client = app.test_client()


    def tearDown(self):
        pass

    def test_create_issue(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 1
                lSess['role'] = 2
                lSess['scooter'] = 100
                # views.duration = "1hr"
            response = lTestClient.post('/createissue', data={
                "ScooterID" : "100",
                "Complaint": "Testing Complaint system"
            })
            assert views.result["message"] == "Successfully created issue."
            assert views.result["code"] == 0


class CreateIssueTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_create_issue(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 1
                lSess['role'] = 2
                lSess['scooter'] = 100
                # views.duration = "1hr"
            response = lTestClient.post('/createissue', data={
                "ScooterID" : "100",
                "Complaint": "Testing Complaint system"
            })
            assert views.result["message"] == "Successfully created issue."
            assert views.result["code"] == 0


class ChangeStatusTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_change_status(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 3
                lSess['role'] = 4
                lSess['scooter'] = 100
                # views.duration = "1hr"
            response = lTestClient.post('/viewAllScooters', data={
                "ScooterID" : "100",
                "submitButton" : "100"
            })
            # print(views.a.available)
            assert views.result["message"] == "Scooter Updated"
            assert views.result["code"] == 0


class IncreasePrioTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_increase_prio(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 3
                lSess['role'] = 4

                lSess['scooter'] = 100
                # views.duration = "1hr"
            response = lTestClient.post('/increasePrio/1')
            # print(views.a.available)
            assert views.result["message"] == "Issue increasePrio Successful"
            assert views.result["code"] == 0


if __name__ == '__main__':
    dc.FillDBForTest()
    unittest.TestLoader.sortTestMethodsUsing = lambda *args: -1
    try:
        unittest.main()
    except:
        print("tests complete")
    dc.FillDB()