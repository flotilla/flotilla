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

import logging
import os.path

from flotilla.dnsmasq import CONFIG_DIR

LOG = logging.getLogger(__name__)
FLOTILLA_HOSTS_CONFIG_FILE = "flotilla-hosts.conf"


class HostsConfig(object):

    def __init__(self, hosts=[], filename=FLOTILLA_HOSTS_CONFIG_FILE):
        self._hosts = set(hosts)
        self.filename = filename

    def add(self, host):
        LOG.debug("jjje")
        self._hosts.add(host)
        LOG.debug("KJKJHKJH")

    def remove(self, host):
        self._hosts.delete(host)

    def persist(self):
        filename = os.path.join(CONFIG_DIR, self.filename)
        filename = os.path.join("/tmp", self.filename)
        LOG.debug("Persisting hosts config to %s" % filename)
        with open(filename, 'w') as fh:
            for host in self._hosts:
                fh.write("dhcp-host=%s" % host)
