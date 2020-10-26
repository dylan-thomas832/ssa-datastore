from . import BaseResource
from ..model import db, Epoch, EpochSchema


class EpochResource(BaseResource):

    multi_schema = EpochSchema(many=True)
    single_schema = EpochSchema()
    model_type = Epoch

    def post(self):
        validated, data = self.validate()
        if not validated:
            return data[0], data[1]

        # Deserialize input
        epoch, json_data = data[0], data[1]
        # Ensure the entry doesn't already exist in DB
        epoch_in_db = Epoch.query.filter_by(
            julian_date=json_data['julian_date']
        ).first()
        if epoch_in_db:
            return {'message': 'Epoch already exists'}, 400

        # Commit valid POST to DB
        db.session.add(epoch)
        db.session.commit()

        # Return valid POST result
        result = self.single_schema.dump(epoch)
        return { "status": 'success', 'data': result }, 201
