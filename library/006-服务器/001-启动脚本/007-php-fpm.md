```
#!/bin/sh
#=======================================================================================
# php-fpm - this script start and stop the php-fpm daemon
#
# chkconfig 35 on
# description: php-fpm is a FastCGI web server.
# processname: php-fpm
# config: /usr/local/php/etc/php-fpm.conf
# pidfile: /var/run/php-fpm.pid
#=======================================================================================
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

BINFILE="/root/lamp/sbin/php-fpm"
CFGFILE="/root/lamp/etc/php-fpm.d/www.conf"
PHPINIFILE="/root/lamp/conf/php.ini"
PIDFILE="/var/run/php-fpm.pid"
LOCKFILE="/var/lock/php-fpm.lock"

RETVAL=0

start() {
    [[ -x $BINFILE ]] || exit 5
    [[ -f $CFGFILE ]] || exit 6

    if [[ `ps aux | grep php-fpm: | grep -v grep | wc -l` -gt 0 ]]; then
        echo "The php-fpm is already running."
        return 1
    fi

    $BINFILE -t >/dev/null 2>&1

    if [[ $? -ne 0 ]]; then
        echo "The php-fpm configure has error."
        return 1
    fi

    echo -n "Starting php-fpm......"
    $BINFILE -y $CFGFILE -g ${PIDFILE} -R
    RETVAL=$?
    echo
    [[ $RETVAL -eq 0 ]] && touch $LOCKFILE

    return $RETVAL
}

stop() {
    if [[ `ps aux | grep php-fpm: | grep -v grep | wc -l` -eq 0 ]]; then
        echo "The php-fpm is not running."
        return 1
    fi

    echo -n "Shutting down php-fpm......"

    if [[ -f $PIDFILE ]]; then
        kill -QUIT `cat ${PIDFILE}`
    else
        kill -QUIT `ps aux | grep php-fpm | awk '/master/{print $2}'`
    fi

    RETVAL=$?
    echo
    [[ $RETVAL -eq 0 ]] && rm -f $LOCKFILE $PIDFILE

    return $RETVAL
}

restart() {
    stop
    sleep 1

    while true
    do
        if [[ `ps aux | grep php-fpm: | grep -v grep | wc -l` -eq 0 ]]; then
            start
            break
        fi
        sleep 1
    done

    RETVAL=$?
    echo

    return $RETVAL
}

reload() {
    if [[ `ps aux | grep php-fpm: | grep -v grep | wc -l` -eq 0 ]]; then
        echo "The php-fpm is not running."
        return 1
    fi

    echo -n $"Reloading php-fpm......"

    if [[ -f $PIDFILE ]]; then
        kill -USR2 `cat ${PIDFILE}`
    else
        kill -USR2 `ps aux | grep php-fpm | awk '/master/{print $2}'`
    fi

    RETVAL=$?
    echo

    return $RETVAL
}

case "$1" in
start)
    start
    ;;

stop)
    stop
    ;;

restart)
    restart
    ;;

reload)
    reload
    ;;

*)
    echo "Usage: service php-fpm {start|stop|restart|reload}"
    RETVAL=1
esac

exit $RETVAL
```
