from flask_restful import Resource


class Observation(Resource):

    def get(self):
        return {"message": "Hello, World! - Observation"}

    def post(self):
        return {"message": "Hello, World! - Observation"}
