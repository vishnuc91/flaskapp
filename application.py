from flask import Flask, request
from flask_restplus import Resource, Api, Namespace
from datetime import datetime
from pymongo import MongoClient
from flask_cors import CORS
import urllib



app = Flask(__name__)
api = Api(app)

CORS(app, resources={r"/api/*": {"origins": "*"}})

@api.route('/test')
class Test(Resource):

    def get(self):
        return {"message": 'successfull buddy1', 'status': 200}


@api.route('/home')
class IOTSensor(Resource):

    def __init__(self):
        self.username = urllib.parse.quote_plus('admin')
        self.password = urllib.parse.quote_plus('Cr0$$t@b123')
        self.uri = "mongodb://{username}:{password}@localhost:27017/?authSource=admin".format(username=self.username,
                                                                                         password=self.password)
        self.client = MongoClient(self.uri)
        self.database = self.client["iot"]
        self.sensordata = self.database["sensordata"]

    def get(self):
        sensor_data = []
        aggregates = {}
        if len(request.args) > 0:
            from_date = request.args['from']
            to_date = request.args['to']
            sensordatas = self.sensordata.find({'date': {'$lte': to_date, '$gte': from_date}})
            aggregate_data = self.sensordata.aggregate([{'$match': {'date': {'$gte': from_date, '$lte': to_date}}}, {
                '$group': {'_id': 'none', 'min': {'$min': "$temperature"}, 'max': {'$max': "$temperature"},
                           'avg': {'$avg': "$temperature"}}}])
            for data in aggregate_data:
                aggregates = data
            for datas in sensordatas:
                sensor_data.append({"temperature": datas["temperature"], "sensortype": datas["sensortype"],
                                    "date": datas["date"], "time": datas["time"]})
            if len(sensor_data) > 0:
                return {'message': 'Successfull', 'data': sensor_data, 'aggregates': aggregates}
            else:
                return {'message': 'Successfull', 'data': 'No Data Available'}
        else:
            sensordatas = self.sensordata.find()
            # Used mongo aggregations to query for mean ,max and min
            aggregate_data = self.sensordata.aggregate([{'$group': {'_id': 'none', 'min': {"$min": "$temperature"},
                                                               "max": {"$max": "$temperature"},
                                                               "avg": {"$avg": "$temperature"}}}])
            for data in aggregate_data:
                aggregates = data
            for datas in sensordatas:
                sensor_data.append({"temperature": datas["temperature"], "sensortype": datas["sensortype"],
                                    "date": datas["date"], "time": datas["time"]})
            return {'message': 'Successfull', 'data': sensor_data, 'aggregates': aggregates}

    # @api.doc(parser=parser)
    def post(self):
        json_data = request.get_json()
        date_time = datetime.fromtimestamp(json_data["timestamp"]).isoformat()
        date_time = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S")
        data = {"temperature": json_data["reading"], "sensortype": json_data["sensorType"],
                "date": date_time.date().isoformat(), "time": date_time.time().isoformat()}
        sensor_data = self.sensordata.insert_one(data).inserted_id
        return {'message': 'Data Saved', "id": str(sensor_data)}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
