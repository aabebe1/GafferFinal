from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView,ListView,
								  DetailView,CreateView,
								  UpdateView,DeleteView,
								  FormView)

from django.urls import reverse_lazy
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.http import Http404
from django.http import HttpResponse
from GafferApp.models import Drill,CoachProfile,CoachingPlan,Player,Lineup,Comment, Bio
from GafferApp.forms import DrillForm,CommentForm, UserCreateForm, CoachingPlanForm, AddToPlanForm, BioForm, EditCoachingPlan
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.views import password_reset
from django.db.models import Q
import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



from . import forms

# def index(request):
#     my_dict = {'insert_me':"Hello this is from view.py!"}
#     return render(request,'GafferApp/index.html',context = my_dict)
# Create your views here.

def help(request):
	my_help = {'insert_help': "This is going to be your help page"}

class SignUp(CreateView):
	form_class = forms.UserCreateForm
	success_url = reverse_lazy("GafferApp:login")
	template_name = "GafferApp/signup.html"


# class LogoutView(LoginRequiredMixin, TemplateView):
	# template_name = 'GafferApp/logout.html'

def logout_view(request):
	logout(request)
	return redirect('GafferApp/logout.html')

class ProfileView(DetailView):
	context_object_name = 'bio_details'
	model = Bio
	template_name = 'GafferApp/coachprofile.html'

	def get(self, request, *args, **kwargs):
		try:
			self.object = self.get_object()
		except Http404:
            # redirect here
			return redirect('GafferApp:bio_list')
		context = self.get_context_data(object=self.object)
		return self.render_to_response(context)

class ProfileListView(ListView):
	model = Bio
	context_object_name = 'bios_list'
	template_name = 'GafferApp/bio_list.html'
	paginate_by=10

	# def get_queryset(self, **kwargs):
	# 	return super(ProfileListView, self).get_queryset()

class BioFormView(LoginRequiredMixin, CreateView):
	form_class = BioForm
	model = Bio
	template_name='GafferApp/bio.html'
	success_url='/GafferApp/bio_list/'

	def form_valid(self, form):
		self.object = form.save(commit = False)
		user = User.objects.get(id = self.request.user.id)
		self.object.user = user
		self.object.save()
		return super().form_valid(form)

class BioUpdateView(LoginRequiredMixin,UpdateView):
	login_url = 'GafferApp/login.html'
	redirect_field_name = 'GafferApp/CoachProfile.html'
	template_name = 'GafferApp/bio.html'
	form_class = BioForm

	model = Bio


class CreateCoachingPlan(LoginRequiredMixin, CreateView):
	form_class = CoachingPlanForm
	model = CoachingPlan
	template_name = 'GafferApp/create_coachingplan.html'
	success_url  = '/GafferApp/view_plan/'

	def form_valid(self, form):
		self.object = form.save(commit = False)
		user = User.objects.get(id = self.request.user.id)
		self.object.coachingPlanOwner = user
		self.object.save()
		return super().form_valid(form)

	def get_initial(self):
		initial = super().get_initial()
		initial.update({'coachingPlanOwner': self.request.user})
		return initial

	def get_absolute_url(self):
		return reverse('view_coaching_plan', args = (self.pk),)

class ViewCoachingPlan(ListView):
	model = CoachingPlan
	context_object_name = 'coachingPlans_list'
	template_name = 'GafferApp/view_coaching_plan.html'
	paginate_by = 20;

	def get_queryset(self, **kwargs):
		return super(ViewCoachingPlan, self).get_queryset()

class CoachingPlanDetail(DetailView):
	context_object_name = 'plan_details'
	model = CoachingPlan
	template_name = 'GafferApp/coaching_plan_detail.html'

	def form_valid(self, form):
		self.object = form.save(commit = False)
		self.object.save()
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(CoachingPlanDetail, self).get_context_data(**kwargs)
		context['form'] = EditCoachingPlan
		return context

	def post(self, request, pk):
		form = EditCoachingPlan(request.POST)
		if form.is_valid():
			#update the plan
			myPlan = CoachingPlan.objects.filter(pk = form['planId'].value())
			myPlan.update(coachingPlanType = form['planType'].value())
			myPlan.update(coachingPlanDescription = form['planDescription'].value())
			myPlan.update(coachingPlanNotes = form['planNotes'].value())

			return redirect('GafferApp:plan_detail', pk=form['planId'].value())

def MaindrillView(request):
	drills = Drill.objects.all()
	drill_dict = {'drills_list':drills}
	return render(request,'GafferApp/drill_list.html',context = drill_dict)

# class IndexView(TemplateView):
#     template_name = 'GafferApp/homePage.html'

def HomeView(request):

	drills = Drill.objects.all()
	drill_dict = {'drills':drills}
	return render(request,'GafferApp/homePage.html',context = drill_dict)


class CreateLineupView(LoginRequiredMixin,TemplateView):
	template_name = 'GafferApp/lineup.html'

class ViewLineupView(TemplateView):
	template_name = 'GafferApp/viewlineup.html'


