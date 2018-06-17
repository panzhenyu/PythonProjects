from . import rstdb

class OrderForm(rstdb.Model):
    __tablename__ = "order_form"
    serial_number = rstdb.Column(rstdb.Integer, primary_key=True)
    restaurant_id = rstdb.Column(rstdb.Integer)
    user_id = rstdb.Column(rstdb.Integer)
    table_id = rstdb.Column(rstdb.Integer)
    time = rstdb.Column(rstdb.DateTime)
    state = rstdb.Column(rstdb.Boolean)


class Kitchen(rstdb.Model):
    __tablename__ = 'kitchen'
    id = rstdb.Column(rstdb.Integer, primary_key=True)
    tel = rstdb.Column(rstdb.String(24), primary_key=False, unique=True)
