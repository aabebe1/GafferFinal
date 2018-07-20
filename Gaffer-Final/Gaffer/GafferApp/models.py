# need to install pillow with pip install pillow for Imagefield
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib import auth
from datetime import datetime

class User(auth.models.User, auth.models.PermissionsMixin):

	def __str__(self):
		return "@{}".format(self.username)


# Create your models here.

class CoachProfile(models.Model):
	profileOwner = models.ForeignKey(User,on_delete=models.CASCADE)
	biosketch = models.TextField()
	profilePic = models.ImageField()

	def __str__(self):
		return self.first_name + " " + self.last_name



class Drill(models.Model):

	DRILL_CHOICES = (('Attack','Attack Drill'), ('Defensive','Defensive Drill'),
	('Passing','Passing Drill'),('Dribbling','Dribbling Drill'),
	('Shooting','Shooting Drill'),('Crossing','Crossing Drill'),
	('Goalie','Goalie Drill'),('Other','Other'),)

	drillTitle = models.CharField(max_length = 20)
	drillOwner = models.ForeignKey('auth.User',on_delete=models.CASCADE)
	drillImage = models.TextField()
	drillDescription = models.TextField()
	drillType = models.CharField(max_length = 20,choices= DRILL_CHOICES)
	drillRate = models.IntegerField(null=True)
	drillSetup = models.TextField()
	drillInstruction = models.TextField()
	drillDate = models.DateField(null=True,default=datetime.now)


	def __str__(self):
		return self.drillTitle

	def get_absolute_url(self):
		return reverse("GafferApp:detail",kwargs={'pk':self.pk})
	def approve_comments(self):
		return self.comments.filter(approved_comment=True)

class Comment(models.Model):
	RATING_CHOICES = ((1,1),(2,2),(3,3),(4,4),(5,5))
	comment = models.ForeignKey('GafferApp.Drill', related_name='comments')
	author = models.CharField(max_length=100)
	text = models.TextField()
	rating = models.IntegerField(choices= RATING_CHOICES)
	created_date = models.DateTimeField(default=timezone.now)
	approved_comment = models.BooleanField(default=False)

	def approve(self):
		self.approved_comment = True
		self.save()

	def get_absolute_url(self):
		return reverse("drill_list")

	def __str__(self):
		return self.text



class CoachingPlan(models.Model):
	coachingPlanOwner = models.ForeignKey('auth.User', related_name='plan')
	coachingPlanTitle = models.CharField(max_length = 20)
	coachingPlanType = models.TextField(null=True, blank=True)
	coachingPlanDate = models.DateField(null=True, default=datetime.now)
	coachingPlanDescription = models.TextField(null=True, blank=True)
	coachingPlanNotes = models.TextField(null=True)
	coachingPlanDrill = models.ManyToManyField(Drill)

class Bio(models.Model):
	user = models.ForeignKey('auth.user',related_name='owner')
	name = models.CharField(max_length=60,null=True)
	website = models.URLField(blank=True,null=True)
	twitterHandle = models.CharField(max_length=255,blank=True,null=True)
	team = models.CharField(max_length=60,null=True)
	bio = models.TextField(null=True)
	profilePic = models.ImageField(upload_to='profilepics', default = 'profilepics/placeholder.png', null=True)

	def get_absolute_url(self):
		return reverse("GafferApp:bio_list")


class Player(models.Model):
	playerId = models.IntegerField(unique = True)
	playerJerseyLabel = models.CharField(max_length = 3)
	playerGoalCount = models.IntegerField()
	playerYellowCard= models.IntegerField()
	PlayerRedCard = models.BooleanField()
	playersCoach= models.ForeignKey(User)

class Lineup(models.Model):
	LineupStyle = models.CharField(max_length = 12)
	LineupPlayers = models.ManyToManyField(Player)
	LineupOwner = models.ForeignKey(User)
