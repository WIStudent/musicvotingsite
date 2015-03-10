import time, os, sys, signal, django, socket, re
from tinytag import TinyTag
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
os.environ['DJANGO_SETTINGS_MODULE'] = 'musicvotingsite.settings'
django.setup()
from musicvoting.models import Track, User, Artist, Album
from django.conf import settings

import musicvoting.mysocket as mysocket
from thread import start_new_thread


#write PID in the file
pidfile_path = os.path.join(os.path.dirname(__file__), os.pardir, 'musicimport.pid')
pidfile = open(pidfile_path, "w")
pid = os.getpid()
pidfile.write("%s" % pid)
pidfile.close()

running = True
#Set number_of_files to -1, meaning we have not counted yet.
number_of_files = -1
number_processed = 0

def handle_serversocket():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('127.0.0.1', 10000))
    serversocket.listen(5)
    while running == True:
        clientsocket, address = serversocket.accept()
        start_new_thread(handle_clientsocket, (clientsocket,))

def handle_clientsocket(clientsocket):
    mysock = mysocket.Mysocket(clientsocket)
    msg = mysock.myreceive()
    #get number of files
    if msg == format(1, '07'):
        mysock.mysend(format(number_of_files, '07'))
    elif msg == format(2, '07'):
        mysock.mysend(format(number_processed, '07'))
    mysock.close()


#start socket handling
start_new_thread(handle_serversocket, ())

#Count files:
music_dir = getattr(settings, 'MUSICVOTING_MUSIC_DIR')
number_of_files = 0
for root, dirs, files in os.walk(music_dir):
    for file in files:
        if file.endswith('.mp3'):
            number_of_files += 1

#import files:
#Delete all db entries
Track.objects.all().delete()
User.objects.all().delete()
Artist.objects.all().delete()
Album.objects.all().delete()


for root, dirs, files in os.walk(music_dir):
    for file in files:
        if file.endswith('.mp3'):
            path = os.path.join(root, file)
            tag = TinyTag.get(path)
            length = int(tag.duration)
            if tag.title is not None:
                title = tag.title
            else:
                title = file.rstrip('.mp3')
            if tag.artist is not None:
                artist = tag.artist
            else:
                artist = 'Unknown artist'
            if tag.album is not None:
                album = tag.album
            else:
                album = 'Unknown album'
            try:
                tracknumber = int(re.sub("[^0-9]", "", tag.track))
            except:
                tracknumber = 0
            try:
                art = Artist.objects.get(artist_name=artist)
            except Artist.DoesNotExist:
                art = Artist(artist_name=artist)
                art.save()

            try:
                alb = Album.objects.get(album_name=album)
            except Album.DoesNotExist:
                alb = Album(album_name=album)
                alb.save()

            track = Track(artist=art, album=alb, track_number = tracknumber, title = title, lenth = length, path = path)
            track.save()
            number_processed += 1

#Set number_of_files, meaning that the import is finished.
number_of_files = -2
#Wait a short moment to be able to answer that the import has finished.
time.sleep(10)
#Stop the serversocket while loop
running = False

#Remove pid file:
os.remove(pidfile_path)
