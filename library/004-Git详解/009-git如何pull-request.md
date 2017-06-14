## 如何正确地给 github 的开源项目提交 pull request

1. `fork` 原始仓库

2. `clone` 自己的仓库

3. 在 `master` 分支添加原始仓库为远程分支 `git remote add upstream` 远程仓库

4. 自己分支开发，如 `dev` 分支开发：`git checkout -b dev`

5. 本地 `dev` 提交

6. 切换 `master` 分支，同步原始仓库：`git checkout master`， `git pull upstream master`

7. 切换本地 `dev` 分支，合并本地 `master` 分支（已经和原始仓库同步），可能需要解冲突 `git merge master`

8. 提交本地 `dev` 分支到自己的远程 `dev` 仓库  `git pull origin dev`

9. 登录`git`平台，切换到自己`fork`的项目中，选择刚刚提交的`dev`分支，可以看到右边有一个`pull new quest`.

10. 点击`pull new quest`会跳到原始仓库，进行提交请求描述，填写内容后提交就可以了。

11. 等待原作者回复（接受/拒绝）
