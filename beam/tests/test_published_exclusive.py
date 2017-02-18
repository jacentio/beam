import pytest
import logging
import docker


@pytest.fixture
def working_client():
    import beam
    b = beam.Beam(["--socket", "/var/run/docker.sock", "--exclusive"])

    yield b

    conts = b.dc.containers.list()
    [cont.remove(force=True) for cont in conts]


def test_registering_no_published_services(working_client):
    container = working_client.dc.containers.run("redis", detach=True)

    services = working_client.get_services_to_register(container.attrs)

    assert len(services) == 0


def test_registering_published_excluded_services(working_client):
    container = working_client.dc.containers.run(
        "redis", detach=True, ports={'6379/tcp': 16379})

    services = working_client.get_services_to_register(container.attrs)

    assert len(services) == 0


def test_registering_published_included_services_miss(working_client):
    container = working_client.dc.containers.run(
        "redis", detach=True, ports={'6379/tcp': 16379}, labels={"BEAM_PORTS": "36379/tcp"})

    services = working_client.get_services_to_register(container.attrs)

    assert len(services) == 0


def test_registering_published_included_services(working_client):
    container = working_client.dc.containers.run(
        "redis", detach=True, ports={'6379/tcp': 16379}, labels={"BEAM_PORTS": "6379/tcp"})

    services = working_client.get_services_to_register(container.attrs)

    assert len(services) == 1

    service = services[0]
    assert service.port == 16379
    assert service.proto == "tcp"
