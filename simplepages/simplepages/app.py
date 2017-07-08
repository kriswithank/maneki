from flask import Flask, render_template
from requests import get

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index.html')


@app.route("/finances-test")
def finances_test():
    return get('http://api-finances').content


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
