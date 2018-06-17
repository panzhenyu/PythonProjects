from . import main
from .forms import Login, Order
from flask import render_template


@main.route('/', methods=['post', 'get'])
def index():
    form = Login()
    return render_template('main/index.html', form=form)

# lst = []
@main.route('test', methods=['post', 'get'])
def test():
    form = Login()
    # if form.is_submitted():
    #     lst.append(form.username.data)
    # str = ""
    # for name in lst:
    #     str += name
    return " "

@main.route("ajax")
def ajax():
    return render_template("main/Ajax.html")

@main.route("test.txt")
def t():
    return render_template("main/test.txt")

@main.errorhandler(404)
def do404(e):
    return "sorry, 404"

@main.route("orderSubmit", methods=["post", "get"])
def orderSubmit():
    orderForm = Order()
    if orderForm.is_submitted():
        orderInfo = open("app/templates/main/test.txt", 'a')
        orderInfo.write(orderForm.__str__() + "\n")
        orderInfo.close()
    return render_template("main/orderSubmit.html", orderForm=orderForm)
