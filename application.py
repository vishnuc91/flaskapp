from flask import Flask, request
from flask_restplus import Resource, Api, Namespace
from datetime import datetime
from pymongo import MongoClient
from flask_cors import CORS
import urllib


username = urllib.parse.quote_plus('admin')
password = urllib.parse.quote_plus('Cr0$$t@b123')
uri = "mongodb://{username}:{password}@localhost:27017/?authSource=admin".format(username=username, password=password)
client = MongoClient(uri)
database = client["iot"]
sensordata = database["sensordata"]

app = Flask(__name__)
api = Api(app)

CORS(app, resources={r"/api/*": {"origins": "*"}})


@api.route('/home')
class IOTSensor(Resource):

    def get(self):
        sensor_data = []
        if len(request.args) > 0:
            from_date = request.args['from']
            to_date = request.args['to']
            sensordatas = sensordata.find({'date': {'$lt': to_date, '$gte': from_date}})
            for datas in sensordatas:
                sensor_data.append({"temperature": datas["temperature"], "sensortype": datas["sensortype"],
                   "date": datas["date"], "time": datas["time"]})
            if len(sensor_data) > 0:
                return {'message': 'Successfull', 'data': sensor_data}
            else:
                return {'message': 'Successfull', 'data': 'No Data Available'}
        else:
            sensordatas = sensordata.find()
            for datas in sensordatas:
                sensor_data.append({"temperature": datas["temperature"], "sensortype": datas["sensortype"],
                   "date": datas["date"], "time": datas["time"]})
            return {'message': 'Successfull', 'data': sensor_data}

    # @api.doc(parser=parser)
    def post(self):
        json_data = request.get_json()
        date_time = datetime.fromtimestamp(json_data["timestamp"]).isoformat()
        date_time = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S")
        data= {"temperature": json_data["reading"], "sensortype": json_data["sensorType"],
               "date": date_time.date().isoformat(), "time": date_time.time().isoformat()}
        sensor_data = sensordata.insert_one(data).inserted_id
        return {'message': 'Data Saved', "id": str(sensor_data)}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
