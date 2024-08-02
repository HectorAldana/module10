import traceback
import json
from flask import Flask, Response
import http.client, urllib.request, urllib.error

# API endpoint URL's and access keys
WMATA_API_KEY = '10614ae712004363a044a44bdae6d211' # <YOUR_API_KEY_HERE>
INCIDENTS_URL = 'https://api.wmata.com/Incidents.svc/json/ElevatorIncidents'
headers = {'api_key': WMATA_API_KEY, 'Accept': '*/*'}

################################################################################

app = Flask(__name__)

# get incidents by machine type (elevators/escalators)
# field is called 'unit_type' in WMATA API response
@app.route('/incidents/<unit_type>', methods=['GET'])
def get_incidents(unit_type):
  unit_type = unit_type[:-1].upper()

  params = urllib.parse.urlencode({  })
  try:
      # create an empty list called 'incidents'
      incidents = []

      # use 'requests' to do a GET request to the WMATA Incidents API
      # retrieve the JSON from the response
      conn = http.client.HTTPSConnection('api.wmata.com')
      conn.request('GET', '/Incidents.svc/json/ElevatorIncidents?%s' % params, '{body}', headers)
      response = conn.getresponse()
      incidents = json.loads(response.read()) # decode json into dictionary
      conn.close()

      # iterate through the JSON response and retrieve all incidents matching 'unit_type'
      # for each incident, create a dictionary containing the 4 fields from the Module 7 API definition
      #   -StationCode, StationName, UnitType, UnitName
      # add each incident dictionary object to the 'incidents' list
      incidents_list = []
      for incident in incidents['ElevatorIncidents']:
          if incident.get('UnitType') == unit_type:
                # Create a dictionary for each matching incident
                incident_dict = {
                    'StationCode': incident.get('StationCode'),
                    'StationName': incident.get('StationName'),
                    'UnitType': incident.get('UnitType'),
                    'UnitName': incident.get('UnitName')
                }
                # Add the incident dictionary to the 'incidents' list
                incidents_list.append(incident_dict)
                 
  except Exception as e:
        print(f'Error: {str(e)}')
        traceback.print_exc()
        return []

  # return the list of incident dictionaries using json.dumps()
  return Response(json.dumps(incidents_list), mimetype='application/json')
  

if __name__ == '__main__':
    app.run(debug=True)
