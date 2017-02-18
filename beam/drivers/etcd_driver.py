import os
import json
import etcd
from beam.models.driver import Driver


class Etcd(Driver):

    def __init__(self):
        super(Etcd, self).__init__()
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
                cfg[attr] = os.environ['ETCD_{}'.format(attr.upper())]
            except KeyError:
                if attr == 'port':
                    cfg[attr] = 2379 ## Set the default ETCD port if it's not provided
                pass

        return cfg

    def add(self, service, ttl):

        etcd_key = '/services/{}'.format(service.name)

        self.client.write('{}/containers/{}/ip'.format(etcd_key,
                                                       service.id),
                          service.ip,
                          ttl=ttl)
        self.client.write(
            '{}/containers/{}/port'.format(etcd_key, service.id),
            service.port, ttl=ttl)
        self.client.write(
            '{}/containers/{}/proto'.format(etcd_key, service.id),
            service.proto, ttl=ttl)
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
