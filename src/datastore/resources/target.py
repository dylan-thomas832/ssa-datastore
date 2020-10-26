from flask import current_app as app, request
from flask_restful import Resource
from marshmallow import ValidationError
from ..model import db, Target, TargetSchema


targets_schema = TargetSchema(many=True)
target_schema = TargetSchema()


class TargetResource(Resource):

    def get(self):
        targets = Target.query.all()
        app.logger.info("Get request returned {0} results".format(len(targets)))
        targets = targets_schema.dump(targets)
        return {'status': 'success', 'data': targets}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        # Validate and deserialize input
        try:
            data = target_schema.load(json_data)
        except ValidationError as error:
            app.logger.error("Invalid data: {0}".format(error.messages))
            app.logger.error("Valid data: {0}".format(error.valid_data))
            return error.messages, 422

        # Ensure the entry doesn't already exist in DB
        target = Target.query.filter_by(name=data['name']).first()
        if target:
            return {'message': 'Target already exists'}, 400
        target = Target(
            unique_id=json_data['unique_id'],
            name=json_data['name'],
        )

        # Commit valid POST to DB
        db.session.add(target)
        db.session.commit()

        # Return valid POST result
        result = target_schema.dump(target)
        return { "status": 'success', 'data': result }, 201
