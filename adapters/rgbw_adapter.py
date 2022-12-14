from adapters.base_adapter import Adapter
from adapters.generic.mixins.rgb import RGBMixin
from devices.rgbw_light import RGBWLight


class RGBWAdapter(Adapter, RGBMixin):
    def __init__(self):
        super().__init__()

        self.dimmer = RGBWLight('light', 'state_brightness_color')
        self.devices.append(self.dimmer)

    def convert_message(self, message):
        message = super().convert_message(message)

        if 'color_temp' in message.raw:
            message.raw['color_temp'] = int(message.raw['color_temp'] * 255 / 500)

        return message

    def handle_command(self, alias, device, command, level, color):
        topic = self.name + '/set'
        return self.set_color(topic, command, level, color)
