## git集成phpcs，commit时检测PHP代码格式
### 安装pear

下载`go-pear.phar`文件，放本地任意目录，http://pear.php.net/go-pear.phar;  
在`cmd`命令行下，执行 `php go-pear.phar`，`go-pear.phar`本质是一个`PHP`脚本文件，安装过程会提示是应用到系统还是当前用户;  
在`cmd`命令行下 输入`pear`，出现`help`文档，此处可能会提示环境变量配置不完善，按要求完善则可（非必须）;  

### pear安装phpcs
关于`CodeSniffer`简称`phpcs`，用于检测`php`、`javascript`、`css`文件的语法标准。  
更多详情可参考：http://pear.php.net/package/PHP_CodeSniffer/  
官方`github`地址:https://github.com/squizlabs/PHP_CodeSniffer  

在`cmd`命令行下，输入安装`PHP_CodeSniffer`命令：
```
pear install PHP_CodeSniffer
```
在`cmd`命令行下，输入 `phpcs --version` ，安装成功会显示版本信息

### phpcs命令

忽略`warning`，如一行超过`85`字符
```
phpcs -n your_file
```
查看当前标准
```
phpcs -i
```
设置默认标准
```
phpcs --config-set default_standard PSR2
```
设置文件编码
```
phpcs --config-set encoding utf-8
```
检查PHP文件
```
phpcs test.php
phpcs D:\work\testApp\controller\
```
使用phpcbf命令，并以PSR2标准修复文件
```
phpcbf --standard=PSR2 test.php
```

### git集成phpcs

使用`git`的`hook`中的`pre-commit`，把以下代码拷贝到项目中的 `.git/hook/pre-commit`中，
在代码`commit`的时候，就会运行`pre-commit`，自动调用`phpcs`检测代码规范性，`git`根据`pre-commit`中的
`exit`返回值决定代码是否提交，单返回值为0时，代码会正常执行`commit`,否则终止`commit`
```
#!/bin/bash
#
# check PHP code syntax error and standard with phpcs
# author : star[github.com/star1989]
# date : 2017-02-24
PROJECT=$(git rev-parse --show-toplevel)
cd $PROJECT
SFILES=$(git diff --cached --name-only --diff-filter=ACMR HEAD | grep \\.php)
TMP_DIR=$PROJECT"/tmp"

# Determine if a file list is passed
if [ "$#" -ne 0 ]
then
    exit 0
fi
echo "Checking PHP Lint..."
for FILE in $SFILES
do
#    echo "php -l -d display_errors=0 ${FILE}"
#	echo "git show :$FILE > $TMP_DIR/$FILE"
    php -l -d display_errors=0 $FILE
    if [ $? != 0  ]
    then
        echo "Fix the error before commit."
        exit 1
    fi
    FILES="$FILES $PROJECT/$FILE"
done

echo "Checkout report dir..."
if [ -d report ]
then
    echo "Delete report dir"
    rm -rf report
fi
if [ ! -d report ]
then
    echo "Create report dir"
    mkdir report
fi

if [ "$FILES" != ""  ]
then
    echo "Running Code Sniffer & MD..."
    mkdir -p $TMP_DIR
    for FILE in $SFILES
    do
        echo $TMP_DIR/$FILE
        mkdir -p $TMP_DIR/$(dirname $FILE)
        git show :$FILE > $TMP_DIR/$FILE
    done
    phpcs --standard=PSR2 -n $TMP_DIR > $PROJECT/report/standard.txt
    PHPCS_ERROR=$?
    rm -rf $TMP_DIR
    if [ $PHPCS_ERROR != 0  ]
    then
        echo "Please look reports.Then fix the errors"
        exit 1
    fi
fi
exit $?
```
