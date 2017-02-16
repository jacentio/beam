import argparse
import docker
from importlib import import_module
from time import time, sleep
from logging import getLogger

from beam.models.service import Service


class Beam(object):
    EXCLUDED_ATTRIBUTES = [
        'TAGS'
    ]

    def __init__(self):
        self.log = getLogger()
        self.args = self.parse_args()
        self.init_drivers()
        self.init_client()

    def init_client(self):
        self.log.debug(
            'Initiating Docker client, using {}'.format(
                self.args.socket))
        self.dc = docker.DockerClient(
            base_url='unix://{}'.format(self.args.socket))
        return self.dc

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description='Flexible Docker Service Discovery')
        parser.add_argument('--drivers', nargs='+')
        parser.add_argument('--hostname', action="store", dest="hostname")
        parser.add_argument(
            '--inclusive',
            dest='inclusive',
            action='store_false')
        parser.add_argument('--internal', dest='internal', action='store_true')
        parser.add_argument('--socket', action="store", dest="socket")
        parser.add_argument('--ttl', action="store", dest="ttl")

        parser.set_defaults(drivers=[])
        parser.set_defaults(hostname=self.get_ip_address())
        parser.set_defaults(inclusive=True)
        parser.set_defaults(internal=False)
        parser.set_defaults(socket="/tmp/docker.sock")
        parser.set_defaults(ttl=30)

        return parser.parse_args()

    def get_ip_address(self):
        return '192.168.1.1'

    def import_driver(self, d):
        self.log.debug('Initiating {} backend driver'.format(d))
        p = 'beam.drivers.{}_driver'.format(d.lower())

        mod = import_module(p)
        met = getattr(mod, d.capitalize())

        return met()

    def init_drivers(self):
        self.drivers = []
        for d in self.args.drivers:
            self.drivers.append(self.import_driver(d))

    def get_services_to_register(self, container):
        services = []
        only_services = []

        if not self.args.inclusive:
            if 'BEAM_PORTS' not in container['Config']['Labels']:
                return services
            else:
                only_services = [
                    x if '/' in x else '{}/tcp'.format(x) for x in
                    container['Config']['Labels']['BEAM_PORTS']]

        if self.args.internal:
            for service in container['Config']['ExposedPorts'].keys():
                if only_services and service not in only_services:
                    continue

                (container_port, proto) = service.split('/')

                s = Service()
                try:
                    s.name = container['Config']['Labels'][
                        'com.docker.swarm.service.id']
                except KeyError:
                    s.name = '{}-{}'.format(
                        container['Name'].lstrip('/'), container_port)
                s.ip = self.args.hostname
                s.port = container_port
                s.proto = proto
                s.id = container['Config']['Hostname']

                services.append(s)
        else:
            for service, cfg in container[
                    'NetworkSettings']['Ports'].iteritems():
                try:
                    cfg = cfg[0]
                except TypeError:
                    continue
                if only_services and service not in only_services:
                    continue

                (container_port, proto) = service.split('/')

                s = Service()
                try:
                    s.name = container['Config']['Labels'][
                        'com.docker.swarm.service.id']
                except KeyError:
                    s.name = '{}-{}'.format(
                        container['Name'].lstrip('/'), container_port)
                s.ip = self.args.hostname
                s.port = cfg['HostPort']
                s.proto = proto
                s.id = container['Config']['Hostname']

                services.append(s)

        return services

    def get_service_attributes(self, service, container):
        attributes = {}

        s = service.name.split('-')
        container_port = s[-1]

        for k, v in container['Config']['Labels'].iteritems():
            if k.startswith('BEAM_') and not k[5].isdigit():
                attr_key = k.replace('BEAM_', '')

                if attr_key in Beam.EXCLUDED_ATTRIBUTES:
                    continue

                attributes[attr_key] = v

        for k, v in container['Config']['Labels'].iteritems():
            if k.startswith(
                'BEAM_{}_{}'.format(
                    container_port,
                    service.proto.upper())):
                attr_key = k.replace(
                    'BEAM_{}_{}_'.format(
                        container_port,
                        service.proto.upper()), '')

                if attr_key in Beam.EXCLUDED_ATTRIBUTES:
                    continue

                attributes[attr_key] = v

        return attributes

    def get_service_tags(self, service, container):
        tags = set()

        s = service.name.split('-')
        container_port = s[-1]

        try:
            tags |= set(container['Config']['Labels']['BEAM_TAGS'].split(','))
        except KeyError:
            pass

        try:
            tags |= set(
                container['Config']['Labels'][
                    'BEAM_{}_{}_TAGS'.format(
                        container_port,
                        service.proto.upper())].split('/'))
        except KeyError:
            pass

        return list(tags)

    def register_container(self, container):
        services = self.get_services_to_register(container)

        for service in services:
            service.attrs = self.get_service_attributes(service, container)
            service.tags = self.get_service_tags(service, container)

            [driver.add(service, self.args.ttl) for driver in self.drivers]

    def run(self):
        while True:
            start = time()
            containers = self.dc.containers.list(filters={'status': 'running'})
            [self.register_container(x.attrs) for x in containers]
            end = time()

            duration = end - start
            self.log.debug('Registration run took {}s'.format(duration))
            sleep_time = int(self.args.ttl - duration) - 5
            self.log.debug('Sleeping for {}s'.format(sleep_time))
            sleep(sleep_time)
