import pytest

from flotilla.dnsmasq.dhcp_host import DHCPHost


def test_dhcp_host_serialize():
    host = DHCPHost("aa:bb:cc:dd:ee:ff", "1.1.1.1", "hostname")
    assert str(host) == "aa:bb:cc:dd:ee:ff,1.1.1.1,hostname,infinite"
