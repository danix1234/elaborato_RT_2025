#!/bin/python3

class router():
    routers = []
    connections = {}
    connNetwork = {}

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
        router.connections[ipAddrSelf] = ipAddrOther
        router.connNetwork[ipAddrSelf] = ipNetwork

    def printConnections():
        print("Connections:")
        for conn in router.connections:
            conn2 = router.connections[conn]
            connNetwork = router.connNetwork[conn]
            print(conn, "-", conn2, "-->", connNetwork)


# build topology represented in topology.png image
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
router.addConnection("192.168.1.1", "192.168.1.2", "192.168.1.0")
router.addConnection("192.168.2.1", "192.168.2.2", "192.168.2.0")
router.addConnection("192.168.3.1", "192.168.3.2", "192.168.3.0")
router.addConnection("192.168.4.1", "192.168.4.2", "192.168.4.0")

# show topology
print(routerA)
print(routerB)
print(routerC)
print(routerD)
router.printConnections()
