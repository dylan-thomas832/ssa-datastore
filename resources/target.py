import logging
from flask import request
from flask.logging import default_handler
from flask_restful import Resource
from model import db, Target, TargetSchema


targets_schema = TargetSchema(many=True)
target_schema = TargetSchema()


root = logging.getLogger("Target")
root.addHandler(default_handler)


class TargetResource(Resource):

    def get(self):
        targets = Target.query.all()
        targets = targets_schema.dump(targets).data
        return {'status': 'success', 'data': targets}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = target_schema.load(json_data)
        if errors:
            return errors, 422
        target = Target.query.filter_by(name=data['name']).first()
        if target:
            return {'message': 'Target already exists'}, 400
        target = Target(
            unique_id=json_data['unique_id'],
            name=json_data['name'],
        )

        db.session.add(target)
        db.session.commit()

        result = target_schema.dump(target).data

        return { "status": 'success', 'data': result }, 201
