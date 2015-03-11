from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
import os, socket, sys, time
from musicvoting.models import Artist, Album, Track, User
import musicvoting.mysocket as mysocket
from subprocess import Popen
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
    

def active_votes(request):
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

    track_list = voter.track_set.all()
    context = {
        'track_list': track_list,
    }
    return render(request, 'musicvoting/active_votes.html', context)


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
    #Check, if import is already running
    pidfile_path = os.path.join(os.path.dirname(__file__), os.pardir, 'musicimport.pid')
    if os.access(pidfile_path, os.F_OK):
        #if pid file ist already there check thef PID number
        pidfile = open(pidfile_path, "r")
        pidfile.seek(0)
        old_pd = pidfile.readline()
        #check if PID from file matches to the current process PID
        if os.path.exists("/proc/%s" % old_pd):
            import_running = True
        else:
            os.remove(pidfile_path)
            import_running = False
    else:
        import_running = False

    if request.method == 'GET':
        if request.user.is_authenticated():
            if request.user.is_superuser:
                context = {
                    'import_running': import_running,
                }
                return render(request, 'musicvoting/import.html', context)
            else:
                return HttpResponse('Unauthorized', status=401)
        else:
            return redirect(reverse('musicvoting:login') + '?next=' + reverse('musicvoting:dbimport'))

    elif request.method == 'POST':
        if request.user.is_superuser:
            if not import_running:
                Popen(['python', os.path.join(os.path.dirname(__file__), 'musicimport.py')])
                while not os.access(pidfile_path, os.F_OK):
                    time.sleep(1)
            return redirect('musicvoting:dbimport')

        else:
            return HttpResponse('Unauthorized', status=401)

def dbimport_status(request):
    try:
        sock = mysocket.Mysocket()
        sock.connect('127.0.0.1', 10000)
        sock.mysend(format(1, '07'))
        number_of_files = int(sock.myreceive())
        sock.close()

        sock = mysocket.Mysocket()
        sock.connect('127.0.0.1', 10000)
        sock.mysend(format(2, '07'))
        number_processed = int(sock.myreceive())
    except:
        number_of_files = -3
        number_processed = 0

    response = {
        'number_of_files': number_of_files,
        'number_processed': number_processed,
    }
    return JsonResponse(response)


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

