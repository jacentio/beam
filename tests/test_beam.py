import pytest
import logging
import docker
import json

@pytest.fixture
def working_published_beam():
	import beam
	return beam.Beam(["--socket", "/var/run/docker.sock"])

@pytest.fixture
def working_exposed_beam():
	import beam
	return beam.Beam(["--socket", "/var/run/docker.sock", "--internal"])

def test_logger(working_published_beam):
	assert isinstance(working_published_beam.log, logging.Logger)

def test_docker_client(working_published_beam):
	assert isinstance(working_published_beam.dc, docker.DockerClient)

def test_empty_drivers_list(working_published_beam):
	assert len(working_published_beam.drivers) == 0

def test_registering_no_published_services(working_published_beam):
	container = working_published_beam.dc.containers.run("redis", detach=True)

	services = working_published_beam.get_services_to_register(container.attrs)

	container.remove(force=True)

        assert len(services) == 0

def test_registering_published_services(working_published_beam):
	container = working_published_beam.dc.containers.run("redis", detach=True, ports={'6379/tcp': 16379})

	services = working_published_beam.get_services_to_register(container.attrs)

	container.remove(force=True)

        assert len(services) == 1

	service = services[0]

	assert service.port == 16379
	assert service.proto == "tcp"

	tags = working_published_beam.get_service_tags(service, container.attrs)
	assert len(tags) == 0

	attrs = working_published_beam.get_service_attributes(service, container.attrs)
	assert len(attrs.keys()) == 0

def test_registering_published_servicewith_default_tag(working_published_beam):
	container = working_published_beam.dc.containers.run("redis", detach=True, ports={'6379/tcp': 16379}, labels={"BEAM_TAGS": "foo"})

	services = working_published_beam.get_services_to_register(container.attrs)

	container.remove(force=True)

        assert len(services) == 1

	service = services[0]

	assert service.port == 16379
	assert service.proto == "tcp"

	tags = working_published_beam.get_service_tags(service, container.attrs)
	assert len(tags) == 1
	assert tags[0] == "foo"

	attrs = working_published_beam.get_service_attributes(service, container.attrs)
	assert len(attrs.keys()) == 0

def test_registering_published_servicewith_default_and_service_tag(working_published_beam):
	container = working_published_beam.dc.containers.run("redis", detach=True, ports={'6379/tcp': 16379}, labels={"BEAM_TAGS": "foo", "BEAM_6379_TCP_TAGS": "bar"})

	services = working_published_beam.get_services_to_register(container.attrs)

	container.remove(force=True)

        assert len(services) == 1

	service = services[0]

	assert service.port == 16379
	assert service.proto == "tcp"

	tags = working_published_beam.get_service_tags(service, container.attrs)
	assert len(tags) == 2
	assert "foo" in tags
	assert "bar" in tags

	attrs = working_published_beam.get_service_attributes(service, container.attrs)
	assert len(attrs.keys()) == 0

def test_registering_no_exposed_services(working_exposed_beam):
	container = working_exposed_beam.dc.containers.run("redis", detach=True)

	services = working_exposed_beam.get_services_to_register(container.attrs)

	container.remove(force=True)

        assert len(services) == 1

	service = services[0]

	assert services[0].port == 6379
	assert services[0].proto == "tcp"

	tags = working_exposed_beam.get_service_tags(service, container.attrs)
	assert len(tags) == 0

	attrs = working_exposed_beam.get_service_attributes(service, container.attrs)
	assert len(attrs.keys()) == 0
