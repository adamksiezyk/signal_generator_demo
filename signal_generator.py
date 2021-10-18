from __future__ import annotations

import logging
from dataclasses import dataclass

from logger import log
from scpi_control import SCPIControl


@dataclass
class SignalGeneratorCommands:
    identification: str
    set_frequency: str
    set_power: str


RS_COMMANDS = SignalGeneratorCommands(
    identification="*IDN?",
    set_frequency=":SOURce1:FREQuency:CW {}",
    set_power=":SOURce1:POWer:LEVel:IMMediate:AMPLitude {}"
)


@log
class SignalGenerator:
    def __init__(self, logger: logging.Logger, commands: SignalGeneratorCommands, ip: str, port: int = 5025) -> None:
        self.logger = logger
        self.__commands = commands
        self.ip = ip
        self.port = port
        self.__client = SCPIControl()
        self.manufacturer = ''
        self.model = ''
        self.serial_number = ''

    def __enter__(self) -> SignalGenerator:
        self.connect()
        return self

    def connect(self) -> None:
        self.logger.info(f"Connecting to {(self.ip, self.port)}")
        self.__client.connect(self.ip, self.port)
        self.identification()

    def __exit__(self, exc_type, exc_val, traceback) -> None:
        self.disconnect()

    def disconnect(self) -> None:
        self.logger.debug("Disconnecting")
        self.__client.disconnect()

    def _write(self, msg: str) -> None:
        self.logger.debug(f"Sending: {msg}")
        self.__client.write(msg)

    def _read(self) -> str:
        msg = self.__client.read()
        self.logger.debug(f"Received: {msg}")
        return msg

    def _ask(self, msg) -> str:
        self.logger.debug(f"Sending: {msg}")
        msg = self.__client.ask(msg)
        self.logger.debug(f"Received: {msg}")
        return msg

    def identification(self) -> None:
        idn = self._identification().split(',')
        self.manufacturer = idn[0]
        self.model = idn[1]
        self.serial_number = idn[2]

    def _identification(self) -> str:
        msg = self._ask(self.__commands.identification)
        self.logger.info(f"Connected to: {msg}")
        return msg

    def set_frequency(self, frequency: int) -> None:
        self.logger.info(f"Setting frequency to {frequency:.0f} Hz")
        self._write(self.__commands.set_frequency.format(frequency))

    def set_power(self, power: float) -> None:
        self.logger.info(f"Setting power to {power:.1f} dBm")
        self._write(self.__commands.set_power.format(power))
