from flask import Flask
app = Flask(__name__)


@app.route('/')
def default():
    return 'Welcome to Speecher'


@app.route('/speech/<query>', methods=['GET', 'POST'])
def speech(query):
    if Flask.method == 'GET':
        return 'get speech'
    else:
        return 'create new speech'


@app.route('/group/<query>', methods=['GET', 'POST'])
def group(query):
    if Flask.method == 'GET':
        return 'get speech'
    else:
        return 'create new speech'


@app.route('/phrase/<query>', methods=['GET', 'POST'])
def phrase(query):
    if Flask.method == 'GET':
        return 'get speech'
    else:
        return 'create new speech'


if __name__ == '__main__':
    app.run()
