from flask import Flask
from marshmallow import Schema, fields, validate, post_load
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()


class Target(db.Model):

    __tablename__ = "target"
    # id = db.Column(db.Integer, primary_key=True)

    # NORAD Catalog Number or Simulation ID
    unique_id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)

    ## Describes satellite associated with NORAD number
    # Corresponds to a valid Space Track "SATNAME" field.
    name = db.Column(db.String(128), unique=True, nullable=False)

    # Relationships to `Ephemeris` & `Observation` tables
    ephemerides = db.relationship(
        'Ephemeris',
        backref=db.backref('target', lazy='joined'),
        lazy='select'
    )
    observations = db.relationship(
        'Observation',
        backref=db.backref('target', lazy='joined'),
        lazy='select'
    )

    def __init__(self, unique_id, name):
        self.unique_id = unique_id
        self.name = name


class Sensor(db.Model):

    __tablename__ = "sensor"
    # id = db.Column(db.Integer, primary_key=True)

    # NORAD Catalog Number or Simulation ID
    unique_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    # Unique sensor name, SATCAT name if satellite sensor
    name = db.Column(db.String(128), unique=True, nullable=False)

    # Type of the observing sensor (Optical, Radar, AdvRadar)
    sensor_type = db.Column(db.String(128), nullable=False)

    # Relationships to `Observation` table
    observations = db.relationship(
        'Observation',
        backref=db.backref('sensor', lazy='joined'),
        lazy='select'
    )

    def __init__(self, unique_id, name, sensor_type):
        self.unique_id = unique_id
        self.name = name
        self.sensor_type = sensor_type


class Ephemeris(db.Model):

    __tablename__ = 'ephemeris'
    id = db.Column(db.Integer, primary_key=True)

    # FK's to `Target`
    target_id = db.Column(db.Integer, db.ForeignKey('target.unique_id'), nullable=False)
    # target_name = db.Column(db.String(128), db.ForeignKey('target.name'), nullable=False)

    ## Cartesian x/y/z-coordinate for inertial satellite location in ECI frame in kilometers
    pos_x_km = db.Column(db.Float, nullable=False)
    pos_y_km = db.Column(db.Float, nullable=False)
    pos_z_km = db.Column(db.Float, nullable=False)

    ## Cartesian x/y/z-coordinate for inertial satellite velocity in ECI frame in kilometers per second
    vel_x_km_p_sec = db.Column(db.Float, nullable=False)
    vel_y_km_p_sec = db.Column(db.Float, nullable=False)
    vel_z_km_p_sec = db.Column(db.Float, nullable=False)

    # FKs to `Epoch` Table
    julian_date = db.Column(db.Float, db.ForeignKey('epoch.julian_date'), nullable=False)
    # timestamp = db.Column(db.DateTime, db.ForeignKey('epoch.timestamp'), nullable=False)

    def __init__(self, julian_date, target_id, eci):
        self.julian_date = julian_date
        self.target_id = target_id
        self.pos_x_km = eci[0]
        self.pos_y_km = eci[1]
        self.pos_z_km = eci[2]
        self.vel_x_km_p_sec = eci[3]
        self.vel_y_km_p_sec = eci[4]
        self.vel_z_km_p_sec = eci[5]


