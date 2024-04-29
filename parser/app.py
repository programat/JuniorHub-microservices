from flask import Flask, jsonify
from parser import parse_tinkoff_internships

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/internships')
def parse_vacancies():
    vacancies = parse_tinkoff_internships()
    return jsonify(vacancies)


if __name__ == '__main__':
    app.run(debug=True)
