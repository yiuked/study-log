## 基础

1. 创建命名空间

    ```
    kubectl create namespace jenkins
    ```

	> 通过 `kubectl get namespaces`查看是否创建成功

2. 添加安装源

    ```
    $ helm repo add jenkinsci https://charts.jenkins.io
    $ helm repo update
    ```

    > 通过` helm search repo jenkinsci`验证安装源是否添加成功

3. 创建jenkins所需要的存储PV

    ```
    apiVersion: v1
    kind: PersistentVolume
    metadata:
      name: jenkins-pv
      namespace: jenkins
    spec:
      storageClassName: jenkins-pv
      accessModes:
      - ReadWriteOnce
      capacity:
        storage: 20Gi
      persistentVolumeReclaimPolicy: Retain
      hostPath:
        path: /data/jenkins-volume/
    ```

    > 源代码地址:https://raw.githubusercontent.com/jenkins-infra/jenkins.io/master/content/doc/tutorials/kubernetes/installing-jenkins-on-kubernetes/jenkins-volume.yaml
    >
    > 将以上代码另外为`jenkins-pv.yaml`
    >
    > 执行`kubectl apply -f jenkins-pv.yaml `,执行完成后可以通过`kubectl get pv`查看是否创建成功

4. 创建 `Service Account `

    ```
    ---
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: jenkins
      namespace: jenkins
    ---
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRole
    metadata:
      annotations:
        rbac.authorization.kubernetes.io/autoupdate: "true"
      labels:
        kubernetes.io/bootstrapping: rbac-defaults
      name: jenkins
    rules:
    - apiGroups:
      - '*'
      resources:
      - statefulsets
      - services
      - replicationcontrollers
      - replicasets
      - podtemplates
      - podsecuritypolicies
      - pods
      - pods/log
      - pods/exec
      - podpreset
      - poddisruptionbudget
      - persistentvolumes
      - persistentvolumeclaims
      - jobs
      - endpoints
      - deployments
      - deployments/scale
      - daemonsets
      - cronjobs
      - configmaps
      - namespaces
      - events
      - secrets
      verbs:
      - create
      - get
      - watch
      - delete
      - list
      - patch
      - update
    - apiGroups:
      - ""
      resources:
      - nodes
      verbs:
      - get
      - list
      - watch
      - update
    ---
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRoleBinding
    metadata:
      annotations:
        rbac.authorization.kubernetes.io/autoupdate: "true"
      labels:
        kubernetes.io/bootstrapping: rbac-defaults
      name: jenkins
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: ClusterRole
      name: jenkins
    subjects:
    - apiGroup: rbac.authorization.k8s.io
      kind: Group
      name: system:serviceaccounts:jenkins
    ```

    > 源代码地址:https://raw.githubusercontent.com/jenkins-infra/jenkins.io/master/content/doc/tutorials/kubernetes/installing-jenkins-on-kubernetes/jenkins-sa.yaml
    >
    > 将以上代码另外为`jenkins-sa.yaml`
    >
    > 执行`kubectl apply -f jenkins-sa.yaml `,执行完成后可以通过`kubectl get sa -n jenkins`查看是否创建成功

5. 编辑配置文件

   > 源代码比较长,地址:https://raw.githubusercontent.com/jenkinsci/helm-charts/main/charts/jenkins/values.yaml
   >
   > 将源代码另外为模板,修改以下几项配置项:
   >
   > - 存储类(与PV中的`storageClassName`一致)
   >
   > ```
   > storageClass: jenkins-pv
   > ```
   >
   > - 修改ServiceAccount(与sa中的name一致)
   >
   > ```
   > 
   > serviceAccount:
   >   create: false
   >   # The name of the service account is autogenerated by default
   >   name: jenkins
   >   annotations: {}
   >   imagePullSecretName:
   > 
   > serviceAccountAgent:
   >   # Specifies whether a ServiceAccount should be created
   >   create: false
   >   # The name of the ServiceAccount to use.
   >   # If not set and create is true, a name is generated using the fullname template
   >   name: jenkins
   >   annotations: {}
   >   imagePullSecretName:
   > 
   > ## Backup cronjob configuration
   > ## Ref: https://github.com/maorfr/kube-tasks
   > backup:
   >   # Backup must use RBAC
   >   # So by enabling backup you are enabling RBAC specific for backup
   >   enabled: false
   >   # Used for label app.kubernetes.io/component
   >   componentName: "backup"
   >   # Schedule to run jobs. Must be in cron time format
   >   # Ref: https://crontab.guru/
   >   schedule: "0 2 * * *"
   >   labels: {}
   >   serviceAccount:
   >     create: false
   >     name: jenkins
   > ```
   >
   > > 注意create需要改为false因为前面已经创建了sa

