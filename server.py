from views.general import *
from views.login import *
from views.template_utils import *
from app import app


if __name__ == '__main__':
    app.run(debug=True, port=9000)