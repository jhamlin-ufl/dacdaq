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
from pymeasure.instruments.validators import (
    truncated_range,
    truncated_discrete_set,
    strict_discrete_set,
)


class Prema6000(Instrument):
    """Control the Prema 6000 digital multimeter (DMM) instrument."""

    MODES = {
        "direct voltage": "VD",
        "alternating voltage": "VA",
        "2-wire resistance": "02",
        "4-wire resistance": "04",
        "direct current": "ID",
        "alternating current": "IA",
    }

    mode = Instrument.control(
        "P0",
        "%s",
        """ A string property that controls the configuration mode for measurements,
        which can take the values: ``direct voltage``, ``alternating voltage``,
        ``2-wire resistance``, ``4-wire resistance``, ``direct current``, or
        ``alternating current``""",
        validator=strict_discrete_set,
        values=MODES,
        map_values=True,
    )

    def __init__(self, adapter, name="Prema 6000 DMM", **kwargs):
        super().__init__(adapter, name, **kwargs)


sourcemeter = Prema6000("GPIB::7")
sourcemeter.mode.setter("2-wire resistance")
