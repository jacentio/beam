import pytest
import logging
import docker


@pytest.fixture
def working_client():
    import beam
    b = beam.Beam(["--socket", "/var/run/docker.sock"])

    yield b

    conts = b.dc.containers.list()
    [cont.remove(force=True) for cont in conts]


def test_logger(working_client):
    assert isinstance(working_client.log, logging.Logger)


def test_docker_client(working_client):
    assert isinstance(working_client.dc, docker.DockerClient)


def test_empty_drivers_list(working_client):
    assert len(working_client.drivers) == 0


def test_registering_no_published_services(working_client):
    container = working_client.dc.containers.run("redis", detach=True)

    services = working_client.get_services_to_register(container.attrs)

    assert len(services) == 0


def test_registering_published_services(working_client):
    container = working_client.dc.containers.run(
        "redis", detach=True, ports={'6379/tcp': 16379})

    services = working_client.get_services_to_register(container.attrs)

    assert len(services) == 1

    service = services[0]

    assert service.port == 16379
    assert service.proto == "tcp"

    tags = working_client.get_service_tags(service, container.attrs)
    assert len(tags) == 0

    attrs = working_client.get_service_attributes(service, container.attrs)
    assert len(attrs.keys()) == 0


def test_registering_published_service_with_default_tag(working_client):
    container = working_client.dc.containers.run(
        "redis",
        detach=True,
        ports={
            '6379/tcp': 16379},
        labels={
            "BEAM_TAGS": "foo"})

    services = working_client.get_services_to_register(container.attrs)

    assert len(services) == 1

    service = services[0]

    assert service.port == 16379
    assert service.proto == "tcp"

    tags = working_client.get_service_tags(service, container.attrs)
    assert len(tags) == 1
    assert tags[0] == "foo"

    attrs = working_client.get_service_attributes(service, container.attrs)
    assert len(attrs.keys()) == 0


def test_registering_published_service_with_default_and_service_tag(
        working_client):
    container = working_client.dc.containers.run(
        "redis",
        detach=True,
        ports={
            '6379/tcp': 16379},
        labels={
            "BEAM_TAGS": "foo",
            "BEAM_6379_TCP_TAGS": "bar"})

    services = working_client.get_services_to_register(container.attrs)

    assert len(services) == 1

    service = services[0]

    assert service.port == 16379
    assert service.proto == "tcp"

    tags = working_client.get_service_tags(service, container.attrs)
    assert len(tags) == 2
    assert "foo" in tags
    assert "bar" in tags

    attrs = working_client.get_service_attributes(service, container.attrs)
    assert len(attrs.keys()) == 0


def test_registering_published_service_with_default_attributes(working_client):
    container = working_client.dc.containers.run(
        "redis",
        detach=True,
        ports={
            '6379/tcp': 16379},
        labels={
            "BEAM_TESTING": "foo"})

    services = working_client.get_services_to_register(container.attrs)

    assert len(services) == 1

    service = services[0]

    assert service.port == 16379
    assert service.proto == "tcp"

    tags = working_client.get_service_tags(service, container.attrs)
    assert len(tags) == 0

    attrs = working_client.get_service_attributes(service, container.attrs)
    assert len(attrs.keys()) == 1
    assert attrs["TESTING"] == "foo"


def test_registering_published_service_with_default_and_service_attributes(
        working_client):
    container = working_client.dc.containers.run(
        "redis",
        detach=True,
        ports={
            '6379/tcp': 16379},
        labels={
            "BEAM_TESTING": "foo",
            "BEAM_6379_TCP_TESTING": "bar"})

    services = working_client.get_services_to_register(container.attrs)

    assert len(services) == 1

    service = services[0]

    assert service.port == 16379
    assert service.proto == "tcp"

    tags = working_client.get_service_tags(service, container.attrs)
    assert len(tags) == 0

    attrs = working_client.get_service_attributes(service, container.attrs)
    assert len(attrs.keys()) == 1
    assert attrs["TESTING"] == "bar"


def test_registering_published_service_with_default_and_service_attributes_mix(
        working_client):
    container = working_client.dc.containers.run("redis", detach=True, ports={'6379/tcp': 16379}, labels={"BEAM_TESTING": "foo", "BEAM_6379_TCP_TESTING": "bar", "BEAM_SHARED": "test_shared", "BEAM_6379_TCP_DEDICATED": "test_dedicated"})

    services = working_client.get_services_to_register(container.attrs)

    assert len(services) == 1

    service = services[0]

    assert service.port == 16379
    assert service.proto == "tcp"

    tags = working_client.get_service_tags(service, container.attrs)
    assert len(tags) == 0

    attrs = working_client.get_service_attributes(service, container.attrs)
    assert len(attrs.keys()) == 3
    assert attrs["TESTING"] == "bar"
    assert attrs["SHARED"] == "test_shared"
    assert attrs["DEDICATED"] == "test_dedicated"
