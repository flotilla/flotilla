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

import argparse
import logging
import sys

from flotilla.config import Config
from flotilla.dnsmasq.config import Config as DnsmasqConfig
from flotilla.dnsmasq.dhcp_range import DHCPRange
from flotilla.kubernetes.control import control_loop

LOG = logging.getLogger(__name__)


def _setup_logger(debug=False):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    log_handler = logging.StreamHandler(sys.stdout)
    fmt = logging.Formatter(fmt='%(asctime)s %(threadName)s %(name)s '
                            '%(levelname)s: %(message)s',
                            datefmt='%F %H:%M:%S')
    log_handler.setFormatter(fmt)
    logger.addHandler(log_handler)


def run(config):

    # add a dummy config for now
    r = DHCPRange('192.168.0.10', '192.168.0.20', '12h')
    c = DnsmasqConfig(interfaces='eth2', dhcp_range=r)
    c.persist()

    control_loop()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-c', '--config', required=True)
    args = parser.parse_args()

    _setup_logger(args.debug)

    config = Config.factory(args.config)
    LOG.debug("Running with config: %s" % config)

    run(config)


if __name__ == '__main__':
    main()
