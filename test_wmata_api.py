from wmata_api import app
import json
import unittest

class WMATATest(unittest.TestCase):
    # ensure both endpoints return a 200 HTTP code
    def test_http_success(self):
        escalators_response = app.test_client().get('/incidents/escalators')
        # assert that the response code of 'incidents/escalators returns a 200 code
        self.assertEqual(escalators_response.status_code, 200)

        elevators_response = app.test_client().get('/incidents/elevators')
        # assert that the response code of 'incidents/elevators returns a 200 code
        self.assertEqual(elevators_response.status_code, 200)

################################################################################

    # ensure all returned incidents have the 4 required fields
    def test_required_fields(self):
        required_fields = ["StationCode", "StationName", "UnitType", "UnitName"]

        response = app.test_client().get('/incidents/escalators')
        json_response = json.loads(response.data.decode())

        # for each incident in the JSON response assert that each of the required fields
        # are present in the response
        for incident in json_response:
                for field in required_fields:
                    self.assertIn(field, incident, f'Missing field: {field} in incident: {incident} for unit type: ESCALATOR')


################################################################################

    # ensure all entries returned by the /escalators endpoint have a UnitType of "escalators"
    def test_escalators(self):
        response = app.test_client().get('/incidents/escalators')
        json_response = json.loads(response.data.decode())

        # for each incident in the JSON response, assert that the 'UnitType' is "escalators"
        for incident in json_response:
            self.assertEqual(incident.get('UnitType'), 'ESCALATOR', f"UnitType is not 'ESCALATOR' in incident: {incident}")


################################################################################

    # ensure all entries returned by the /elevators endpoint have a UnitType of "elevators"
    def test_elevators(self):
        response = app.test_client().get('/incidents/elevators')
        json_response = json.loads(response.data.decode())

        # for each incident in the JSON response, assert that the 'UnitType' is "elevators"
        for incident in json_response:
            self.assertEqual(incident.get('UnitType'), 'ELEVATOR', f"UnitType is not 'ELEVATOR' in incident: {incident}")

################################################################################

if __name__ == "__main__":
    unittest.main()