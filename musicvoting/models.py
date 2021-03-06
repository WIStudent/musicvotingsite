from django.db import models

# Create your models here.
class Artist(models.Model):
    artist_name = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % self.artist_name

class Album(models.Model):
    album_name = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % self.album_name

class User(models.Model):
    pass

class Track(models.Model):
    artist = models.ForeignKey(Artist)
    album = models.ForeignKey(Album)
    track_number = models.IntegerField(default=0)
    title = models.CharField(max_length=150)
    lenth = models.IntegerField(default=0)
    path = models.TextField()
    voting_users = models.ManyToManyField(User)
    votes= models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s -- %s -- %s' % (self.artist.artist_name, self.album.album_name, self.title)
