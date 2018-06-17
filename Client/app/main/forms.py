from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateTimeField, BooleanField

class Login(FlaskForm):
    username = StringField()
    password = PasswordField()
    submit = SubmitField()

class Order(FlaskForm):
    serial_number = IntegerField()
    restaurant_id = IntegerField()
    user_id = IntegerField()
    table_id = IntegerField()
    time = DateTimeField()
    foods = StringField()
    state = BooleanField()
    other_info = StringField()
    submit = SubmitField()

    def __str__(self):
        val = ""
        val += str(self.serial_number.data) + " "\
               + str(self.restaurant_id.data) + " "\
               + str(self.user_id.data) + " "\
               + str(self.table_id.data) + " "\
               + str(self.time.data) + " "\
               + str(self.foods.data) + " "\
               + str(self.state.data) + " "\
               + str(self.other_info.data)
        return val