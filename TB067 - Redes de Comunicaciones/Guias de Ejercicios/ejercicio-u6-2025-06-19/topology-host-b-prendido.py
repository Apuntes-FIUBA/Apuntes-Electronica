#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    def build(self, **_opts):
        # Add 2 routers in two different subnets
        rA = self.addHost('rA', cls=LinuxRouter, ip='10.0.0.1/24')
        rB = self.addHost('rB', cls=LinuxRouter, ip='10.1.0.1/24')

        # Add 2 switches
        sA = self.addSwitch('sA', dpid='00000001')
        sB = self.addSwitch('sB', dpid='00000002')
        sC = self.addSwitch('sC', dpid='00000003')

        # Add host-switch links in the same subnet
        self.addLink(sA,
                     rA,
                     intfName2='rA-eth1',
                     params2={'ip': '10.0.0.1/24'})

        self.addLink(sB,
                     rB,
                     intfName2='rB-eth1',
                     params2={'ip': '10.1.0.1/24'})

        # Add link in a new subnet for the router-router connection
        self.addLink(rA,
                     sC,
                     intfName1='rA-eth2',
                     params1={'ip': '10.100.0.1/24'})

        self.addLink(rB,
                     sC,
                     intfName1='rB-eth2',
                     params1={'ip': '10.100.0.2/24'})

        # Adding hosts specifying the default route
        hA = self.addHost(name='hA',
                          ip='10.0.0.251/24',
                          defaultRoute='via 10.0.0.1')
        hB = self.addHost(name='hB',
                          ip='10.1.0.252/24',
                          defaultRoute='via 10.1.0.1')

        # Add host-switch links
        self.addLink(hA, sA)
        self.addLink(hB, sB)


def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo)

    # Add routing for reaching networks that aren't directly connected
    info(net['rA'].cmd("ip route add 10.1.0.0/24 via 10.100.0.2 dev rA-eth2"))
    info(net['rB'].cmd("ip route add 10.0.0.0/24 via 10.100.0.1 dev rB-eth2"))

    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
