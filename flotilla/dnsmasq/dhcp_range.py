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


class DHCPRange(object):

    def __init__(self, start_ipv4, end_ipv4, lease='24h'):
        self.start_ipv4 = start_ipv4
        self.end_ipv4 = end_ipv4
        self.lease = lease

    def __str__(self):
        return ",".join([self.start_ipv4, self.end_ipv4, self.lease])
