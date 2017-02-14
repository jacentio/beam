Beam
====================

Beam is a (WIP) flexible Docker service discovery tool. It periodically polls the locally running Docker containers then submits that data to one or more backend registries. 

The current priority is an EtcD backend registry, although contributions are welcome for others.

## Development Usage ##

Beam can be ran by cloning the repo and running;

`python ./scripts/run.py --socket /var/run/docker.sock`

A full list of supported arguments can be found here;

`python ./scripts/run.py --help`
