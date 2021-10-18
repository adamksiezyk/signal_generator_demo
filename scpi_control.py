import socket


class SCPIError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class SCPIControl:
    """
    Class for device controll over SCPI
    """

    def __init__(self):
        self.connected = False
        # Create TCP socket
        self.handle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Disable Nagle algorithm
        self.handle.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.handle.settimeout(1)

    def connect(self, ip: str, port: int) -> None:
        try:
            self.handle.connect((ip, port))
            self.connected = True
            return True
        except socket.error as e:
            self.connected = False
            raise SCPIError(
                f"An error occured while trying to connect: {e!s}")

    def disconnect(self) -> None:
        try:
            self.handle.close()
            self.connected = False
        except socket.error as e:
            self.connected = False
            raise SCPIError(
                f"An error occured while trying to disconnect: {e!s}")

    def write(self, msg: str) -> None:
        msg_ = msg + '\n'
        msg_len = len(msg_)
        try:
            totalsent = 0
            while totalsent < msg_len:
                sent = self.handle.send(msg_[totalsent:].encode())
                if sent == 0:
                    raise socket.error("Connection broken")
                totalsent = totalsent + sent
        except socket.error as e:
            self.connected = False
            raise SCPIError(
                f"An error occured while trying to send message: {msg!r}. {e!s}")

    def read(self) -> str:
        try:
            msg = ""
            finished = False
            while not finished:
                chunk = self.handle.recv(1).decode()
                if chunk == '\n':
                    finished = True
                if chunk == "":
                    raise socket.error("Connection broke")
                msg = msg + chunk.strip()
            return msg
        except socket.error as e:
            self.connected = False
            raise SCPIError(
                f"An error occured while trying to receive message: {msg!r}. {e!s}")

    def ask(self, msg) -> str:
        self.write(msg)
        return self.read()
