#!/bin/python3

class router():
    nicks = []
    ipaddr = []
    connections = {}

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.nicks}, {self.ipaddr}, {self.connections}'

    def addNick(self, interfaceName, ipAddr):
        """
        interfaceName and ipAddr must be relative to the same nick
        both interfaceName and ipAddr must be strings
        """
        self.nicks.append(interfaceName)
        self.ipaddr.append(ipAddr)

    def addConnection(self, ipAddrSelf, ipAddrOther):
        if ipAddrSelf not in self.ipaddr:
            raise ValueError("invalid connection!")
        if ipAddrSelf not in self.connections:
            self.connections[ipAddrSelf] = [ipAddrOther]
        else:
            conn = self.connections[ipAddrSelf]
            if ipAddrOther in conn:
                raise ValueError("connecton already established")
            conn.append(ipAddrOther)


routerA = router("A")
routerA.addNick("eth1", "192.168.1.1")
routerA.addConnection("192.168.1.1", "192.168.1.2")
routerA.addConnection("192.168.1.1", "192.168.1.3")
print(routerA)
