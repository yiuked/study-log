```
docker run \
  -u root \
  --rm \
  -d \
  -p 7001:8080 \
  -p 7002:50000 \
  -v jenkins-data:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkinsci/blueocean
```

```
apiVersion: v1
kind: Service
metadata:
  name: jenkins
spec:
  type: NodePort
  ports:
  - port: 8080
    targetPort: 8080
  selector:
    app: jenkins
--- 
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jenkins
spec:
  selector:
    matchLabels:
      app: jenkins
  template:
    metadata:
      labels:
        app: jenkins
    spec:
      containers:
      - name: jenkins
        image: jenkins/jenkins:lts-jdk11
        ports:
        - containerPort: 8080
        volumeMounts:
        - name: jenkins-home
          mountPath: /var/jenkins_home
      volumes:
      - name: jenkins-home
        hostPath:
          path: /run/desktop/mnt/host/d/v/k8s/jenkins
        #emptyDir: { }
        # wsl -d docker-desktop
        # chown -R 1000:1000 /mnt/host/d/v/k8s/jenkins
```

查看密码
```
/var/lib/jenkins/secrets/initialAdminPassword
```

更换插件源
```
sed -i 's/https:\/\/updates.jenkins.io\/download/http:\/\/mirrors.tuna.tsinghua.edu.cn\/jenkins/g' /var/lib/jenkins/updates/default.json

sed -i 's/www.google.com/www.baidu.com/g' /var/lib/jenkins/updates/default.json
```

以root启动
```
# 打开配置文件 
vim /etc/sysconfig/jenkins 
# 修改$JENKINS_USER，并去掉当前行注释 
$JENKINS_USER="root"

chown -R root:root /var/lib/jenkins 
chown -R root:root /var/cache/jenkins 
chown -R root:root /var/log/jenkins

# 重启Jenkins（若是其他方式安装的jenkins则重启方式略不同） 
service jenkins restart
```