#!/bin/bash

# Replace these three settings.
PROJDIR="/home/pi/Django/musicvotingsite"
PIDFILE="$PROJDIR/musicvoting.pid"
SOCKET="$PROJDIR/musicvoting.sock"

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

exec /usr/bin/env - \
  PYTHONPATH="../python:.." \
  ./manage.py runfcgi socket=$SOCKET pidfile=$PIDFILE
