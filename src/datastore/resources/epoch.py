from flask import current_app as app, request
from flask_restful import Resource
from marshmallow import ValidationError
from ..model import db, Epoch, EpochSchema


epochs_schema = EpochSchema(many=True)
epoch_schema = EpochSchema()


class EpochResource(Resource):

    def get(self):
        epochs = Epoch.query.all()
        app.logger.info("Get request returned {0} results".format(len(epochs)))
        epochs = epochs_schema.dump(epochs)
        return {'status': 'success', 'data': epochs}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        # Validate and deserialize input
        try:
            data = epoch_schema.load(json_data)
        except ValidationError as error:
            app.logger.error("Invalid data: {0}".format(error.messages))
            app.logger.error("Valid data: {0}".format(error.valid_data))
            return error.messages, 422

        # Ensure the entry doesn't already exist in DB
        epoch = Epoch.query.filter_by(julian_date=data['julian_date']).first()
        if epoch:
            return {'message': 'Epoch already exists'}, 400
        epoch = Epoch(
            julian_date=json_data['julian_date'],
        )

        # Commit valid POST to DB
        db.session.add(epoch)
        db.session.commit()

        # Return valid POST result
        result = epoch_schema.dump(epoch)
        return { "status": 'success', 'data': result }, 201
