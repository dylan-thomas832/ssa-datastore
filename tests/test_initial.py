from flask import json, url_for
import requests


class TestEndPoints:

    base_url = "http://127.0.0.1:5000/api"
    end_points = (
        "ephemeris",
    )

    def testGetRequest(self, client):
        response = client.get(url_for('api.epochresource'))
        assert response.status_code == 200

    def testEpochPostRequest(self, client):
        epoch = {
            "julian_date": 2459144.1
        }
        response = client.post(url_for('api.epochresource'), data=json.dumps(epoch))
        assert response.status_code == 201

    def testPostRequest(self, client):
        tgt = {
            "unique_id": 11111,
            "name": "TargetSat"
        }
        response = client.post(url_for('api.targetresource'), data=json.dumps(tgt))
        assert response.status_code == 201
