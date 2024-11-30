"""
URL configuration for jobportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from job.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index,name="index"),
    path('user_login', user_login, name="user_login"),
    path('admin_login',admin_login,name="admin_login"),
    path('recruiter_Login', recruiter_login, name="recruiter_login"),
    path('user_signup',user_signup,name="user_signup"),
    path('user_home',user_home,name="user_home"),
    path('recruiter_signup',recruiter_signup,name="recruiter_signup"),
    path('recruiter_home', recruiter_home, name="recruiter_home"),
    path('admin_home', admin_home, name="admin_home"),
    path('view_users', view_users, name="view_users"),
    path('Education/', Education, name='Education'),
    path('IT/', IT, name='IT'),
    path('Finance/', Finance, name='Finance'),
    path('Marketing/', Marketing, name='Marketing'),
    path('Construction/',Construction, name='Construction'),
    path('Healthcare/',Healthcare, name='Healthcare'),
    path('application/',application, name='application'),
    path('contactus/',contactus,name='contactus'),
    path('recruiter_pending', recruiter_pending, name="recruiter_pending"),
    path('delete_user/<int:pid>', delete_user, name="delete_user"),
    path('change_status/<int:pid>', change_status, name="change_status"),
    path('recruiter_accepted', recruiter_accepted, name="recruiter_accepted"),
    path('recruiter_rejected', recruiter_rejected, name="recruiter_rejected"),
    path('recruiter_all', recruiter_all, name="recruiter_all"),
    path('edit_jobdetail/<int:pid>',edit_jobdetail, name="edit_jobdetail"),
    path('change_companylogo/<int:pid>',change_companylogo, name="change_companylogo"),
    path('change_passwordadmin', change_passwordadmin, name="change_passwordadmin"),
    path('change_passworduser', change_passworduser, name="change_passworduser"),
    path('change_passwordrecruiter', change_passwordrecruiter, name="change_passwordrecruiter"),
    path('add_job', add_job, name="add_job"),
    path('job_list', job_list, name="job_list"),
    path('joblistadmin', joblistadmin, name="joblistadmin"),
    path('profile/', user_profile, name='user_profile'),
    path('logout/', logout_view, name='logout'),
    path('listedjobs/', listedjobs, name='listedjobs'),
    path('apply-job/<int:job_id>/', apply_job, name='apply_job'),
    path('ResumeTips/',ResumeTips, name='ResumeTips'),
    path('applied-jobs/', applied_jobs, name='applied_jobs'),
    path('recruiter-dashboard/',recruiter_dashboard, name='recruiter_dashboard'),
    path('view-application/<int:application_id>/', view_application_details, name='view_application_details'),
    path('delete-job/<int:job_id>/', delete_jobdetail, name='delete_jobdetail'),
    path('shortlist/<int:job_id>/<int:application_id>/', shortlist_candidate, name='shortlist_candidate'),
    path('shortlisted/<int:job_id>', view_shortlisted_candidates, name='view_shortlisted_candidates'),
    path('submit_recruiter_feedback/', submit_recruiter_feedback, name='submit_recruiter_feedback'),
    path('submit_jobseeker_feedback/', submit_jobseeker_feedback, name='submit_jobseeker_feedback'),
    path('job_seeker_feedback/', job_seeker_feedback_view, name='job_seeker_feedback'),
    path('recruiter_feedback/', recruiter_feedback_view, name='recruiter_feedback'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)