```
#!/bin/sh
#
# memcached - this script starts and stops the memcached daemin
#
# chkconfig: - 55 45
# description: The memcached daemon is a network memory cache service. \
# processname: memcached
# config: /etc/sysconfig/memcached
# Source function library - for other linux
#. /etc/rc.d/init.d/functions
# Source function library - for suse linux

NAME=memcached
PORT=11211
USER=root
#最大连接数，根据实际需求修改
MAXCONN=1024
#最大内存量，单位M
CACHESIZE=128
OPTIONS=""
DAEMON=/root/lamp/bin/$NAME
LOCKFILE="/var/lock/memcached.lock"

if [ -f $DAEMON ];then
	$DAEMON
fi

# Check that networking is up.
if [ "$NETWORKING" = "no" ]
then
	exit 0
fi

RETVAL=0

start () {
    echo -n $"Starting $NAME: "
    # insure that /usr/local/memcached has proper permissions
    chown $USER $DAEMON
    $DAEMON -d -p $PORT -u $USER  -m $CACHESIZE -c $MAXCONN -P $LOCKFILE $OPTIONS
    RETVAL=$?
    echo
    [ $RETVAL -eq 0 ] && touch /var/lock/subsys/memcached
}
stop () {
    echo -n $"Stopping $NAME: "
    killproc memcached
    RETVAL=$?
    echo
    if [ $RETVAL -eq 0 ] ; then
        rm -f /var/lock/subsys/memcached
        rm -f $LOCKFILE
    fi
}

restart () {
    stop
    start
}
# See how we were called.
case "$1" in
    start)
        start
        ;;
    stop)
    stop
    ;;
    status)
    status memcached
    ;;
    restart|reload)
    restart
    ;;
    condrestart)
    [ -f /var/lock/subsys/memcached ] && restart || :
    ;;
    *)
    echo $"Usage: $0 {start|stop|status|restart|reload|condrestart}"
    exit 1
esac
exit $?
```
