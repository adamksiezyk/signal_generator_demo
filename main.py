from signal_generator import SignalGenerator, RS_COMMANDS


if __name__ == "__main__":
    ip = "192.168.255.240"
    with SignalGenerator(RS_COMMANDS, ip) as sg:
        sg.set_frequency(3440e6)
        sg.set_power(-50)
