from flask import current_app as app, json, url_for


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
            "julian_date": 2459144.3
        }
        response = client.post(url_for('api.epochresource'), data=json.dumps(epoch))
        app.logger.info(response.data)
        assert response.status_code == 201

    def testEpochBadPostRequest(self, client):
        epoch = {
            "julia_date": 2459144.5
        }
        response = client.post(url_for('api.epochresource'), data=json.dumps(epoch))
        app.logger.info(response.data)
        assert response.status_code == 422

    def testTargetPostRequest(self, client):
        tgt = {
            "unique_id": 11112,
            "name": "TargetSat1"
        }
        response = client.post(url_for('api.targetresource'), data=json.dumps(tgt))
        app.logger.info(response.data)
        assert response.status_code == 201
