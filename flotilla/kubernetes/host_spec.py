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

import stringcase


class HostSpec(object):

    def __init__(self, hostname, mac_address, ip_address, image,
                 management_driver=None, management_address=None,
                 management_username=None, management_password=None):
        self.hostname = hostname
        self.mac_address = mac_address
        self.ip_address = ip_address
        self.image = image
        self.management_driver = management_driver
        self.management_address = management_address
        self.management_username = management_username
        self.management_password = management_password


def snakecase_dict(data):
    newdata = {}

    for k, v in data.items():
        if isinstance(v, dict):
            v = snakecase_dict(v)
        newdata[stringcase.snakecase(k)] = v

    return newdata


class HostSpecFactory(object):

    @staticmethod
    def from_dict(data):
        newdata = snakecase_dict(data)
        return HostSpec(**newdata)
