
1 把本地的 develop 分支强制(-f)推送到远程 master
但是上面操作，本地的 master 分支还是旧的，通常来说应该在本地做好修改再去 push 到远端，所以我推荐如下操作

git push origin fix9e49:master -f
2  切换到旧的分支

git checkout master 
3  将本地的旧分支 master 重置成 develop

git reset --hard fix9e49  
4  再推送到远程仓库

git push origin master --force 