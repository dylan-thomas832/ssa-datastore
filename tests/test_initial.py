import requests
import json


class TestEndPoints:

    base_url = "http://127.0.0.1:5000/api"
    end_points = (
        "ephemeris",
    )

    def testGetRequest(self):
        response = requests.get("http://127.0.0.1:5000/api/epoch")
        assert response.status_code == 200

    def testEpochPostRequest(self):
        epoch = {
            "julian_date": 2459144.0
        }
        response = requests.post("http://127.0.0.1:5000/api/epoch", data=json.dumps(epoch))
        print(response.text)
        assert response.status_code == 201

    def testPostRequest(self):
        tgt = {
            "unique_id": 11111,
            "name": "TargetSat"
        }
        response = requests.post("http://127.0.0.1:5000/api/target", data=json.dumps(tgt))
        print(response)
        assert response.status_code == 201
