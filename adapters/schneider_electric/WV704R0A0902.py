import json
from adapters.base_adapter import Adapter
from devices.sensor.temperature import TemperatureSensor
from devices.sensor.voltage import VoltageSensor
from devices.sensor.percentage import PercentageSensor
from devices.switch.selector_switch import SelectorSwitch
from devices.setpoint import SetPoint


class WV704R0A0902(Adapter):
    def __init__(self):
        super().__init__()

        self.devices.append(VoltageSensor('cell', 'voltage', ' (Battery Voltage)'))
        self.devices.append(PercentageSensor('btperc', 'battery', ' (Battery)'))
        self.devices.append(TemperatureSensor('temp', 'local_temperature', ' (Temperature)'))
        self.devices.append(SetPoint('spoint', 'occupied_heating_setpoint', ' (SetPoint)'))

    def handle_command(self, alias, device, command, level, color):
        topic = self.name + '/set'

        if alias == 'spoint' and command == 'Set Level':
            msg = json.dumps({'occupied_heating_setpoint': level})

            return {
                'topic': topic,
                'payload': msg
            }
