#!/bin/python3

def updateRoutingTable(oldRib, dest, destMask, nextHop, distance):
    oldRib.append((dest, destMask, nextHop, distance))
    return oldRib


def printRoutingTable(rib):
    for elem in rib:
        destination = str(elem[0]) + "/" + str(elem[1])
        print(destination, "via", elem[2], "[distance:", str(elem[3])+"]")


rib = updateRoutingTable([], "192.168.4.0", "24", "192.168.1.2", 2)
printRoutingTable(rib)
