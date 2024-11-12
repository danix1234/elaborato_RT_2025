#!/bin/python3
"""
Python script to simulate the how the rip protocol works.
In particular, it allows to build a topolofy of n routers and for each router
    it allows to specify a list of mac addresses and ip address.
It also allows to simulate connections, altought the code isn't able to
    calculate the network ip value, thus it needs to be specified. Said
    networks must have a netmask of /24, since the number is hardcoded to have
    a complete output.
After the router topology is built, the script is able to have routers exchange
    their distance vectors, and for each iteration of such exchanges, it writes
    to output the content of each router Routing Table.

Notes: The topology isn't run through checks to make sure it's valid.
       Thus it is necessary to be sure the manual configuration of it is
       correct, otherwise the script may fail or report invalid results.
"""


class RoutingTable():
    """
    Class which contains all the routing entries for a specific router.
    A routing entry is made up of three values:
        - destination: a string representing the network id of destination
        - nextHop: a string representing the ip address of the next hop
        - distance: an integer representing the distance in amount of hops
    """

    def __init__(self):
        """
        Creates empty RoutingTable.
        """
        self.destination = []
        self.nextHop = []
        self.distance = []

    def __str__(self, router):
        """
        Pretty formatting of the Routing Table.
        """
        res = f"Routing Table of {router.name}:"
        for dest in sorted(self.destination):
            i = self.destination.index(dest)
            nextHop = self.nextHop[i]
            nextName = Router.findRouter(nextHop).name
            distance = self.distance[i]
            interface = router.findNick(nextHop)
            correctSide = nextHop in router.ipaddr
            if not correctSide:
                res += f'\n{dest}/24 [{distance}] via ({nextName}) {nextHop},'
            else:
                res += f'\n{dest}/24 is directly connected,'
            res += f' on {interface}'
        return res

    def update(self, destination, nextHop, distance):
        """
        Updates routing table if destination is missing, or if
        the new distance is inferior to the current one.
        """
        if destination in self.destination:
            i = self.destination.index(destination)
            if self.distance[i] <= distance:
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

    def updateAll(self, routingTable, nextHop):
        """
        Updates routing table with all the entries from an
        other routing table.
        """
        changes = False
        for i, destination in enumerate(routingTable.destination):
            distance = routingTable.distance[i] + 1
            changes |= self.update(destination, nextHop, distance)
        return changes


class Router():
    """
    Class which represents a single router in the topology.
    It also stores all routers, for semplicity.
    """
    routers = []
    connectionSide1 = []
    connectionSide2 = []
    connectionNetwork = []

    def __init__(self, name):
        """
        Create empty Router, with a name.
        """
        self.name = name
        self.nicks = []
        self.ipaddr = []
        self.routers.append(self)
        self.routingTable = RoutingTable()

    def __str__(self):
        """
        Pretty formatting for the router.
        """
        acc = f"Router {self.name}:\n"
        for i, nick in enumerate(self.nicks):
            ipAddr = self.ipaddr[i]
            acc += f"{nick} {ipAddr}\n"
        return acc

    def addNick(self, interfaceName, ipAddr):
        """
        To add a nick, with its interface name and the ip address.
        """
        self.nicks.append(interfaceName)
        self.ipaddr.append(ipAddr)

    def addConnection(ipAddrSelf, ipAddrOther, ipNetwork):
        """
        To establish a connection between two ip addresses.
        """
        Router.connectionSide1.append(ipAddrSelf)
        Router.connectionSide2.append(ipAddrOther)
        Router.connectionNetwork.append(ipNetwork)

    def findNick(self, nextHop):
        """
        Finds the nick of the router associated with the next hop.
        Note: the next hop can be either the ip address on the other
            side of the connection, or the ip address on this router
            side of the connection.
        """
        if nextHop in self.ipaddr:
            return self.nicks[self.ipaddr.index(nextHop)]
        if nextHop in Router.connectionSide1:
            connIndex = Router.connectionSide1.index(nextHop)
            conn = Router.connectionSide2[connIndex]
        if nextHop in Router.connectionSide2:
            connIndex = Router.connectionSide2.index(nextHop)
            conn = Router.connectionSide1[connIndex]
        return self.nicks[self.ipaddr.index(conn)]

    def findRouter(ipAddr):
        """
        Find the router which has the ip address specified.
        """
        for router in Router.routers:
            if ipAddr in router.ipaddr:
                return router

    def getConnectedIndexes(self):
        """
        Get a list of the index of all connected ip networks.
        """
        indexes = []
        for i, conn1 in enumerate(Router.connectionSide1):
            conn2 = Router.connectionSide2[i]
            if conn1 in self.ipaddr or conn2 in self.ipaddr:
                indexes.append(i)
        return indexes

    def getNeighbors(self):
        """
        Get a dictionary of all connected neightbors, with the ip address
            they have on the connection with this router.
        """
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
        """
        Pretty output for the established connection between all routers.
        Note: if self is not None it only shows the connections of this router.
        """
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
            print(f"({r1}) {conn} - ({r2}) {conn2}  -->  {connNetwork}/24")

    def printRoutingTable(self=None):
        """
        Pretty output for all the routing tables.
        Note: If self is not None it only shows this router routing table.
        """
        if self is None:
            for router in Router.routers:
                router.printRoutingTable()
        else:
            print(self.routingTable.__str__(self))

    def initRoutingTables(self=None):
        """
        Initialize all the routing tables with only the directly connected
        networks.
        Note: If self is not None it only initialize this router routing table.
        """
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

    def updateRoutingTable(self=None):
        """
        Update the routing table for all routers.
        Note: If self is not none, it only updates this router.
        """
        if self is None:
            changes = False
            for router in Router.routers:
                changes |= router.updateRoutingTable()
            return changes
        else:
            changes = False
            for router, nextHop in self.getNeighbors().items():
                selfRib = self.routingTable
                nearRib = router.routingTable
                changes |= selfRib.updateAll(nearRib, nextHop)
            return changes


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

# initialize the routing tables with the connected networks
print("\nINITIALIZATION:")
Router.initRoutingTables()
Router.printRoutingTable()

# keep updating distance until no more changes are made
phase = 0
while Router.updateRoutingTable():
    phase += 1
    print(f"\nPHASE {phase}")
    Router.printRoutingTable()
