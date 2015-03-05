from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
import os, socket
from tinytag import TinyTag
from musicvoting.models import Artist, Album, Track, User
import musicvoting.mysocket as mysocket
# Create your views here.

def pause(request):
    #check if admin
    permission = request.user.is_superuser
    if permission == True:
        sock = mysocket.Mysocket()
        sock.connect(mysocket.ADDR, mysocket.PORT)
        sock.mysend(format(1, '07'))
        answer = sock.myreceive()
        sock.close()
        if answer == format(1, '07'):
            return HttpResponse("Music is paused. " + answer)
        else:
            return HttpResponse("ERROR")
    else:
        return HttpResponse('Unauthorized', status=401)


def unpause(request):
    permission = request.user.is_superuser
    if permission == True:
        sock = mysocket.Mysocket()
        sock.connect(mysocket.ADDR, mysocket.PORT)
        sock.mysend(format(2, '07'))
        answer = sock.myreceive()
        sock.close()
        if answer == format(1, '07'):
            return HttpResponse("Music is unpaused. " + answer)
        else:
            return HttpResponse("ERROR")
    else:
        return HttpResponse('Unauthorized', status=401)
    

def next_track(request):
    permission = request.user.is_superuser
    if permission == True:
        sock = mysocket.Mysocket()
        sock.connect(mysocket.ADDR, mysocket.PORT)
        sock.mysend(format(3, '07'))
        answer = sock.myreceive()
        sock.close()
        current_track = get_object_or_404(Track, pk=int(answer))
        context = {
            'current_track': current_track,
            }
        return render(request, 'musicvoting/player.html', context)
        
    else:
        return HttpResponse('Unautorized', status=401)

@ensure_csrf_cookie
def index(request):
    #Set cookie
    if 'voter_id' not in request.session:
        cookie = False
        voter = User()
        voter.save()
        request.session['voter_id'] = voter.id
        request.session.set_expiry(24*60*60)
    else:
        try:
            voter = User.objects.get(pk=request.session['voter_id'])
        except User.DoesNotExist:
            #In case there is a cookie with a voter_id but not an corresponding entry in the database
            voter = User()
            voter.save()
            request.session['voter_id'] = voter.id
        request.session.set_expiry(24*60*60)
        cookie = True
    try:    
        #Get current track
        sock = mysocket.Mysocket()
        sock.connect(mysocket.ADDR, mysocket.PORT)
        sock.mysend(format(4, '07'))
        answer = sock.myreceive()
        sock.close()
    
        current_track = Track.objects.get(pk=int(answer))

        #Get current playing status
        sock = mysocket.Mysocket()
        sock.connect(mysocket.ADDR, mysocket.PORT)
        sock.mysend(format(5, '07'))
        answer = sock.myreceive()
        sock.close()

        if answer == format(1, '07'):
            playing = True
        elif answer == format(0, '07'):
            playing = False
        else:
            playing = 'Error'
        player_running = True
    except socket.error:
        current_track = None
        playing = None
        player_running = False

    #Get tracks ranked by votes
    track_ranking = Track.objects.filter(votes__gt=0).order_by('-votes')

    #Check if admin
    admin = request.user.is_superuser

    context = {
        'current_track': current_track,
        'track_ranking': track_ranking,
        'cookie': cookie,
        'voter': voter,
        'playing': playing,
        'admin': admin,
        'player_running': player_running,
        }
    response = render(request, 'musicvoting/index.html', context)
    if cookie == False:
        response.set_cookie('test_cookie', 'true')
    return response

def artist(request):
    artist_list = Artist.objects.order_by('artist_name')
    context = {'artist_list': artist_list}
    return render(request, 'musicvoting/artist.html', context)

@ensure_csrf_cookie
def artist_detail(request, pk):
    #get voter_id from session or redirect to main page
    if 'voter_id' in request.session:
        try:
            voter = User.objects.get(pk=request.session['voter_id'])
        except User.DoesNotExist:
            #In case there is a cookie with a voter_id but not an corresponding entry in the database
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

@ensure_csrf_cookie
def album_detail(request, pk):
    #get voter_id from session or redirect to main page
    if 'voter_id' in request.session:
        try:
            voter = User.objects.get(pk=request.session['voter_id'])
        except User.DoesNotExist:
            #In case there is a cookie with a voter_id but not an corresponding entry in the database
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

def search(request):
    #get voter_id from session or redirect to main page
    if 'voter_id' in request.session:
        try:
            voter = User.objects.get(pk=request.session['voter_id'])
        except User.DoesNotExist:
            #In case there is a cookie with a voter_id but not an corresponding entry in the database
            voter = User()
            voter.save()
            request.session['voter_id'] = voter.id
        request.session.set_expiry(24*60*60)
    else:
        return redirect('musicvoting:index')

    search_string = request.GET['search']
    track_list = Track.objects.filter( Q(title__icontains = search_string) | Q(album__album_name__icontains = search_string) | Q(artist__artist_name__icontains = search_string)).order_by('album__album_name', 'track_number')
    context = {
        'track_list': track_list,
        'voter' : voter,
        'search_string' : search_string,
    }
    return render(request, 'musicvoting/search.html', context)
    
def vote_track(request):
    if request.method == "POST":
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
        track_id = int(request.POST['track_id'])
        track = get_object_or_404(Track, pk=track_id)
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
        #Refresh vote counter when vote button was pressed.
        return HttpResponse("Votes: " + str(track.votes))

    else:
        return HttpResponse("Use POST")


def unvote_track(request):
    if request.method == "POST":
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

        track_id = int(request.POST['track_id'])
        track = get_object_or_404(Track, pk=track_id)
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
        #Refresh vote counter when unvote button was pressed.
        return HttpResponse("Votes: " + str(track.votes))
    else:
        return HttpResponse("Use POST")


def dbimport(request):
    permission = request.user.is_superuser
    if permission == True:
        music_dir = getattr(settings, 'MUSICVOTING_MUSIC_DIR')

        #Delete all db entries
        Track.objects.all().delete()
        User.objects.all().delete()
        Artist.objects.all().delete()
        Album.objects.all().delete()
		
        import re
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

        return HttpResponse("DB was updated")
    else:
        return HttpResponse('Unauthorized', status=401)


def shutdown(request):
    permission = request.user.is_superuser
    if request.method == 'POST':
        if permission == True:
            #shut device down
            command = "/usr/bin/sudo /sbin/shutdown -h now"
            import subprocess
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            output = process.communicate()[0]
            return HttpResponse("Shutting down now.\n" + output)
        else:
            return HttpResponse('Unauthorized', status=401)

