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

   