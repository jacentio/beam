import pytest
import logging
import docker

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
	working_published_beam.dc.images.pull("redis")
	container = working_published_beam.dc.containers.run("redis", detach=True)

	services = working_published_beam.get_services_to_register(container.attrs)

	container.remove(force=True)

        assert len(services) == 0

def test_registering_no_exposed_services(working_exposed_beam):
	working_exposed_beam.dc.images.pull("redis")
	container = working_exposed_beam.dc.containers.run("redis", detach=True)

	services = working_exposed_beam.get_services_to_register(container.attrs)

	container.remove(force=True)

        assert len(services) == 1
	assert services[0].port == 6379
	assert services[0].proto == "tcp"
