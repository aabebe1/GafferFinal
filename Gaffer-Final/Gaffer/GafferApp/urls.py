from django.conf.urls import url
from GafferApp import views
from django.contrib.auth import views as auth_views

app_name = 'GafferApp'

urlpatterns = [


    url(r'^help/$',views.help,name='help'),
    url(r"signup/$", views.SignUp.as_view(), name="signup"),


    url(r"login/$", auth_views.LoginView.as_view(template_name="GafferApp/login.html"),name='login'),
    url(r"logout/$", auth_views.LogoutView.as_view(template_name="GafferApp/logout.html"), name="auth_logout"),


    url(r'^coachprofile/$',views.ProfileView.as_view(),name='coachprofile'),
    url(r'^maindrill/$',views.MaindrillView,name='maindrill'),
    url(r'^lineup/$',views.CreateLineupView.as_view(),name='create_lineup'),
    url(r'^viewlineup/$',views.ViewLineupView.as_view(),name='view_lineup'),
    url(r'^create_plan/$',views.CreateCoachingPlan.as_view(),name='create_coaching_plan'),
    url(r'^view_plan/$',views.ViewCoachingPlan.as_view(),name='view_coaching_plan'),
    url(r'^view_plan/(?P<pk>\d+)/$',views.CoachingPlanDetail.as_view(),name='plan_detail'),

    url(r'^homePage/$',views.HomeView,name='homePage'),
    # url(r'^/$',views.IndexView.as_view(),name='indexPage'),
    url(r'^drill_form/$',views.CreateDrillView.as_view(),name='drillform'),
    url(r'^drill_list/$',views.DrillListView.as_view(),name='drill_list'),
    url(r'^drill_list/(?P<pk>\d+)/$',views.DrillDetailView.as_view(),name='detail'),
    url(r'^drill_list/(?P<pk>\d+)/rating$',views.add_comment_to_drill,name='rating'),
    url(r'^drill_list/(?P<pk>\d+)/remove/$', views.DrillDeleteView.as_view(), name='drill_remove'),
    url(r'^drill_list/(?P<pk>\d+)/edit/$', views.DrillUpdateView.as_view(), name='drill_edit'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
	url(r'^forum/', views.ForumView.as_view(), name='forum'),
    url(r'^bioform/$',views.BioFormView.as_view(),name='bioform'),
    url(r'^bio_list/$',views.ProfileListView.as_view(),name='bio_list'),
    url(r'^bio_list/(?P<pk>\d+)/$',views.ProfileView.as_view(),name='individual_bio_list'),

    url(r'^bio_list/(?P<pk>\d+)/edit/$', views.BioUpdateView.as_view(), name='bio_edit'),

    url(r'^search/$',views.search,name='search'),
]
