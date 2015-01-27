import os, sys, pygame, django, random, socket
from thread import start_new_thread
sys.path.append('/home/pi/Django/musicvotingsite')
os.environ['DJANGO_SETTINGS_MODULE'] = 'musicvotingsite.settings'
django.setup()
from musicvoting.models import Track, User
from django.db.models import Max
import musicvoting.mysocket as mysocket
                         
SONG_END = pygame.USEREVENT + 1

current_track = None


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

def handle_clientsocket(clientsocket):
    mysock = mysocket.Mysocket(clientsocket)
    msg = mysock.myreceive()
    #pause
    if msg == format(1, '07'):
        print "pausing music"
        pygame.mixer.music.pause()
        mysock.mysend(format(1, '07'))
        mysock.close()
    #unpause
    elif msg == format(2, '07'):
        print "unpausing music"
        pygame.mixer.music.unpause()
        mysock.mysend(format(1, '07'))
        mysock.close()
    #nexttrack
    elif msg == format(3, '07'):
        print "playing next track"
        next_track()
        mysock.mysend(format(1, '07'))
        mysock.close()
    #get track
    elif msg == format(4, '07'):
        global current_track
        ret = format(current_track.id, '07')
        mysock.mysend(ret)
        mysock.close()
    #is playing?
    elif msg == format(5, '07'):
        if pygame.mixer.music.get_busy():
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
    
