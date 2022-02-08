from app import app


@app.route('/', methods=['POST', 'GET'])
def index():
    return "Hello world"