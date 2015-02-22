#!/bin/bash

# Replace these three settings.
PROJDIR="/home/pi/Django/musicvotingsite"
PIDFILE="$PROJDIR/django.pid"
SOCKET="$PROJDIR/musicvoting.sock"
PIDFILEPLAYER="$PROJDIR/musicplayer.pid"

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

if [ -f $PIDFILEPLAYER ]; then
    kill `cat -- $PIDFILEPLAYER`
    rm -f -- $PIDFILEPLAYER
fi

python musicvoting/musicplayer.py &
python $PROJDIR/manage.py runfcgi method=prefork socket=$SOCKET pidfile=$PIDFILE &
