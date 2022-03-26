https://github.com/AliyunContainerService/k8s-for-docker-desktop


提示以下错误时的处理方式:

> persistentvolumes is forbidden: User "system:serviceaccount:kube-system:default" cannot create resource "persistentvolumes" in API group "" at the cluster scope

1. 清理旧提权

    ```
    kubectl delete clusterrolebinding serviceaccount-cluster-admin
    ```

2. 创建集群用户

    ```
    kubectl create clusterrolebinding serviceaccount-cluster-admin   --clusterrole=cluster-admin   --user=system:serviceaccount:kubernetes-dashboard:kubernetes-dashboard
    ```

3. 查看token

   ```
   kubectl  describe  secrets  -n kubernetes-dashboard
   ```

   
#### 安装面板

加载yaml文件

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.4.0/aio/deploy/recommended.yaml
```

获取登录token

```
$TOKEN=((kubectl -n kube-system describe secret default | Select-String "token:") -split " +")[1]
kubectl config set-credentials docker-desktop --token="${TOKEN}"
echo $TOKEN
```

http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/

mysql.yaml

```
apiVersion: v1
kind: Service
metadata:
  name: basic-mysql
  labels:
    app: basic
spec:
  type: LoadBalancer
  ports:
    - port: 3306
      targetPort: 3306
  selector:
    app: basic
    tier: mysql
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: basic-mysql
  labels:
    app: basic
spec:
  selector:
    matchLabels:
      app: basic
      tier: mysql
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: basic
        tier: mysql
    spec:
      containers:
      - image: mysql:8.0.26
        name: mysql
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: "123456"
        ports:
        - containerPort: 3306
          name: mysql
        volumeMounts:
        - name: mysql-persistent-storage
          mountPath: /var/lib/mysql
      volumes:
      - name: mysql-persistent-storage
        hostPath:
          path: /run/desktop/mnt/host/d/v/k8s/data
```

# windows docker desktop 设置2375端口远程访问

netsh interface portproxy add v4tov4 listenport=2375 connectaddress=127.0.0.1 connectport=2375 listenaddress=<your-public-ip> protocol=tcp
