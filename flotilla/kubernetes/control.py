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
import pprint

try:
    from Queue import Queue
except ImportError:
    from queue import Queue

from threading import Thread

from flotilla.dnsmasq.hosts_config import HostsConfig
from flotilla.drivers import ManagementDriverFactory
from flotilla.kubernetes.host_spec import HostSpecFactory

from kubernetes import client, config, watch

LOG = logging.getLogger(__name__)


def update_hosts(event_queue):

    known_hosts = {}

    while True:
        dhcp_dirty = False
        event = event_queue.get()
        LOG.debug("Received an API event: %s" % pprint.pformat(event))

        uid = event['object']['metadata']['uid']
        host = HostSpecFactory.from_dict(event['object']['spec'])

        if event.get('type') == 'ADDED' or event.get('type') == 'MODIFIED':
            known_hosts[uid] = host
            dhcp_dirty = True
        elif uid in known_hosts and event.get('type') == 'DELETED':
            del(known_hosts[uid])
            dhcp_dirty = True

        if dhcp_dirty:
            LOG.debug("Persisting the configuration")
            HostsConfig(hosts=known_hosts.values()).persist()

            driver_name = host.management_driver
            driver = ManagementDriverFactory.get_driver(driver_name,
                                                        {"host": host})
            if not driver:
                LOG.error("Failed to get driver with name: %s", driver_name)
                continue

            LOG.info("Rebooting host '%s' with pxe= True" % host.hostname)
            driver.reboot(pxe=True)


def control_loop(config_file='flotilla-hosts.conf'):

    try:
        config.load_incluster_config()
    except Exception as e:
        LOG.warning("Failed to load in-cluster config. "
                    "Trying environment. Error: %s", e)
        config.load_kube_config()

    crds = client.CustomObjectsApi()

    event_queue = Queue()
    update_thread = Thread(target=update_hosts, args=(event_queue,))
    update_thread.daemon = True
    update_thread.start()

    LOG.debug("Starting watch loop")
    while True:
        stream = watch.Watch().stream(
            crds.list_cluster_custom_object,
            "stable.flotilla.io",
            "v1",
            "pxehosts")
        LOG.debug("Received stream data from API server.")
        for event in stream:
            LOG.debug("Putting event on queue: %s" % pprint.pformat(event))
            event_queue.put(event)
