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

from flotilla.drivers import ManagementDriver

from amt.client import Client

LOG = logging.getLogger(__name__)


class AMTManagementDriver(ManagementDriver):

    def __init__(self, host):
        self.host = host
        self._client = Client(address=host.management_address,
                              password=host.management_password,
                              username=host.management_username)

    def power_on(self):
        LOG.debug("Powering on host %s" % (self.host.hostname))
        self._client.power_on()

    def power_off(self):
        LOG.debug("Powering off host %s" % (self.host.hostname))
        self._client.power_off()

    def reboot(self, pxe=False):
        LOG.debug("Rebooting host %s pxe: %s" % (self.host.hostname, pxe))
        if pxe:
            self._client.pxe_next_boot()

        self._client.power_cycle()
