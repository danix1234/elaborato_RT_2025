#!/bin/python3

class RoutingTable():
    def __init__(self):
        self.destination = []
        self.nextHop = []
        self.distance = []

    def __str__(self, router):
        res = f"Routing Table of {router.name}:"
        for i, dest in enumerate(self.destination):
            nextHop = self.nextHop[i]
            nextRouter = Router.findRouter(nextHop).name
            distance = self.distance[i]
            res += f'\n{dest} via ({nextRouter}) {nextHop}, [{distance}]'
        return res

    def update(self, destination, nextHop, distance):
        if destination in self.destination:
            i = self.destination.index(destination)
            if self.distance[i] < distance:
                return False
            if self.nextHop[i] == nextHop and self.distance[i] == distance:
                return False
            self.nextHop[i] = nextHop
            self.distance[i] = distance
        else:
            self.destination.append(destination)
            self.nextHop.append(nextHop)
            self.distance.append(distance)
        return True


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

    def getConnectedIndexes(self):
        indexes = []
        for i, conn1 in enumerate(Router.connectionSide1):
            conn2 = Router.connectionSide2[i]
            if conn1 in self.ipaddr or conn2 in self.ipaddr:
                indexes.append(i)
        return indexes

    def getNeighbors(self):
        neighbors = {}
        for i in self.getConnectedIndexes():
            conn1 = Router.connectionSide1[i]
            conn2 = Router.connectionSide2[i]
            conn = conn1
            if conn1 in self.ipaddr:
                conn = conn2
            neighbors[Router.findRouter(conn)] = conn
        return neighbors

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
            print(self.routingTable.__str__(self))

    def initRoutingTables(self=None):
        if self is None:
            for router in Router.routers:
                router.initRoutingTables()
        else:
            for i in self.getConnectedIndexes():
                network = Router.connectionNetwork[i]
                conn1 = Router.connectionSide1[i]
                conn2 = Router.connectionSide2[i]
                conn = conn1
                if conn2 in self.ipaddr:
                    conn = conn2
                self.routingTable.update(network, conn, 0)


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
print("Routers:")
print(routerA)
print(routerB)
print(routerC)
print(routerD)
print()
Router.printConnections()
print()
Router.initRoutingTables()
Router.printRoutingTable()
