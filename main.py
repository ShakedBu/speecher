from flask import Flask
app = Flask(__name__)


@app.route('/hi')
def print_hi():
    return 'Speecher'


if __name__ == '__main__':
    app.run()
