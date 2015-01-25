import os, sys, pygame, django, random, socket
from thread import start_new_thread
sys.path.append('/home/pi/Django/musicvotingsite')
os.environ['DJANGO_SETTINGS_MODULE'] = 'musicvotingsite.settings'
django.setup()
from musicvoting.models import Track, User
from django.db.models import Max

MSGLEN = 7
class mysocket:
    #from https://docs.python.org/2/howto/sockets.html
    
    
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk= self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == "":
                raise RuntimeError("socket connection brocken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return ''.join(chunks)
                                    

SONG_END = pygame.USEREVENT + 1

current_track = None


def next_track():
    max_votes = Track.objects.all().aggregate(Max('votes'))['votes__max']
    track_set = Track.objects.filter(votes=max_votes)
    current_track = random.choice(track_set)
    current_track.votes = 0
    current_track.save()
    current_track.voting_users.clear()
    print (current_track.title + " votes: " + str(max_votes))
    pygame.mixer.music.load(current_track.path)
    pygame.mixer.music.play()

def handle_clientsocket(clientsocket):
    mysock = mysocket(clientsocket)
    msg = mysock.myreceive()
    #pause
    if msg == format(1, '07'):
        print "pausing music"
        pygame.mixer.music.pause()
        mysock.mysend(format(1, '07'))
    #unpause
    elif msg == format(2, '07'):
        print "unpausing music"
        pygame.mixer.music.unpause()
        mysock.mysend(format(1, '07'))
    #nexttrack
    elif msg == format(3, '07'):
        print "playing next track"
        next_track()
        mysock.mysend(format(1, '07'))
    #get track
    elif msg == format(4, '07'):
        ret = format(current_track.id, '07')
        mysock.mysend(ret)
    #is playing?
    elif msg == format(5, '07'):
        if pygame.mixer.music.get_busy():
            mysock.mysend(format(1, '07'))
        else:
            mysock.mysend(format(0, '07'))

#play next track when current track is finished
def play_next_track():
    while True:
        for event in pygame.event.get():
            if event.type == SONG_END:
                next_track()

#setting up socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('127.0.0.1', 9999))
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
    




