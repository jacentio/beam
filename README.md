Beam
====================

[![Build Status](https://travis-ci.org/jacentio/beam.svg?branch=master)](https://travis-ci.org/jacentio/beam)
[![codecov](https://codecov.io/gh/jacentio/beam/branch/master/graph/badge.svg)](https://codecov.io/gh/jacentio/beam)

Beam is a flexible Docker service discovery tool. It periodically polls the locally running Docker containers then submits that data to one or more backend registries. 

The only backend registry currently supported is EtcD, although contributions are welcome for others.

## Running Beam ##

`docker run -d --name=beam --net=host --volume=/var/run/docker.sock:/tmp/docker.sock beam --drivers etcd`

## Development Usage ##

Beam can be ran by cloning the repo and running;

`python ./scripts/run.py --socket /var/run/docker.sock`

A full list of supported arguments can be found here;

`python ./scripts/run.py --help`
