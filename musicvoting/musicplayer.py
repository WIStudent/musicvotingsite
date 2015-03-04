import os, sys, pygame, django, random, socket
from thread import start_new_thread
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
os.environ['DJANGO_SETTINGS_MODULE'] = 'musicvotingsite.settings'
django.setup()
from musicvoting.models import Track, User
from django.db.models import Max
import musicvoting.mysocket as mysocket
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
                         
SONG_END = pygame.USEREVENT + 1

current_track = None
playing = False


def next_track():
    max_votes = Track.objects.all().aggregate(Max('votes'))['votes__max']
    track_set = Track.objects.filter(votes=max_votes)
    global current_track
    current_track = random.choice(track_set)
    current_track.votes = 0
    current_track.save()
    current_track.voting_users.clear()
    print (current_track.title + " votes: " + str(max_votes))
    pygame.mixer.music.load(current_track.path)
    pygame.mixer.music.play()
    global playing
    playing = True

def handle_clientsocket(clientsocket):
    mysock = mysocket.Mysocket(clientsocket)
    msg = mysock.myreceive()
    #pause
    if msg == format(1, '07'):
        print "pausing music"
        pygame.mixer.music.pause()
        global playing
        playing = False
        mysock.mysend(format(1, '07'))
        mysock.close()
    #unpause
    elif msg == format(2, '07'):
        print "unpausing music"
        pygame.mixer.music.unpause()
        global playing
        playing = True
        mysock.mysend(format(1, '07'))
        mysock.close()
    #nexttrack
    elif msg == format(3, '07'):
        print "playing next track"
        next_track()
        global current_track
        mysock.mysend(format(current_track.id, '07'))
        mysock.close()
    #get track
    elif msg == format(4, '07'):
        global current_track
        #send back id of new track
        ret = format(current_track.id, '07')
        mysock.mysend(ret)
        mysock.close()
    #is playing?
    elif msg == format(5, '07'):
        global playing
        if playing:
            mysock.mysend(format(1, '07'))
        else:
            mysock.mysend(format(0, '07'))
        mysock.close()

#play next track when current track is finished
def play_next_track():
    while True:
        for event in pygame.event.get():
            if event.type == SONG_END:
                next_track()

#setting up socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((mysocket.ADDR, mysocket.PORT))
serversocket.listen(5)
#setting up music player
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_endevent(SONG_END)
next_track()


start_new_thread(play_next_track, ())

while True:
    clientsocket, address = serversocket.accept()
    print address
    start_new_thread(handle_clientsocket, (clientsocket,))
    
