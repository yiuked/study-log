```
#/bin/bash

BASE_DIR=/root/core


Upgrade(){
        set -x
        cd $BASE_DIR/$1
        git checkout production
        git checkout -- ./
        git pull
        res=$?
        set +x

        if [ $res -ne 0 ]; then
                echo "Err:git pull `$1` fail"
                echo
                exit 1
        fi

        set -x
        go test
        res=$?
        set +x

        if [ $res -ne 0 ]; then
                echo "Err:go test fail"
                echo
                exit 1
        fi

        set -x
        go run ./ migrate
        go run ./ request
        set +x

        set -x
        go build -o $BASE_DIR/$1
        res=$?
        set +x
        if [ $res -eq 0 ]; then
                echo "upgrade $1 successfull"
        else
                echo "upgrade $1 fail"
        fi

        set -x
}
if [ "$1" = "all" ]; then
        Upgrade app1
        Upgrade app2
        Upgrade app3
elif [ -n "$1" ]; then
        Upgrade $1
else
        echo "Options:"
        echo "--type <type> Appoint a upgrade type(options:app1,app2,app3)."
fi


```

