from . import BeamObject


class Driver(BeamObject):

    def add(self, service, ttl):
        raise NotImplementedError(
            'The add function should be defined at a backend driver level.')
