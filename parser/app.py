from flask import Flask, jsonify, Response, json
from parser import parse_tinkoff_internships

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/internships')
def get_internships():
    internships_data = parse_tinkoff_internships()
    if internships_data:
        response = Response(json.dumps(internships_data, ensure_ascii=False),
                            content_type='application/json; charset=utf-8')
        return response
    else:
        return jsonify({"error": "Data not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
