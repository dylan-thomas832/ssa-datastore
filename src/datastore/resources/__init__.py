from collections import namedtuple
from flask import current_app as app, request
from flask_restful import Resource
from marshmallow import ValidationError


class BaseResource(Resource):

    multi_schema = None
    single_schema = None
    model_type = None

    # 
    Valid = namedtuple('Valid', ('object', 'json'))
    InValid = namedtuple('Invalid', ('data', 'status'))

    def get(self):
        entries = self.model_type.query.all()
        app.logger.info(
            "Get request returned {0} {1} entries".format(
                len(entries),
                self.model_type.__tablename__
            )
        )
        entries = self.multi_schema.dump(entries)
        return {'status': 'success', 'data': entries}, 200

    def validate(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return False, ({'message': 'No input data provided'}, 400)

        # Validate input
        try:
            data = self.single_schema.load(json_data)
        except ValidationError as error:
            app.logger.error("Invalid data: {0}".format(error.messages))
            app.logger.error("Valid data: {0}".format(error.valid_data))
            return False, ({'message': error.messages}, 422)

        return True, (data, json_data)
