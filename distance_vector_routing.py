#!/bin/python3


class Router():
    routers = []
    connectionSide1 = []
    connectionSide2 = []
    connectionNetwork = []

    def __init__(self, name):
        self.name = name
        self.nicks = []
        self.ipaddr = []
        self.routers.append(self)

    def __str__(self):
        return f'{self.name}, {self.nicks}, {self.ipaddr}'

    def addNick(self, interfaceName, ipAddr):
        """
        interfaceName and ipAddr must be relative to the same nick
        both interfaceName and ipAddr must be strings
        """
        self.nicks.append(interfaceName)
        self.ipaddr.append(ipAddr)

    def addConnection(ipAddrSelf, ipAddrOther, ipNetwork):
        Router.connectionSide1.append(ipAddrSelf)
        Router.connectionSide2.append(ipAddrOther)
        Router.connectionNetwork.append(ipNetwork)

    def printConnections():
        print("Connections:")
        for i, conn in enumerate(Router.connectionSide1):
            conn2 = Router.connectionSide2[i]
            connNetwork = Router.connectionNetwork[i]
            print(conn, "-", conn2, "-->", connNetwork)


# build topology represented in topology.png image
routerA = Router("A")
routerB = Router("B")
routerC = Router("C")
routerD = Router("D")
routerA.addNick("eth1", "192.168.1.1")
routerB.addNick("eth1", "192.168.2.1")
routerB.addNick("eth2", "192.168.4.1")
routerB.addNick("eth3", "192.168.1.2")
routerC.addNick("eth1", "192.168.2.2")
routerC.addNick("eth2", "192.168.3.1")
routerD.addNick("eth1", "192.168.4.2")
routerD.addNick("eth2", "192.168.3.2")
Router.addConnection("192.168.1.1", "192.168.1.2", "192.168.1.0")
Router.addConnection("192.168.2.1", "192.168.2.2", "192.168.2.0")
Router.addConnection("192.168.3.1", "192.168.3.2", "192.168.3.0")
Router.addConnection("192.168.4.1", "192.168.4.2", "192.168.4.0")

# show topology
print(routerA)
print(routerB)
print(routerC)
print(routerD)
Router.printConnections()
