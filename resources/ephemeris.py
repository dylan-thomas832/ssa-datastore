from flask import request
from flask_restful import Resource
from model import db, Ephemeris, EphemerisSchema


ephemerides_schema = EphemerisSchema(many=True)
ephemeris_schema = EphemerisSchema()


class EphemerisResource(Resource):

    def get(self):
        ephems = Ephemeris.query.all()
        ephems = ephemerides_schema.dump(ephems).data
        return {'status': 'success', 'data': ephems}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = ephemeris_schema.load(json_data)
        if errors:
            return errors, 422
        ephemeris = Ephemeris.query.filter_by(id=data['id']).first()
        if ephemeris:
            return {'message': 'Ephemeris already exists'}, 400
        ephemeris = Ephemeris(
            eci=json_data['eci']
        )

        db.session.add(ephemeris)
        db.session.commit()

        result = ephemeris_schema.dump(ephemeris).data

        return { "status": 'success', 'data': result }, 201
