from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(StudentUser)
admin.site.register(Recruiter)
admin.site.register(ContactMessage)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(RecruiterFeedback)
admin.site.register(JobSeekerFeedback)