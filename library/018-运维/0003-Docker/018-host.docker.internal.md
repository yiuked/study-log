### linux
docker
```
docker run -it --add-host=host.docker.internal:host-gateway ubuntu bash
```
docker-compose
```
version: "3.8"

services:

ubuntu:

image: ubuntu

container_name: ubuntu

extra_hosts:

- "host.docker.internal:host-gateway"

command: sleep infinity
```