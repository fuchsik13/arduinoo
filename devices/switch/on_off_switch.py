import domoticz
from devices.device import Device


class OnOffSwitch(Device):
    def __init__(self, alias, value_key, device_name_suffix=''):
        super().__init__(alias, value_key, device_name_suffix)
        self.icon = 1

    def set_icon(self, icon_number):
        self.icon = icon_number

    def create_device(self, unit, device_id, device_name):
        return domoticz.create_device(Unit=unit, DeviceID=device_id, Name=device_name, TypeName="Switch", Image=self.icon)

    def get_numeric_value(self, value, device):
        if hasattr(self, 'feature'):
            if 'value_on' in self.feature and value == self.feature['value_on']:
                return 1
            if 'value_off' in self.feature and value == self.feature['value_off']:
                return 0
            else:
                return device.nValue
        elif value.lower() == 'on':
            return 1
        elif value.lower() == 'off':
            return 0
        else:
            return device.nValue

    def get_string_value(self, value, device):
        n_value = self.get_numeric_value(value, device)
        return 'On' if n_value == 1 else 'Off'

    def handle_command(self, device_data, command, level, color):
        device_address = device_data['ieee_addr']
        device = self.get_device(device_address)

        domoticz.debug('Command "' + command + '" from device "' + device.Name + '"')

        self.update_device(device, {
            'nValue': self.get_numeric_value(command, device),
            'sValue': self.get_string_value(command, device)
        })
