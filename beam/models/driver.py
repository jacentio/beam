from . import BeamObject


class Driver(BeamObject):

    def add(self, service):
        raise NotImplementedError(
            'The add function should be defined at a backend driver level.')

    def remove(self, service):
        raise NotImplementedError(
            'The remove function should be defined at a backend driver level.')
