# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2018, Craig Tracey <craigtracey@gmail.com>
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations


class DHCPHost(object):

    def __init__(self, mac, ipv4, hostname, lease='infinite'):
        self.mac = mac
        self.ipv4 = ipv4
        self.hostname = hostname
        self.lease = lease

    def __str__(self):
        return ",".join([self.mac, self.ipv4, self.hostname, self.lease])

    def __hash__(self):
        return (hash(self.mac) + hash(self.ipv4))
