import os
import json
import etcd
from beam.models.driver import Driver


class Etcd(Driver):

    def __init__(self):
        self.init_client()

    def init_client(self):
        etcd_cfg = self.build_cfg()

        if etcd_cfg:
            self.client = etcd.Client(**etcd_cfg)
        else:
            self.client = etcd.Client()

    def build_cfg(self):
        cfg = {}

        for attr in [
            'host',
            'port',
            'protocol',
            'srv_domain',
            'version_prefix',
                'allow_redirect']:
            try:
                cfg[attr] = os.environ['ETCD_{}'.format(attr.capitalize())]
            except KeyError:
                pass

        return cfg

    def add(self, service, ttl):
        etcd_key = '/services/{}/{}'.format(service.name, service.id)

        self.client.write('{}/ip'.format(etcd_key), service.ip, ttl=ttl)
        self.client.write('{}/port'.format(etcd_key), service.port, ttl=ttl)
        self.client.write('{}/proto'.format(etcd_key), service.proto, ttl=ttl)
        self.client.write(
            '{}/attributes'.format(etcd_key),
            json.dumps(
                service.attrs),
            ttl=ttl)
        self.client.write(
            '{}/tags'.format(etcd_key),
            json.dumps(
                service.tags),
            ttl=ttl)
