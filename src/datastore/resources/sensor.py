from . import BaseResource
from ..model import db, Sensor, SensorSchema


class SensorResource(BaseResource):

    multi_schema = SensorSchema(many=True)
    single_schema = SensorSchema()
    model_type = Sensor

    def post(self):
        validated, data = self.validate()
        if not validated:
            return data[0], data[1]

        # Deserialize input
        sensor, json_data = data[0], data[1]
        # Ensure the entry doesn't already exist in DB
        sensor_in_db = Sensor.query.filter_by(
            unique_id=json_data['unique_id']
        ).first()
        if sensor_in_db:
            return {'message': 'Sensor already exists'}, 400

        # Commit valid POST to DB
        db.session.add(sensor)
        db.session.commit()

        # Return valid POST result
        result = self.single_schema.dump(sensor)
        return { "status": 'success', 'data': result }, 201
