import pytest
import logging
import docker


@pytest.fixture
def working_client():
    import beam
    b = beam.Beam(["--socket", "/var/run/docker.sock",
                   "--internal", "--drivers", "etcd"])

    yield b

    conts = b.dc.containers.list(filters={"label": "EPHEMERAL"})
    [cont.remove(force=True) for cont in conts]


def test_registered_driver(working_client):
    from beam.drivers.etcd_driver import Etcd

    assert len(working_client.drivers) == 1
    assert isinstance(working_client.drivers[0], Etcd)


def test_registering_no_published_services(working_client):
    container = working_client.dc.containers.run(
        "redis", detach=True, labels={"EPHEMERAL": "true"})

    working_client.register_container(container.attrs)
