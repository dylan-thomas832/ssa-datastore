from flask_restful import Resource


class Sensor(Resource):

    def get(self):
        return {"message": "Hello, World! - Sensor"}

    def post(self):
        return {"message": "Hello, World! - Sensor"}
