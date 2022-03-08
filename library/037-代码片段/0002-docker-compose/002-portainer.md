```
version: '3'

services:
    docker.portainer:
        container_name: docker.portainer
        image: portainer/portainer
        volumes:
         - /var/run/docker.sock:/var/run/docker.sock
         - ./data:/data
        ports:
         - 9000:9000
        restart: always

```

