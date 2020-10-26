from . import BaseResource
from ..model import db, Ephemeris, EphemerisSchema


class EphemerisResource(BaseResource):

    multi_schema = EphemerisSchema(many=True)
    single_schema = EphemerisSchema()
    model_type = Ephemeris

    def post(self):
        validated, data = self.validate()
        if not validated:
            return data[0], data[1]

        # Deserialize input
        ephemeris, json_data = data[0], data[1]
        # Ensure the entry doesn't already exist in DB
        ephemeris_in_db = Ephemeris.query.filter_by(
            julian_date=json_data['julian_date'],
            target_id=json_data['target_id']
        ).first()
        if ephemeris_in_db:
            return {'message': 'Ephemeris already exists'}, 400

        # Commit valid POST to DB
        db.session.add(ephemeris)
        db.session.commit()

        # Return valid POST result
        result = self.single_schema.dump(ephemeris).data
        return { "status": 'success', 'data': result }, 201