6. 安装jenkins

   ```
   helm install jenkins -n jenkins -f .\jenkins-values.yaml jenkinsci/jenkins
   ```

   > 如果安装后,需要修改配置信息 `helm upgrade jenkins -n jenkins -f .\jenkins-values.yaml jenkinsci/jenkins`
   
   安装完成后会输出以下内容:
   
   ```
   1. Get your 'admin' user password by running:
     kubectl exec --namespace jenkins -it svc/jenkins -c jenkins -- /bin/cat /run/secrets/chart-admin-password && echo
   2. Get the Jenkins URL to visit by running these commands in the same shell:
     echo http://127.0.0.1:8080
     kubectl --namespace jenkins port-forward svc/jenkins 8080:8080
   
   3. Login with the password from step 1 and the username: admin
   4. Configure security realm and authorization strategy
   5. Use Jenkins Configuration as Code by specifying configScripts in your values.yaml file, see documentation: http:///configuration-as-code and examples: https://github.com/jenkinsci/configuration-as-code-plugin/tree/master/demos
   
   For more information on running Jenkins on Kubernetes, visit:
   https://cloud.google.com/solutions/jenkins-on-container-engine
   
   For more information about Jenkins Configuration as Code, visit:
   https://jenkins.io/projects/jcasc/
   
   
   NOTE: Consider using a custom image with pre-installed plugins
   ```
   
   > - 通过 ```kubectl exec --namespace jenkins -it svc/jenkins -c jenkins -- /bin/cat /run/secrets/chart-admin-password```可以获得登录密码,得到密码为`rQ5H4Pw2ssoP1YgyYmCPGG`(你的可能不一样)
   > - 通过`kubectl --namespace jenkins port-forward svc/jenkins 8080:8080`可以将jenkins的8080访问端口映射出来

更多安装方式:https://www.jenkins.io/doc/book/installing/kubernetes/

## 应用

### **Pipeline** 

##### 概述

   Jenkins 2.x的精髓是Pipeline as Code，那为什么要用Pipeline呢？jenkins1.0也能实现自动化构建，但Pipeline能够将以前project中的配置信息以steps的方式放在一个脚本里，将原本独立运行于单个或者多个节点的任务连接起来，实现单个任务难以完成的复杂流程，形成流水式发布，构建步骤视图化。简单来说，Pipeline适用的场景更广泛，能胜任更复杂的发布流程。举个例子，job构建工作在master节点，自动化测试脚本在slave节点，这时候jenkins1.0就无法同时运行两个节点，而Pipeline可以。

##### 组件

- Stage: 阶段，一个Pipeline可以划分为若干个Stage，每个Stage代表一组操作。注意，Stage是一个逻辑分组的概念，可以跨多个Node。
- Node: 节点，一个Node就是一个Jenkins节点，或者是Master，或者是slave，是执行Step的具体运行期环境。
- Step: 步骤，Step是最基本的操作单元，小到创建一个目录，大到构建一个Docker镜像，由各类Jenkins Plugin提供



### 问题

```
$ kubectl logs jenkins-0 -n jenkins
error: a container name must be specified for pod jenkins-0, choose one of: [jenkins config-reload] or one of the init containers: [init]
```

> `kubectl logs jenkins-0 -n jenkins -c jenkins`



K8S 地址:

```
<service-name>.<namespace-name>.svc.cluster.local
```



basic-docker-resitry.default.svc.cluster.local





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
      volumes:
      - name: jenkins-home
        hostPath:
          path: /run/desktop/mnt/host/d/v/data/jenkins_home
          type: DirectoryOrCreate
```



```
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: jenkins
  namespace: jenkins
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  annotations:
    rbac.authorization.kubernetes.io/autoupdate: "true"
  labels:
    kubernetes.io/bootstrapping: rbac-defaults
  name: jenkins
rules:
- apiGroups:
  - '*'
  resources:
  - statefulsets
  - services
  - replicationcontrollers
  - replicasets
  - podtemplates
  - podsecuritypolicies
  - pods
  - pods/log
  - pods/exec
  - podpreset
  - poddisruptionbudget
  - persistentvolumes
  - persistentvolumeclaims
  - jobs
  - endpoints
  - deployments
  - deployments/scale
  - daemonsets
  - cronjobs
  - configmaps
  - namespaces
  - events
  - secrets
  verbs:
  - create
  - get
  - watch
  - delete
  - list
  - patch
  - update
- apiGroups:
  - ""
  resources:
  - nodes
  verbs:
  - get
  - list
  - watch
  - update
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  annotations:
    rbac.authorization.kubernetes.io/autoupdate: "true"
  labels:
    kubernetes.io/bootstrapping: rbac-defaults
  name: jenkins
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: jenkins
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: Group
  name: system:serviceaccounts:jenkins
```


```
pipeline{

      environment{
	    // 定义变量,或从Jenkins传入进来的变量
      }

      agent{
        node{
          // 选择 k8s 集群节点
        }
      }

      stages{
 
            stage('获取代码'){
                steps{
                 // 拉取项目程序源码
               }
            }
            
            stage('代码编译打包'){
              steps{
                 container("maven") {
                 // 使用 maven 容器,编译打包
                 }
              }
            }

            stage('镜像构建推送'){
              steps{ 
              	container("kaniko") { 
                    // 使用 kaniko 容器, docker镜像编译与推送到镜像仓库
                }
              }
            }

            stage('获取部署配置'){
              steps{
                 // 拉取 yaml 部署文件
               }
              }
             
            stage('应用部署到K8S集群') {
              steps {
                container('kubectl') {
                // 使用 kubectl 容器, 执行 yaml 部署文件，部署应用到 k8s集群
                }	
              }  
            }
			
        }
    }
```

#### 问题

- ``` 
  inbound-agent 是做什么用的
  ```

[Kaniko 在构建大量图像时被 OOM 杀死 ·问题 #1680 ·GoogleContainerTools/kaniko (github.com)](https://github.com/GoogleContainerTools/kaniko/issues/1680)

