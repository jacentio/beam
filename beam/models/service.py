from beam.models import BeamObject


ATTR_TYPES = {"id": str,
              "name": str,
              "ip": str,
              "port": int,
              "tags": list,
              "attrs": dict,
              "proto": str}


class Service(BeamObject):

    def validate(self):
        for k, v in ATTR_TYPES.iteritems():
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
