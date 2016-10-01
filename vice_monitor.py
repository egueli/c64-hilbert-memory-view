import socket
import re


class ViceRemoteMonitorTalker:
    def __init__(self):
        ip = '127.0.0.1'
        port = 6510

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.connect((ip, port))

        self.promptRegex = "\(C:\$[0-9a-f]{4}\) "
        self.firstTalk = True

    def talk(self, command):
        self.sock.send(command + "\n")
        if self.firstTalk:
            self.receive()
            self.firstTalk = False
            # print "tt", "skipped first talk"

        lines = self.receive()
        # for line in lines:
        #  	print "tt>>", line
        return lines

    def receive(self):
        data = True
        input_buffer = ""
        while data:
            # print "rr before recv, count:", self.count
            data = self.sock.recv(4096)
            input_buffer += data
            # print "rr", "|" + data + "|"

            prompt_matches = [m for m in re.finditer(self.promptRegex, input_buffer)]
            if len(prompt_matches) > 0:
                pos = prompt_matches[-1].start()
                # print "rr", "prompt found at", pos
                output = input_buffer[:pos]
                lines = output.split("\n")

                return lines[:-1]
            # else:
            # 	print "rr", "prompt is not here"

    def close(self):
        self.sock.close()
