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

from abc import abstractmethod, ABCMeta
from stevedore.driver import DriverManager

MANAGEMENT_DRIVER_NAMESPACE = "flotilla.management.drivers"
LOG = logging.getLogger(__name__)


class ManagementDriver(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def power_on(self):
        return

    @abstractmethod
    def power_off(self):
        return

    @abstractmethod
    def reboot(self, pxe=False):
        return


class ManagementDriverFactory(object):

    @staticmethod
    def get_driver(driver_name, kwargs={}):
        driver_mgr = DriverManager(namespace=MANAGEMENT_DRIVER_NAMESPACE,
                                   name=driver_name,
                                   invoke_kwds=kwargs,
                                   invoke_on_load=True)
        return driver_mgr.driver
