from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
import os, socket
from mutagen.mp3 import EasyMP3
from musicvoting.models import Artist, Album, Track, User
# Create your views here.
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


def pause(request):
    sock = mysocket()
    sock.connect('127.0.0.1', 9999)
    sock.mysend(format(1, '07'))
    answer = sock.myreceive()
    if answer == format(1, '07'):
        return HttpResponse("Music is paused. " + answer)
    else:
        return HttpResponse("ERROR")

def unpause(request):
    sock = mysocket()
    sock.connect('127.0.0.1', 9999)
    sock.mysend(format(2, '07'))
    answer = sock.myreceive()
    if answer == format(1, '07'):
        return HttpResponse("Music is unpaused. " + answer)
    else:
        return HttpResponse("ERROR")

def next_track(request):
    sock = mysocket()
    sock.connect('127.0.0.1', 9999)
    sock.mysend(format(3, '07'))
    answer = sock.myreceive()
    if answer == format(1, '07'):
        return HttpResponse("playing next track. " + answer)
    else:
        return HttpResponse("ERROR") 

def index(request):
    #Set cookie
    if 'voter_id' not in request.session:
        cookie = False
        voter = User()
        voter.save()
        request.session['voter_id'] = voter.id
        request.session.set_expiry(24*60*60)
    else:
        cookie = True
        
    return HttpResponse("Hello World. Cookie: " + str(cookie))

def artist(request):
    artist_list = Artist.objects.order_by('artist_name')
    context = {'artist_list': artist_list}
    return render(request, 'musicvoting/artist.html', context)

def artist_detail(request, pk):
    #get voter_id from session or redirect to main page
    if 'voter_id' in request.session:
        try:
            voter = User.objects.get(pk=request.session['voter_id'])
        except User.DoesNotExist:
            #In case there is a cookie with a voter_id but not an coresponding entry in the database
            voter = User()
            voter.save()
            request.session['voter_id'] = voter.id
        request.session.set_expiry(24*60*60)
    else:
        return redirect('musicvoting:index')
    
    artist = get_object_or_404(Artist, pk=pk)
    track_list = Track.objects.filter(artist = artist).order_by('album__album_name', 'track_number')
    context = {
        'artist': artist,
        'track_list': track_list,
        'voter': voter,
        'path': request.path,
        }
    return render(request, 'musicvoting/artist_detail.html', context)

def album(request):
    album_list = Album.objects.order_by('album_name')
    context = {'album_list': album_list}
    return render(request, 'musicvoting/album.html', context)

def album_detail(request, pk):
    #get voter_id from session or redirect to main page
    if 'voter_id' in request.session:
        try:
            voter = User.objects.get(pk=request.session['voter_id'])
        except User.DoesNotExist:
            #In case there is a cookie with a voter_id but not an coresponding entry in the database
            voter = User()
            voter.save()
            request.session['voter_id'] = voter.id
        request.session.set_expiry(24*60*60)
    else:
        return redirect('musicvoting:index')

    album = get_object_or_404(Album, pk=pk)
    track_list = Track.objects.filter(album = album).order_by('track_number')
    context = {
        'album': album,
        'track_list': track_list,
        'voter': voter,
        'path': request.path,
        }
    return render(request, 'musicvoting/album_detail.html', context)

def vote_track(request, pk):
    #get voter_id from session or redirect to main page
    if 'voter_id' in request.session:
        try:
            voter = User.objects.get(pk=request.session['voter_id'])
        except User.DoesNotExist:
            #In case there is a cookie with a voter_id but not an coresponding entry in the database
            voter = User()
            voter.save()
            request.session['voter_id'] = voter.id
        request.session.set_expiry(24*60*60)
    else:
        return redirect('musicvoting:index')

    

    #Get track
    track = get_object_or_404(Track, pk=pk)
    try:
        #If voter already voted for this track
        track.voting_users.get(pk=voter.id)
        #return HttpResponse("You already voted.")
    #Else
    except User.DoesNotExist:
        track.voting_users.add(voter)
        track.votes += 1
        track.save()
        #return HttpResponse("You voted. " + track.title + " Votes : " + str(track.votes))
    #Redirect to page where vote button was pressed.
    return HttpResponseRedirect(request.GET['next'])

def unvote_track(request, pk):
    #get voter_id from session or redirect to main page
    if 'voter_id' in request.session:
        try:
            voter = User.objects.get(pk=request.session['voter_id'])
        except User.DoesNotExist:
            #In case there is a cookie with a voter_id but not an coresponding entry in the database
            voter = User()
            voter.save()
            request.session['voter_id'] = voter.id
        request.session.set_expiry(24*60*60)
    else:
        redirect('musicvoting:index')

    track = get_object_or_404(Track, pk=pk)
    try:
        #If voter voted for this track
        track.voting_users.get(pk=voter.id)
        track.voting_users.remove(voter)
        track.votes -= 1
        track.save()
        #return HttpResponse("You unvoted. "  + track.title + " Votes : " + str(track.votes))
    except User.DoesNotExist:
        #If voter never voted for this track in the first place.
        #return HttpResponse("You never voted for this Track in the first place.")
        pass
    #Redirect to page where unvote button was pressed.
    return HttpResponseRedirect(request.GET['next'])


def dbimport(request):
    permission = request.user.is_superuser
    if permission == True:
        music_dir = getattr(settings, 'MUSICVOTING_MUSIC_DIR')

        #Delete all db entries
        Track.objects.all().delete()
        User.objects.all().delete()
        Artist.objects.all().delete()
        Album.objects.all().delete()
        
        for root, dirs, files in os.walk(music_dir):
            for file in files:
                if file.endswith('.mp3'):
                   path = os.path.join(root, file)
                   mp3 = EasyMP3(path)
                   mp3info = mp3.tags
                   mpeginfo = mp3.info
                   length = int(mpeginfo.length)
                   title = mp3info['title'][0]
                   artist = mp3info['artist'][0]
                   album = mp3info['album'][0]
                   tracknumber = mp3info['tracknumber'][0]
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

        return HttpResponse("DB was updated")
    else:
        return HttpResponse('Unauthorized', status=401)
