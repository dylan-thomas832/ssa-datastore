from . import BaseResource
from ..model import db, Target, TargetSchema


class TargetResource(BaseResource):

    multi_schema = TargetSchema(many=True)
    single_schema = TargetSchema()
    model_type = Target

    def post(self):
        validated, data = self.validate()
        if not validated:
            return data[0], data[1]

        # Deserialize input
        target, json_data = data[0], data[1]
        # Ensure the entry doesn't already exist in DB
        target_in_db = Target.query.filter_by(
            unique_id=json_data['unique_id']
        ).first()
        if target_in_db:
            return {'message': 'Target already exists'}, 400

        # Commit valid POST to DB
        db.session.add(target)
        db.session.commit()

        # Return valid POST result
        result = self.single_schema.dump(target)
        return { "status": 'success', 'data': result }, 201
