from flask import Flask
from flask_restful import Api, Resource, reqparse
from http import HTTPStatus

from utils import DeviceHandler


app = Flask(__name__)
api = Api(app)


class Index(Resource):
    def get(self):
        return {"message": "Net API is running"}, HTTPStatus.OK


class NetworkDevices(Resource):
    def get(self):
        """
        List all network devices.
        """
        dh = DeviceHandler()
        dh.load_devices()
        devices = dh.get_devices()
        return {"networkdevices": devices}, HTTPStatus.OK


class NetworkDevice(Resource):
    def get(self, dev_id):
        """
        Gets a network device by UUID.
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
        if not dh.model_valid(dev_model):
            msg = (
                f"Model is invalid. Expected one of the following: "
                f"{', '.join(dh.get_valid_models())}"
            )
            return {"dev_model": msg}, HTTPStatus.BAD_REQUEST

        dh.load_devices()
        success, msg = dh.create_device(dev_id, dev_model, dev_version)
        dh.write_devices()
        status = HTTPStatus.CREATED if success else HTTPStatus.BAD_REQUEST
        return {"message": msg}, status

    def patch(self, dev_id):
        """
        Update one or more device fields.
        :param dev_id: <str> ID of the device to update
        ---
        POST to /networkdevice/<string:dev_id>
        {
            "dev_fqdn": <str>,
            "dev_model": <str>,
            "dev_version": <str>
        }
        """
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "dev_fqdn",
            type=str,
            required=False,
            help="The FQDN of the device",
            location="json",
        )
        self.parser.add_argument(
            "dev_model",
            type=str,
            required=False,
            help="The model of the device",
            location="json",
        )
        self.parser.add_argument(
            "dev_version",
            type=str,
            required=False,
            help="The version of the device",
            location="json",
        )
        self.args = self.parser.parse_args()
        dh = DeviceHandler()
        dev_model = self.args["dev_model"]
        if dev_model and not dh.model_valid(dev_model):
            msg = (
                f"Model is invalid. Expected one of the following: "
                f"{', '.join(dh.get_valid_models())}"
            )
            return {"dev_model": msg}, HTTPStatus.BAD_REQUEST

        dh.load_devices()
        success, msg = dh.update_device_by_id(dev_id, self.args)
        dh.write_devices()
        status = HTTPStatus.ACCEPTED if success else HTTPStatus.BAD_REQUEST
        return {"message": msg}, status

    def delete(self, dev_id):
        """
        Deletes a network device by UUID
        :param dev_id: <str> ID of the device to update
        """
        dh = DeviceHandler()
        dh.load_devices()
        success, msg = dh.delete_device_by_id(dev_id)
        dh.write_devices()
        status = HTTPStatus.ACCEPTED if success else HTTPStatus.NOT_FOUND
        return {"message": msg}, status


api.add_resource(Index, "/")
api.add_resource(NetworkDevices, "/networkdevices")
api.add_resource(NetworkDevice, "/networkdevices/<string:dev_id>")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