class CreateDrillView(LoginRequiredMixin,CreateView):
	form_class= DrillForm
	model = Drill
	template_name = 'GafferApp/drill_form.html'
	# redirect_field_name = '/GafferApp/drill_list.html'
	success_url  =    '/GafferApp/maindrill/'
	# http_method_names = ['post']

	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return
		self.object = form.save(commit = False)
		user = User.objects.get(id=self.request.user.id)
		self.object.drillOwner = user
		self.object.drillRate = 0
		self.object.save()
		return super().form_valid(form)


	# def get_initial(self):
	#     initial = super(CreateDrillView, self).get_initial()
	#     initial.update({'drillRate': 0 })
	#     return initial


class DrillListView(ListView):
	model = Drill
	context_object_name = 'drills_list'
	template_name = 'GafferApp/drill_list.html'
	paginate_by = 3;


	def get_queryset(self, **kwargs):
		# queryset= super(DrillListView, self).get_queryset()
		#
		# drillType= self.request.GET.get('drillType', None)
		#
		# if drillType == 'Attacking Drill':
		#     queryset = queryset.filter(drillType = 'Attack')
		# return queryset
		# drillType= self.request.GET.get('drillTy', None)

		if 'attack' in self.request.GET:
			return Drill.objects.filter(drillType = 'Attack').order_by('drillRate')
		elif 'defense' in self.request.GET:
			return Drill.objects.filter(drillType = 'Defensive')
		elif 'pass' in self.request.GET:
			return Drill.objects.filter(drillType = 'Passing')
		elif 'shoot' in self.request.GET:
			return Drill.objects.filter(drillType = 'Shooting')
		elif 'dribble' in self.request.GET:
			return Drill.objects.filter(drillType = 'Dribbling')
		elif 'cross' in self.request.GET:
			return Drill.objects.filter(drillType = 'Crossing')
		elif 'goalie' in self.request.GET:
			return Drill.objects.filter(drillType = 'Goalie')
		elif 'other' in self.request.GET:
			return Drill.objects.filter(drillType = 'Other')


		return super(DrillListView, self).get_queryset()

class DrillDetailView(DetailView):
	context_object_name = 'drill_details'
	model = Drill
	template_name = 'GafferApp/drill_detail.html'

	def form_valid(self, form):
		self.object = form.save(commit = False)
		self.object.save()
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(DrillDetailView, self).get_context_data(**kwargs)
		if (self.request.user.is_authenticated):
			context['userPlans'] = CoachingPlan.objects.filter(coachingPlanOwner = self.request.user)

		context['form'] = AddToPlanForm
		return context

	def post(self, request, pk):
		form = AddToPlanForm(request.POST)
		if form.is_valid():
			#add the drill to the coaching plan
			myPlan = CoachingPlan.objects.get(pk = form['planId'].value())
			myDrill = Drill.objects.get(pk = form['drillId'].value())
			myPlan.coachingPlanDrill.add(myDrill)
			return redirect('GafferApp:plan_detail', pk=myPlan.pk)


class DrillDeleteView(LoginRequiredMixin,DeleteView):
	model = Drill
	success_url = reverse_lazy('GafferApp:drill_list')


class DrillUpdateView(LoginRequiredMixin,UpdateView):
	login_url = 'GafferApp/login.html'
	redirect_field_name = 'GafferApp/drill_detail.html'

	form_class = DrillForm

	model = Drill

class ForumView(TemplateView):
	template_name = 'GafferApp/forum.html'

@login_required
def add_comment_to_drill(request, pk):
	drill = get_object_or_404(Drill, pk=pk)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.comment = drill
			if(drill.drillRate == 0):
				drill.drillRate = comment.rating
			else:
				drill.drillRate = (((comment.rating + (drill.drillRate * (Comment.objects.filter(comment=drill).count()) )))/ (Comment.objects.filter(comment=drill).count() + 1))

			drill.save()
			comment.save()
			return redirect('GafferApp:detail', pk=drill.pk)
	else:
		form = CommentForm()
	return render(request, 'GafferApp/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.approve()
	return redirect('drill_detail', pk=comment.comment.pk)


@login_required
def comment_remove(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment_pk = comment.comment.pk
	comment.delete()
	return redirect('drill_detail', pkcomment_pk)


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search(request):
	query_string = ''
	found_entries = None
	found_entries_paged = None
	if ('q' in request.GET) and request.GET['q'].strip():
		query_string = request.GET['q']
		entry_query = get_query(query_string, ['drillTitle', 'drillDescription','drillSetup','drillInstruction'])
		found_entries = Drill.objects.filter(entry_query).order_by('drillRate')
		page = request.GET.get('page',1)
		paginator = Paginator(found_entries, 1)
		try:
			found_entries_paged = paginator.page(page)
		except PageNotAnInteger:
			found_entries_paged = paginator.page(1)
		except EmptyPage:
			found_entries_paged = paginator.page(paginator.num_pages)

	return render(request,'GafferApp/search_results.html',{'query_string': query_string, 'found_entries': found_entries_paged })
