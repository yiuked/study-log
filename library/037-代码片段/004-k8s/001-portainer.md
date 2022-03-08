portainer是一个管理Docker的WEB工具,K8S中POD定义

```
apiVersion: v1
kind: Service
metadata:
  name: basic-portainer
  labels:
    app: basic
spec:
  ports:
    - port: 9000
  selector:
    app: basic
    tier: portainer
  type: LoadBalancer
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: basic-portainer
  labels:
    app: basic
spec:
  selector:
    matchLabels:
      app: basic
      tier: portainer
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: basic
        tier: portainer
    spec:
      containers:
      - name: portainer-leader
        image: "portainer/portainer"
        ports:
        - containerPort: 9000
        volumeMounts:
        - name: docker-sock
          mountPath: /var/run/docker.sock
        - name: portainer-persistent-storage
          mountPath: /data
      volumes:
      - name: docker-sock
        hostPath:
          path: /var/run/docker.sock
      - name: portainer-persistent-storage
        hostPath:
          path: /run/desktop/mnt/host/d/v/data/portainer
          type: DirectoryOrCreate

```

