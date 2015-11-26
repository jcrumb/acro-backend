from flask import Flask
from flask_restful import Api

from resources.root import RootResource

app = Flask(__name__)
api = Api(app)

api.add_resource(RootResource, '/')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')