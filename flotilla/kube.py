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

try:
    from Queue import Queue
except:
    from queue import Queue

from threading import Thread

from flotilla.dnsmasq.dhcp_host import DHCPHost
from flotilla.dnsmasq.hosts_config import HostsConfig

from kubernetes import client, config, watch

LOG = logging.getLogger(__name__)


def update_hosts(event_queue):

    known_hosts = {}

    while True:
        dirty = False
        event = event_queue.get()
        LOG.debug("Received API event: %s" % event)

        uid = event['object']['metadata']['uid']

        if event.get('type') == 'ADDED' or event.get('type') == 'MODIFIED':
            mac = event['object']['spec']['macAddress']
            ipv4 = event['object']['spec']['ipAddress']
            hostname = event['object']['spec']['hostname']
            host = DHCPHost(mac, ipv4, hostname)

            known_hosts[uid] = host
            dirty = True
        elif uid in known_hosts and event.get('type') == 'DELETED':
            del(known_hosts[uid])
            dirty = True

        if dirty:
            LOG.debug("Persisting the configuration")
            HostsConfig(hosts=known_hosts.values()).persist()


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
        LOG.debug("FOOOO")
        stream = watch.Watch().stream(
            crds.list_cluster_custom_object,
            "stable.flotilla.io",
            "v1",
            "pxehosts")
        LOG.debug("Received stream data from API server.")
        for event in stream:
            LOG.debug("Putting event on queue")
            event_queue.put(event)
