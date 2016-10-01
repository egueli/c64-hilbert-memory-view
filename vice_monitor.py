import socket
import re


class ViceRemoteMonitorTalker:
    def __init__(self):
        TCP_IP = '127.0.0.1'
        TCP_PORT = 6510

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.connect((TCP_IP, TCP_PORT))

        self.promptRegex = "\(C:\$[0-9a-f]{4}\) "
        self.firstTalk = True

    def talk(self, command):
        self.sock.send(command + "\n")
        if self.firstTalk == True:
            self.receive()
            self.firstTalk = False
            # print "tt", "skipped first talk"

        lines = self.receive()
        # for line in lines:
        #  	print "tt>>", line
        return lines

    def receive(self):
        data = True
        buffer = ""
        while data:
            # print "rr before recv, count:", self.count
            data = self.sock.recv(4096)
            buffer += data
            # print "rr", "|" + data + "|"

            promptMatches = [m for m in re.finditer(self.promptRegex, buffer)]
            if len(promptMatches) > 0:
                pos = promptMatches[-1].start()
                # print "rr", "prompt found at", pos
                output = buffer[:pos]
                lines = output.split("\n")

                return lines[:-1]
            # else:
            # 	print "rr", "prompt is not here"

    def close(self):
        self.sock.close()
