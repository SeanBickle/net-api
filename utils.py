import json
import uuid


class DeviceHandler:
    def __init__(self):
        self.devices_filename = "devices.json"
        self.devices = {}
        self.valid_models = ["ios-xr", "ios-xe", "nx-os"]

    def load_devices(self):
        """
        Load JSON from file
        :return: <dict> JSON data from file
        """
        try:
            with open(self.devices_filename) as devices_file:
                self.devices = json.load(devices_file)
        except json.JSONDecodeError:
            self.devices = {}

    def write_devices(self):
        """
        Write the devices dict back to the JSON file
        """
        with open(self.devices_filename, "w") as devices_file:
            json.dump(self.devices, devices_file)

    def _fqdn_exists(self, fqdn):
        """
        Checks whether FQDN currently exists
        :param fqdn: <str> FQDN for which to check
        :return: <bool> Whether FQDN exists
        """
        for dev_id, dev_data in self.devices.items():
            if dev_data["dev_fqdn"] == fqdn:
                return True
        return False

    def _model_valid(self, model):
        """
        Checks the input model is one of the valid values
        :param model: <str> Model to check
        :return: <bool> Model validity
        """
        return model in self.valid_models

    def _create_uuid(self):
        return str(uuid.uuid4())

    def _format_device(self, fqdn, model, version):
        """
        Formats device into standard structure
        """
        return {"dev_fqdn": fqdn, "dev_model": model, "version": version}

    def create_device(self, fqdn, model, version):
        """
        Adds a new device
        :param fqdn: <str> FQDN of device
        :param model: <str> Device model e.g. ios-xr
        :param version: <str> Device version
        :return: <bool> success, <str> message
        """
        if self._fqdn_exists(fqdn):
            return False, f"FQDN {fqdn} already exists"
        if not self._model_valid(model):
            return False, (
                f"Model {model} is invalid. Expected one of the following: "
                f"{', '.join(self.valid_models)}"
            )
        dev_uuid = self._create_uuid()
        self.devices[dev_uuid] = self._format_device(fqdn, model, version)
        return True, f"Created device {fqdn} ({dev_uuid})"

    def get_device_by_id(self, dev_id):
        """
        Get a single device
        :param dev_id: <str> UUID of the target device
        :return: <dict> Device detail
        """
        return self.devices.get(dev_id, {})

    def delete_device_by_id(self, dev_id):
        """
        Deletes a single device.
        :param dev_id: <str> UUID of target device
        :return: <bool> Success, <str> message
        """
        if dev_id not in self.devices:
            return False, f"Device {dev_id} does not exist"
        del self.devices[dev_id]
        return True, f"Deleted device {dev_id}"
