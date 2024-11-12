#!/bin/python3

class router():
    # keep track of all routers has. Necessary for broadcast operations
    routers = []

    def __init__(self, name):
        self.name = name
        self.nicks = []
        self.ipaddr = []
        self.connections = {}
        self.routers.append(self)

    def __str__(self):
        return f'{self.name}, {self.nicks}, {self.ipaddr}, {self.connections}'

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
routerB = router("B")
routerC = router("C")
routerD = router("D")

routerA.addNick("eth1", "192.168.1.1")

routerB.addNick("eth1", "192.168.2.1")
routerB.addNick("eth2", "192.168.4.1")
routerB.addNick("eth3", "192.168.1.2")

routerC.addNick("eth1", "192.168.2.2")
routerC.addNick("eth2", "192.168.3.1")

routerD.addNick("eth1", "192.168.4.2")
routerD.addNick("eth2", "192.168.3.2")

print(routerA)
print(routerB)
print(routerC)
print(routerD)
