from flask import Flask, render_template, make_response, jsonify

# from flask_cors import CORS
# from flasgger import Swagger
# from flasgger.utils import swag_from


app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route("/users/<name>", strict_slashes=False)
def users(name):
    return "Welcome to Stocklerts {}".format(name)


if __name__ == '__main__':
    app.run(debug=True)
