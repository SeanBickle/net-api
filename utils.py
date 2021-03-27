import json
import uuid


class DeviceHandler:
    def __init__(self):
        self.devices_filename = "devices.json"
        self.devices = {}
        self.__valid_models = ["ios-xr", "ios-xe", "nx-os"]

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

    def model_valid(self, model):
        """
        Checks the input model is one of the valid values
        :param model: <str> Model to check
        :return: <bool> Model validity
        """
        return model in self.__valid_models

    def get_valid_models(self):
        """
        :return: <list> Valid device models
        """
        return self.__valid_models

    def _create_uuid(self):
        return str(uuid.uuid4())

    def _format_device(self, fqdn, model, version):
        """
        Formats device into standard structure
        """
        return {"dev_fqdn": fqdn, "dev_model": model, "dev_version": version}

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
        dev_uuid = self._create_uuid()
        self.devices[dev_uuid] = self._format_device(fqdn, model, version)
        return True, f"Created device {fqdn} ({dev_uuid})"

    def get_devices(self):
        """
        Gets all network devices. For now, this just returns the contents
        of the devices file.
        :return: <dict> Network devices
        """
        return self.devices

    def get_device_by_id(self, dev_id):
        """
        Get a single device
        :param dev_id: <str> UUID of the target device
        :return: <dict> Device detail
        """
        return self.devices.get(dev_id, {})

    def update_device_by_id(self, dev_id, dev_data):
        """
        Updates a single device. Skip fields with a None value, these have not
        been specified by the user.
        :param dev_id: <str> UUID of target device
        :param dev_data: <dict> Device data of fields to update
        :return: <bool> Success, <str> message
        """
        if dev_id not in self.devices:
            return False, f"Device {dev_id} does not exist"
        for field, value in dev_data.items():
            if value and field in self.devices[dev_id]:
                self.devices[dev_id][field] = value
        return True, f"Updated device {dev_id}"

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
