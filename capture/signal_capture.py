from typing import List
from typing import Tuple
from multiprocessing import Event
from multiprocessing import Value
from datetime import datetime

import pytz
import serial
from dateutil.parser import parse

from capture.base_capture import BaseCapture


class SignalCapture(BaseCapture):

    def __init__(self, serial_port: str, serial_bound_rate: int,
                 signal_buffer: List, interval: float, capture_index: Value,
                 capture_event: Event, terminate_event: Event) -> None:
        self._serial_port = serial_port
        self._serial_bound_rate = serial_bound_rate
        self._serial_interface = serial.Serial(self._serial_port,
                                               self._serial_bound_rate)
        self._signal_buffer = signal_buffer
        super(SignalCapture, self).__init__(interval, capture_index,
                                            capture_event, terminate_event)

    def start_capture(self) -> None:
        self._serial_interface.reset_output_buffer()
        self._serial_interface.reset_input_buffer()
        return super(SignalCapture, self).start_capture()

    def read_line(self) -> bytes:
        return self._serial_interface.readline()

    def handler(self) -> None:
        current_datetime = pytz.utc.localize(datetime.utcnow())
        data = current_datetime.isoformat().encode(
            'ascii') + b',' + self.read_line()
        self._signal_buffer.append(data)

    def pop_buffer(self) -> List[Tuple[datetime, float, float, float]]:

        def parse_signals(raw_value):
            try:
                values = raw_value.replace(b'\n', b'').replace(b'\r', b'')
                values = values.decode('utf-8').split(',')
                datetime_str, bvp, gsr, skt = values
                return parse(datetime_str), float(bvp), float(gsr), float(skt)
            except BaseException:
                return None

        result_list = [
            value for value in map(parse_signals, self._signal_buffer)
            if value is not None
        ]
        for _ in range(len(self._signal_buffer)):
            self._signal_buffer.pop()
        return result_list
