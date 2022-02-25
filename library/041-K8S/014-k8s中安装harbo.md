1. 创建命名空间

   ```
   kubectl create namespace harbor
   ```

https://github.com/goharbor/harbor-helm

```
apiVersion: v1
kind: Pod
metadata:
  name: kaniko
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:latest
    args:
    - "--dockerfile=<path to Dockerfile within the build context>"
    - "--context=s3://<bucket name>/<path to .tar.gz>"
    - "--destination=mycr.azurecr.io/my-repository:my-tag"
    envFrom:
    # when authenticating with service principal
    - secretRef:
        name: azure-secret
    volumeMounts:
    - name: docker-config
      mountPath: /kaniko/.docker/
  volumes:
  - name: docker-config
    configMap:
      name: docker-config
  restartPolicy: Never
```

