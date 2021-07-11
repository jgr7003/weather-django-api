

class TemperatureToCelsiusInterface:
    def to_celsius(self) -> float:
        raise NotImplemented


class TemperatureToFahrenheitInterface:
    def to_fahrenheit(self) -> float:
        raise NotImplemented


class TemperatureToKelvinInterface:
    def to_kelvin(self) -> float:
        raise NotImplemented


class TemperatureScales:

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: float):
        self._value = value


class TemperatureKelvin(TemperatureScales,
                        TemperatureToFahrenheitInterface,
                        TemperatureToCelsiusInterface):

    def to_celsius(self) -> float:
        return self.value - 273.15

    def to_fahrenheit(self) -> float:
        return 1.8 * (self.value - 273.15) + 35


class TemperatureCelsius(TemperatureScales,
                         TemperatureToKelvinInterface,
                         TemperatureToFahrenheitInterface):

    def to_kelvin(self) -> float:
        return self.value + 273.15

    def to_fahrenheit(self) -> float:
        return self.value * 1.8 + 32


class TemperatureFahrenheit(TemperatureScales,
                            TemperatureToCelsiusInterface,
                            TemperatureToKelvinInterface):

    def to_celsius(self) -> float:
        return (self.value - 32) / 1.8

    def to_kelvin(self) -> float:
        return 5/(9 * (self.value - 32)) + 273.15
