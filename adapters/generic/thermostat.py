import json
from adapters.adapter_with_battery import AdapterWithBattery
from devices.sensor.temperature import TemperatureSensor
from devices.switch.selector_switch import SelectorSwitch
from devices.setpoint import SetPoint


class ThermostatAdapter(AdapterWithBattery):

    def __init__(self):
        super().__init__()

        mode_switch = SelectorSwitch('mode', 'system_mode', ' (Mode)')
        mode_switch.add_level('Off', 'off')
        mode_switch.add_level('Auto', 'auto')
        mode_switch.add_level('Heat', 'heat')
        mode_switch.set_selector_style(SelectorSwitch.SELECTOR_TYPE_BUTTONS)
        mode_switch.set_icon(15)

        self.devices.append(TemperatureSensor('temp', 'local_temperature',' (Temperature)'))
        self.devices.append(SetPoint('spoint', 'current_heating_setpoint',' (Setpoint)'))
        self.devices.append(mode_switch)

    def handle_command(self, alias, device, command, level, color):
        topic = self.name + '/set'

        if alias == 'spoint' and command == 'Set Level':
            msg = json.dumps({ 'current_heating_setpoint': level })

            return {
                'topic': topic,
                'payload': msg
            }

        if alias == 'mode':
            switch = self.get_device_by_alias(alias)
            level_index = int(level / 10)
            msg = json.dumps({ 'system_mode': switch.level_values[level_index] })

            return {
                'topic': topic,
                'payload': msg
            }
