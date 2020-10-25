import logging
from flask import request
from flask.logging import default_handler
from flask_restful import Resource
from model import db, Epoch, EpochSchema


epochs_schema = EpochSchema(many=True)
epoch_schema = EpochSchema()


root = logging.getLogger("Epoch")
root.addHandler(default_handler)


class EpochResource(Resource):

    def get(self):
        epochs = Epoch.query.all()
        epochs = epochs_schema.dump(epochs).data
        return {'status': 'success', 'data': epochs}, 200

    def post(self):
        json_data = request.get_json(force=True)
        
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = epoch_schema.load(json_data)
        if errors:
            return errors, 422
        epoch = Epoch.query.filter_by(julian_date=data['julian_date']).first()
        if epoch:
            return {'message': 'Epoch already exists'}, 400
        epoch = Epoch(
            julian_date=json_data['julian_date'],
        )

        db.session.add(epoch)
        db.session.commit()

        result = epoch_schema.dump(epoch).data

        return { "status": 'success', 'data': result }, 201
