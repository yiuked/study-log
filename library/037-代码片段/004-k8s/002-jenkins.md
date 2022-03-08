```
apiVersion: v1
kind: Service
metadata:
  name: jenkins-svc
  labels:
    app: jenkins
spec:
  ports:
    - name: http
      port: 8080  
    - name: agent
      port: 50000
  selector:
    app: jenkins
  type: LoadBalancer
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jenkins
spec:
  replicas: 1
  selector:
    matchLabels:
      app: jenkins
  template:
    metadata:
      labels:
        app: jenkins
    spec:
      serviceAccountName: jenkins
      containers:
      - name: jenkins
        image: jenkins/jenkins:lts-jdk11
        ports:
        - containerPort: 8080
          name: web
          protocol: TCP
        - containerPort: 50000
          name: agent
          protocol: TCP
        volumeMounts:
        - name: jenkins-home
          mountPath: /var/jenkins_home
        - name: docker-sock
          mountPath: /var/run/docker.sock
        - name: docker-bin
          mountPath: /usr/bin/docker
      volumes:
      - name: jenkins-home
        hostPath:
          path: /run/desktop/mnt/host/d/v/data/jenkins_home
          type: DirectoryOrCreate
      - name: docker-sock
        hostPath:
          path: /var/run/docker.sock
      - name: docker-bin
        hostPath:
          path: /usr/bin/docker
```

