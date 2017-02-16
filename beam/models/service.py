from beam.models import BeamObject


class Service(BeamObject):
    ATTR_TYPES = {"id": str,
                  "name": str,
                  "ip": str,
                  "port": int,
                  "tags": list,
                  "attrs": dict,
                  "proto": str}

    def __init__(self):
        self.id = None
        self.name = None
        self.ip = None
        self.port = None
        self.tags = []
        self.attrs = {}
        self.proto = "tcp"

    def validate(self):
        for k, v in Service.ATTR_TYPES.iteritems():
            var = getattr(self, k)
            if not isinstance(var, v):
                raise AttributeError(
                    "{} is a {} but should be a {}".format(
                        k, type(var), v))

    def generate_id(self):
        s = self.name.split('-')
        name = '-'.join(s[:-1])
        port = s[-1]

        service_id = "{ip}:{name}:{port}:{proto}".format(
            ip=self.ip, name=name, port=port, proto=self.proto)

        return service_id
