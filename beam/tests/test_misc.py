import pytest
import logging
import docker


@pytest.fixture
def working_client():
    import beam
    b = beam.Beam(["--socket", "/var/run/docker.sock", "--internal"])

    yield b

    conts = b.dc.containers.list(filters={"label": "BEAM_TEST_TYPE=ephemeral"})
    [cont.remove(force=True) for cont in conts]


def test_logger(working_client):
    assert isinstance(working_client.log, logging.Logger)


def test_docker_client(working_client):
    assert isinstance(working_client.dc, docker.DockerClient)


def test_empty_drivers_list(working_client):
    assert len(working_client.drivers) == 0
