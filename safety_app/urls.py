from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('hub/', views.training_hub, name='training_hub'),
    path('start-assessment/', views.start_assessment, name='start_assessment'),
    path('retest-weak-areas/', views.retest_weak_areas, name='retest_weak_areas'),
    path('assessment/', views.take_assessment, name='take_assessment'),
    path('submit-assessment/', views.submit_assessment, name='submit_assessment'),
    path('results/<int:attempt_id>/', views.results_view, name='results'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('set-api-key/', views.set_api_key, name='set_api_key'),
]
