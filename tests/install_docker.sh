#!/bin/bash -x

# Copyright 2016 go-dockerclient authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

if [[ $TRAVIS_OS_NAME == "linux" ]]; then
	sudo stop docker || true
	sudo rm -rf /var/lib/docker
	sudo rm -f `which docker`

	set -e
	sudo apt-get update
	sudo apt-get install -y --no-install-recommends \
		linux-image-extra-$(uname -r) \
		linux-image-extra-virtual
	sudo apt-get install -y --no-install-recommends \
		apt-transport-https \
		ca-certificates \
		curl \
		software-properties-common
	curl -fsSL https://apt.dockerproject.org/gpg | sudo apt-key add -
	sudo add-apt-repository \
		"deb https://apt.dockerproject.org/repo/ \
		ubuntu-$(lsb_release -cs) \
		main"
	sudo apt-get update
	sudo apt-get -y install docker-engine
	sudo start docker || true
fi
