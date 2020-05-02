from flask import Flask, request
from flask_restplus import Resource, Api, Namespace
from datetime import datetime
from pymongo import MongoClient
import urllib


username = urllib.parse.quote_plus('admin')
password = urllib.parse.quote_plus('Cr0$$t@b123')
uri = "mongodb://{username}:{password}@localhost:27017/?authSource=admin".format(username=username, password=password)
client = MongoClient(uri)

database = client["iot"]
sensordata = database["sensordata"]

app = Flask(__name__)
api = Api(app)

# api = Namespace('Sensor Details', description='')
# parser = api.parser()
# parser.add_argument('temperature', type=str, help='project_name', location='form')


@api.route('/home')
class IOTSensor(Resource):

    def get(self):
        sensordatas = sensordata.find()
        for datas in sensordatas:
            print (datas)
        return {'hello': 'world'}

    # @api.doc(parser=parser)
    def post(self):
        json_data = request.get_json()
        date_time = datetime.fromtimestamp(json_data["timestamp"]).isoformat()
        date_time = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S")
        data= {"temperature": json_data["reading"], "sensortype": json_data["sensorType"],
               "date": date_time.date().isoformat(), "time": date_time.time().isoformat()}
        print (data)
        return {'message': 'Data Saved'}


if __name__ == '__main__':
    app.run(debug=True)
