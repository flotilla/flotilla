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

import os

from flotilla.dnsmasq import CONFIG_PATH, DEFAULT_TFTP_ROOT

from jinja2 import BaseLoader, Environment

CONFIG_TMPL = '''
{% if interfaces == 'all' %}
bind-interfaces
{% else %}
interface={{ interfaces }}
{% endif %}
{% if tftp_enabled -%}
enable-tftp
tftp-root={{ tftp_root }}
{%- endif %}
{%- if dhcp_range %}
dhcp-range={{ dhcp_range }}
{% endif -%}
{%- for dhcp_host in dhcp_hosts -%}
dhcp-host={{ dhcp_host }}
{%- endfor %}

dhcp-match=ipxe,175
dhcp-boot=tag:#ipxe,ipxe.pxe
dhcp-boot=tag:ipxe,flotilla/flotilla.ipxe

log-dhcp
'''


class Config(object):

    def __init__(self, interfaces='all', dhcp_range=None, dhcp_hosts=[],
                 tftp_enabled=True, tftp_root=DEFAULT_TFTP_ROOT):
        self.interfaces = interfaces
        self.dhcp_range = dhcp_range
        self.dhcp_hosts = dhcp_hosts
        self.tftp_enabled = tftp_enabled
        self.tftp_root = tftp_root

    def persist(self, filename=os.path.join(CONFIG_PATH, "flotilla.conf")):
        template = Environment(loader=BaseLoader()).from_string(CONFIG_TMPL)
        output = template.render(self.__dict__)

        with open(filename, 'w') as fh:
            fh.write(output)

        # FIXME: this really belongs as its own thing
        ipxe_config = os.path.join(DEFAULT_TFTP_ROOT, "flotilla/flotilla.ipxe")
        with open(ipxe_config, "w") as fh:
            conf = "#!ipxe\n\nchain http://192.168.1.10:8081/boot.ipxe"  # noqa
            fh.write(conf)
