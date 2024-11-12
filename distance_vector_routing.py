#!/bin/python3

class router():
    nicks = []
    ipaddr = []

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.nicks}, {self.ipaddr}'

    def addNick(self, interfaceName, ipAddr):
        """
        interfaceName and ipAddr must be relative to the same nick
        both interfaceName and ipAddr must be strings
        """
        self.nicks.append(interfaceName)
        self.ipaddr.append(ipAddr)
