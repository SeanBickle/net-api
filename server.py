from flask import Flask
from flask_restful import Api, Resource, reqparse
from http import HTTPStatus

from utils import DeviceHandler


app = Flask(__name__)
api = Api(app)


class Index(Resource):
    def get(self):
        return {"message": "Net API is running"}, HTTPStatus.OK


class NetworkDevice(Resource):
    def get(self, dev_id):
        """
        Gets a network device.
        :param dev_id: <str> Unique identifier of the device
        """
        dh = DeviceHandler()
        dh.load_devices()
        device = dh.get_device_by_id(dev_id)
        status = HTTPStatus.OK if device else HTTPStatus.NOT_FOUND
        return {"networkdevice": device}, status

    def post(self, dev_id):
        """
        Creates a new network device.
        :param dev_id: <str> Identifier for the device, in this case FQDN
        ---
        POST to /networkdevice/<string:dev_id>
        {
            "dev_model": <str>,
            "dev_version": <str>
        }
        """
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "dev_model",
            type=str,
            required=True,
            help="A device model is required, e.g. ios-xe",
            location="json",
        )
        self.parser.add_argument(
            "dev_version",
            type=str,
            required=True,
            help="A device version is required",
            location="json",
        )
        self.args = self.parser.parse_args()
        dev_model = self.args["dev_model"]
        dev_version = self.args["dev_version"]

        dh = DeviceHandler()
        dh.load_devices()
        success, msg = dh.create_device(dev_id, dev_model, dev_version)
        dh.write_devices()
        status = HTTPStatus.CREATED if success else HTTPStatus.BAD_REQUEST
        return {"message": msg}, status


api.add_resource(Index, "/")
api.add_resource(NetworkDevice, "/networkdevices/<string:dev_id>")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
