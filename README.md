# Project Description

This Python Flask backend application contains backend services which fetches data from IOT device. Service is created for fetching temperature data based on date and time. I have used Mongo Database and Flask to create backend services.

### `Project Setup using Conda`

1: Create anaconda environment by `conda create -n {environment_name} python=3.5`.

2: Activate anaconda environment using `conda activate {environment_name}`.

3: Clone the project and go to the project path.

4: To install all the packages run `pip install -r requirements.txt`.

5: Change MongoDB credentials inside `application.py`.

6: Set Flask enviromental variable like `EXPORT FLASK_APP=application.py` and `EXPORT FLASK_DEBUG=1`.

7: We can also run the project by simply running `python application.py`.

### `Project Setup using Docker`

1: Navigate to the project folder

2: To build the image run the docker command  `sudo docker build --tag flaskapp .`.

3: To Start the application using container run `sudo docker run --name python-app -p 5000:5000 flaskapp`.

**Note: Enter data in database using post operation**

Example: "http://localhost:5000/home"
METHOD: POST

sample json payload:{
	"reading": 32.5,
	"timestamp": 1506161234,
	"sensorType": "Temperature"
}
