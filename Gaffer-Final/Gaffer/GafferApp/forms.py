from django import forms
from django.core import validators
from GafferApp.models import Drill,Comment, CoachingPlan, Bio
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
import re
import base64


class UserCreateForm(UserCreationForm):
	class Meta:
		fields = ("username", "email", "password1", "password2")
		model = get_user_model()

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["username"].label = "Username"
		self.fields["email"].label = "Email address"


class DrillForm(forms.ModelForm):
	drillImage = forms.CharField(widget=forms.HiddenInput())
	class Meta:
		model = Drill
		fields = ('drillTitle',
		'drillImage',
		'drillDescription',
		'drillType',
		'drillSetup',
		'drillInstruction',
		'drillDate')

		labels = {
			'drillTitle': _('Title'),
			'drillDescription': _('Drill Description'),
			'drillType': _('Drill Type'),
			'drillSetup': _('Drill Setup'),
			'drillInstruction': _('Drill Instruction'),
			'drillDate': _('Drill Date'),
		}

class CoachingPlanForm(forms.ModelForm):
	class Meta:
		model = CoachingPlan
		fields = ('coachingPlanTitle',
		'coachingPlanType',
		'coachingPlanDescription',
		'coachingPlanNotes',
		'coachingPlanDate',
		)

		labels = {
			'coachingPlanTitle': _('Title'),
			'coachingPlanType': _('Coaching Plan Type'),
			'coachingPlanDescription': _('Coaching Plan Description'),
			'coachingPlanDate': _('Coaching Plan Date'),
		}

class AddToPlanForm(forms.Form):
	drillId = forms.IntegerField(widget=forms.HiddenInput(), label="drillId")
	planId = forms.IntegerField(widget=forms.HiddenInput(), label="planId")
	
class EditCoachingPlan(forms.Form):
	planId = forms.IntegerField(widget=forms.HiddenInput(), label="planId")
	planType = forms.CharField(widget=forms.HiddenInput(), label = "planType")
	planDescription = forms.CharField(widget=forms.HiddenInput(), label="planDescription")
	planNotes = forms.CharField(widget=forms.HiddenInput(), label="planNotes")

class BioForm(forms.ModelForm):

	class Meta:
		model = Bio
		fields = ('name',
		 		  'team',
				  'website',
				  'twitterHandle',
				  'bio',
				  'profilePic')

		labels = {
		'name': _('Coach Full Name '),
		'team': _('Team '),
		'website': _('Website URL '),
		'twitterHandle': _('Twitter Handle '),
		'bio': _('About Me '),
		'profilePic': _('Upload Your Picture'),
		}

class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ('author', 'text','rating')

		labels = {
		'author': _('Author'),
		'text': _('Comment'),
		'rating': _('Rating'),
		}
