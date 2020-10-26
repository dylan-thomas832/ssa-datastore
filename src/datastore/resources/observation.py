from . import BaseResource
from ..model import db, Observation, ObservationSchema


class ObservationResource(BaseResource):

    multi_schema = ObservationSchema(many=True)
    single_schema = ObservationSchema()
    model_type = Observation

    def post(self):
        validated, data = self.validate()
        if not validated:
            return data[0], data[1]

        # Deserialize input
        observation, json_data = data[0], data[1]
        # Ensure the entry doesn't already exist in DB
        observation_in_db = Observation.query.filter_by(
            julian_date=json_data['julian_date'],
            target_id=json_data['target_id'],
            sensor_id=json_data['sensor_id'],
        ).first()
        if observation_in_db:
            return {'message': 'Observation already exists'}, 400

        # Commit valid POST to DB
        db.session.add(observation)
        db.session.commit()

        # Return valid POST result
        result = self.single_schema.dump(observation)
        return { "status": 'success', 'data': result }, 201
