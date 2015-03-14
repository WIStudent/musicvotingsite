import os, sys, django, random, socket
from thread import start_new_thread
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
os.environ['DJANGO_SETTINGS_MODULE'] = 'musicvotingsite.settings'
django.setup()
from musicvoting.models import Track, User, Player
from django.db.models import Max
import musicvoting.mysocket as mysocket
import vlc
#Make it runnable even if no display is attached.
os.environ["SDL_VIDEODRIVER"] = "dummy"

pidfile_path = os.path.join(os.path.dirname(__file__), os.pardir, 'musicplayer.pid')
if os.access(pidfile_path, os.F_OK):
    #if pid file ist already there check thef PID number
    pidfile = open(pidfile_path, "r")
    pidfile.seek(0)
    old_pd = pidfile.readline()
    #check if PID from file matches to the current process PID
    if os.path.exists("/proc/%s" % old_pd):
        print "You already have an instance running."
        print "It is running as process %s" % old_pd
        sys.exit(1)
    else:
        os.remove(pidfile_path)

#write PID in the file
pidfile = open(pidfile_path, "w")
pidfile.write("%s" % os.getpid())
pidfile.close()

#If an entry for the player already exists in the database, use this entry.
player_query_set = Player.objects.all()
if len(player_query_set) > 0:
    player_dbobj = player_query_set[0]
else:
    player_dbobj = Player()

current_track = None

player = vlc.MediaPlayer()

def next_track():
    global player_dbobj
    player_dbobj.user_set.clear()
    max_votes = Track.objects.all().aggregate(Max('votes'))['votes__max']
    track_set = Track.objects.filter(votes=max_votes)
    global current_track
    current_track = random.choice(track_set)
    player_dbobj.track = current_track
    player_dbobj.number_of_votes = current_track.votes
    current_track.votes = 0
    current_track.save()
    current_track.voting_users.clear()
    #print (current_track.title + " votes: " + str(max_votes))
    global player
    player.set_mrl(current_track.path)
    player.play()
    player_dbobj.playing = True
    player_dbobj.save()

def handle_clientsocket(clientsocket):
    mysock = mysocket.Mysocket(clientsocket)
    msg = mysock.myreceive()
    global player
    global current_track
    global player_dbobj
    #pause
    if msg == format(1, '07'):
        #print "pausing music"
        player.pause()
        player_dbobj.playing = False
        player_dbobj.save()
        mysock.mysend(format(1, '07'))
    #unpause
    elif msg == format(2, '07'):
        #print "unpausing music"
        player.play()
        player_dbobj.playing = True
        player_dbobj.save()
        mysock.mysend(format(1, '07'))
    #nexttrack
    elif msg == format(3, '07'):
        #print "playing next track"
        next_track()
        mysock.mysend(format(current_track.id, '07'))
    #get track
    elif msg == format(4, '07'):
        #send back id of new track
        ret = format(current_track.id, '07')
        mysock.mysend(ret)
    #is playing?
    elif msg == format(5, '07'):
        if player.is_playing():
            mysock.mysend(format(1, '07'))
        else:
            mysock.mysend(format(0, '07'))
    elif msg == format(6, '07'):
        mysock.mysend(format(player_dbobj.id, '07'))
    mysock.close()

def next_track_callback(event):
    #If next_track is not called in a separate track, the vlc player will not play the next track.
    start_new_thread(next_track, ())

#setting up socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((mysocket.ADDR, mysocket.PORT))
serversocket.listen(5)
#setting up music player
mp_em = player.event_manager()
mp_em.event_attach(vlc.EventType.MediaPlayerEndReached, next_track_callback)

if player_dbobj.track is None:
    next_track()
#Play the track that was playing when the musicplayer was killed.
else:
    current_track = player_dbobj.track
    player.set_mrl(player_dbobj.track.path)
    player.play()

while True:
    clientsocket, address = serversocket.accept()
    #print address
    start_new_thread(handle_clientsocket, (clientsocket,))
    
