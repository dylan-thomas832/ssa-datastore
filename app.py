from flask import Blueprint
from flask_restful import Api
from resources.ephemeris import EphemerisResource
from resources.epoch import EpochResource
from resources.observation import Observation
from resources.sensor import Sensor
from resources.target import TargetResource


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(EphemerisResource, '/ephemeris')
api.add_resource(EpochResource, '/epoch')
api.add_resource(Observation, '/observation')
api.add_resource(Sensor, '/sensor')
api.add_resource(TargetResource, '/target')
