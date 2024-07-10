#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2024 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import strict_discrete_set

MODES = {
    "direct voltage": "VD",
    "alternating voltage": "VA",
    "2-wire resistance": "O2",  # Note O not 0! Stupid Prema
    "4-wire resistance": "O4",  # Note O not 0! Stupid Prema
    "direct current": "ID",
    "alternating current": "IA",
    "celsius": "TC",
    "farenheit": "TF",
    "kelvin": "TK",
}


def status_string_to_mode(response_string):
    lookup = {v: k for k, v in MODES.items()}
    mode_string = response_string[12:14]
    return lookup[mode_string]


class Prema6000(Instrument):
    """Control the Prema 6000 digital multimeter (DMM) instrument."""

    MODES = {
        "direct voltage": "VD",
        "alternating voltage": "VA",
        "2-wire resistance": "O2",  # Note O not 0! Stupid Prema
        "4-wire resistance": "O4",  # Note O not 0! Stupid Prema
        "direct current": "ID",
        "alternating current": "IA",
        "celsius": "TC",
        "farenheit": "TF",
        "kelvin": "TK",
    }

    mode = Instrument.control(
        "P0",
        "%s",
        """ A string property that controls the configuration mode for measurements,
        which can take the values: ``direct voltage``, ``alternating voltage``,
        ``2-wire resistance``, ``4-wire resistance``, ``direct current``,
        ``alternating current``, ``celsius``, ``farenheit``, or ``kelvin``.""",
        validator=strict_discrete_set,
        values=MODES,
        map_values=True,
    )

    return_mode = Instrument.control(
        None,
        "%s",
        """ A string property that controls whether the instrument
        transmits only the measurements result or the measurement
        result and a status code.  Takes the values:
        ``measurement only``, ``measurement and status``.""",
        validator=strict_discrete_set,
        values={"measurement only": "L0", "measurement and status": "L1"},
        map_values=True,
    )

    autorange = Instrument.control(
        None,
        "%s",
        """ A string property that enables or disable the
        autorange function, which can take the values:
        ``enabled`` or True and ``disabled`` or False.""",
        validator=strict_discrete_set,
        values={True: "A1", False: "A0", "enabled": "A1", "disabled": "A0"},
        map_values=True,
    )

    integration_time = Instrument.control(
        None,
        "%s",
        """ A string property that sets the integration
        time used by the instrument, which can take the values:
        ``100ms``, ``1s``, or ``10s``.""",
        validator=strict_discrete_set,
        values={"100ms": "T1", "1s": "T3", "10s": "T4"},
        map_values=True,
    )

    voltage = Instrument.measurement(
        "P0",
        """Reads DC or AC voltage based on the currently
        active mode of the instrument""",
        get_process=lambda x: x[:12],
    )

    resistance = Instrument.measurement(
        "P0",
        """Reads 2- or 4-wire resistance based on the currently
        active mode of the instrument""",
        get_process=lambda x: x[:12],
    )

    current = Instrument.measurement(
        "P0",
        """Reads DC or AC current based on the currently
        active mode of the instrument""",
        get_process=lambda x: x[:12],
    )

    temperature = Instrument.measurement(
        "P0",
        """Reads temperature.  Based on the currently
        active mode of the instrument, the value will be
        in celsius, farenheit, or kelvin.""",
        get_process=lambda x: x[:12],
    )

    def __init__(self, adapter, name="Prema 6000 DMM", **kwargs):
        super().__init__(adapter, name, **kwargs)


sourcemeter = Prema6000("GPIB::7")
sourcemeter.mode = "4-wire resistance"
print(f"{sourcemeter.resistance = }")
print(f'{sourcemeter.ask("P0") = }')
print(f"{sourcemeter.mode = }")


class Foobar:
    def myfunc(self, something):
        print(f"{something} is cool!")

    def anotherfunc(self, something):
        print("calling anotherfunc and then calling myfunc...")
        self.myfunc(something)

    VARIABLE = 2


myfoobar = Foobar()
print(myfoobar.VARIABLE)
