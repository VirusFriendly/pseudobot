import socket
from select import select

commands = {
    "PING": "PONG!",
    "!* GETLOCALIP": "My IP: 127.168.53.103",
    "!* SCANNER OFF": "SCANNER STOPPED!",
    "!* SCANNER ON": "SCANNER STARTED!",
    "!* REPLICATION START": "REPLICATION STARTED!",
    "!* REPLICATION STOP": "REPLICATION STOPPED!",
    "!* HOLD": "",
    "!* JUNK": "",
    "!* KILLATTK": "",
    "!* LOLNOGTFO": ""
}

log_commands = ["!* HOLD", "!* JUNK", "!* KILLATTK", "!* LOLNOGTFO"]

f = open("./lizkebab.cfg","r")
logfile = open("./lizkebab.log", "w")

servers = []

for line in f:
    ip, port = line.split(":")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.connect((ip, int(port)))
    except:
        print "%s refused connection" % (ip)
    else:
        servers.append(server)
        print "connected to %s:%s" % (ip, port)

while True:
    connections, x, y = select(servers, [], [])

    for server in connections:
        try:
            message = server.recv(4096)
            address = server.getpeername()
        except:
            pass
        else:
            if len(message) > 0:
                print "%s: %s %d" % (address, repr(message), len(message))

            while len(message) > 0:
                for command in commands.keys():
                    if message[:len(command)] == command:
                        if command in log_commands:
                            logfile.write("%s: %s" % (address, message))
                        server.send(commands[command])
                        message = message[len(command):]
                        break
                else:
                    command = "!* SCANNER"

                    if message[:len(command)] == command:
                        server.send("!* SCANNER ON | OFF")
                        message = message[len(command):]
                    elif len(message) > 1:
                        logfile.write("unknown command: %s from server: %s" % (message, address))
                        message = ""
                    else:
                        message = ""