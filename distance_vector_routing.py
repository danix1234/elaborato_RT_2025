#!/bin/python3

class RoutingTable():
    def __init__(self):
        self.destination = []
        self.nextHop = []
        self.distance = []

    def __str__(self, name):
        res = f"Routing Table of {name}:"
        for i, dest in enumerate(self.destination):
            nextHop = self.nextHop[i]
            distance = self.distance[i]
            res += f'\n{dest},{nextHop},{distance}'
        return res


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
        self.routingTable = RoutingTable()

    def __str__(self):
        return f'{self.name}, {self.nicks}, {self.ipaddr}'

    def addNick(self, interfaceName, ipAddr):
        self.nicks.append(interfaceName)
        self.ipaddr.append(ipAddr)

    def addConnection(ipAddrSelf, ipAddrOther, ipNetwork):
        Router.connectionSide1.append(ipAddrSelf)
        Router.connectionSide2.append(ipAddrOther)
        Router.connectionNetwork.append(ipNetwork)

    def findRouter(ipAddr):
        for router in Router.routers:
            if ipAddr in router.ipaddr:
                return router

    def printConnections(self=None):
        if self is not None:
            print(f"Connections of {self.name}")
        else:
            print("Connections:")
        for i, conn in enumerate(Router.connectionSide1):
            conn2 = Router.connectionSide2[i]
            connNetwork = Router.connectionNetwork[i]
            if self is not None:
                if conn not in self.ipaddr and conn2 not in self.ipaddr:
                    continue
                else:
                    if conn2 in self.ipaddr:
                        tmp = conn
                        conn = conn2
                        conn2 = tmp
            r1 = Router.findRouter(conn).name
            r2 = Router.findRouter(conn2).name
            print(f"({r1}) {conn} - ({r2}) {conn2} --> {connNetwork}")

    def printRoutingTable(self=None):
        if self is None:
            for router in Router.routers:
                router.printRoutingTable()
        else:
            print(self.routingTable.__str__(self.name))


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
routerA.printRoutingTable()
routerC.printConnections()
Router.printRoutingTable()
Router.printConnections()