class Observation(db.Model):

    __tablename__ = 'observation'
    id = db.Column(db.Integer, primary_key=True)

    # Observed azimuth of target from observing sensor in radians
    azimuth_rad = db.Column(db.Float)

    # Observed elevation of target from observing sensor in radians
    elevation_rad = db.Column(db.Float)

    # Observed range of target from observing sensor in kilometers
    range_km = db.Column(db.Float, nullable=True)

    # Observed range rate of target from observing sensor in kilometers per second
    range_rate_km_p_sec = db.Column(db.Float, nullable=True)

    # FK's to `Sensor` Table
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.unique_id'), nullable=False)
    # sensor_name = db.Column(db.String(128), db.ForeignKey('sensor.name'), nullable=False)

    # FK's to `Target` Table
    target_id = db.Column(db.Integer, db.ForeignKey('target.unique_id'), nullable=False)
    # target_name = db.Column(db.String(128), db.ForeignKey('target.name'), nullable=False)

    # FKs to `Epoch` Table
    julian_date = db.Column(db.Float, db.ForeignKey('epoch.julian_date'), nullable=False)
    # timestamp = db.Column(db.DateTime(), db.ForeignKey('epoch.timestamp'), nullable=False)

    def __init__(self, julian_date, sensor_id, target_id, **measurements):
        self.julian_date = julian_date
        self.sensor_id = sensor_id
        self.target_id = target_id
        self.azimuth_rad = measurements.get('azimuth')
        self.elevation_rad = measurements.get('elevation')
        self.range_km = measurements.get('range', None)
        self.range_rate_km_p_sec = measurements.get('range_rate', None)


class Epoch(db.Model):

    __tablename__ = 'epoch'
    id = db.Column(db.Integer, primary_key=True)

    ## Defines the epoch associated with the given data
    # i.e. when this data is provided
    julian_date = db.Column(db.Float, unique=True, nullable=False)  # primary_key=True, index=True

    # Human readable version of the `julian_date`
    # timestamp = db.Column(db.DateTime, unique=True, nullable=False)

    # Relationships to `Ephemeris` & `Observation` tables
    ephemerides = db.relationship(
        'Ephemeris',
        backref=db.backref('epoch', lazy='joined'),
        lazy='select'
    )
    observations = db.relationship(
        'Observation',
        backref=db.backref('epoch', lazy='joined'),
        lazy='select'
    )

    def __init__(self, julian_date):
        self.julian_date = julian_date
        # self.timestamp = timestamp


class TargetSchema(ma.Schema):

    # id = fields.Integer()
    unique_id = fields.Integer(required=True)
    name = fields.String(required=True)

    @post_load
    def makeTarget(self, data, **kwargs):
        return Target(**data)


class SensorSchema(ma.Schema):

    # id = fields.Integer()
    unique_id = fields.Integer(required=True)
    name = fields.String(required=True)
    sensor_type = fields.String(required=True)

    @post_load
    def makeSensor(self, data, **kwargs):
        return Sensor(**data)


class EphemerisSchema(ma.Schema):

    id = fields.Integer()
    pos_x_km = fields.Float(required=True)
    pos_y_km = fields.Float(required=True)
    pos_z_km = fields.Float(required=True)
    vel_x_km_p_sec = fields.Float(required=True)
    vel_y_km_p_sec = fields.Float(required=True)
    vel_z_km_p_sec = fields.Float(required=True)
    # FK's to `Target`
    target_id = fields.Integer(required=True)
    # FKs to `Epoch` Table
    julian_date = fields.Integer(required=True)
    # timestamp = fields.DateTime(required=True)

    @post_load
    def makeEphemeris(self, data, **kwargs):
        return Ephemeris(**data)


class ObservationSchema(ma.Schema):

    id = fields.Integer()
    azimuth_rad = fields.Float(required=True)
    elevation_rad = fields.Float(required=True)
    range_km = fields.Float(required=False)
    range_rate_km_p_sec = fields.Float(required=False)
    # FK's to `Sensor` Table
    sensor_id = fields.Integer(required=True)
    # FK's to `Target` Table
    target_id = fields.Integer(required=True)
    # FKs to `Epoch` Table
    julian_date = fields.Float(required=True)
    # timestamp = fields.DateTime(required=True)

    @post_load
    def makeObservation(self, data, **kwargs):
        return Observation(**data)


class EpochSchema(ma.Schema):

    id = fields.Integer()
    julian_date = fields.Float(required=True)
    # timestamp = fields.DateTime(required=True)

    @post_load
    def makeEpoch(self, data, **kwargs):
        return Epoch(**data)
