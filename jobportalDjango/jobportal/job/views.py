from datetime import date

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages

from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .forms import ContactForm
# Create your views here.
def index(request):
    return render(request,'index.html')


def application(request):
    return render(request,'application.html ')

def job_list(request):
    jobs = Job.objects.all()

    # Handling cases where the recruiter might not be found
    for job in jobs:
        try:
            recruiter = job.recruiter
        except Recruiter.DoesNotExist:
            recruiter = None  # Handle this case however you see fit

    return render(request, 'listedjobs.html', {'jobs': jobs})

def admin_login(request):
    error=""
    if request.method =='POST':
        u= request.POST['uname']
        p = request.POST['pwd']
        user= authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    d={'error':error}
    return render(request,'admin_login.html',d)
def user_login(request):
    error=""

    if request.method=="POST":
        u= request.POST['uname'];
        p=request.POST['pwd'];
        user=authenticate(username=u,password=p)
        if user:
            try:
                user1=StudentUser.objects.get(user=user)
                if user1.type=="student":
                    login(request,user)
                    error="no"
                else:
                    error="yes"
            except:
                error="yes"
        else:
            error="yes"

    d={'error':error}
    return render(request,'user_login.html',d)
def recruiter_login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname'];
        p = request.POST['pwd'];
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = Recruiter.objects.get(user=user)
                if user1.type == "recruiter" and user1.status!="pending":
                    login(request, user)
                    error = "no"
                else:
                    error = "not"
            except:
                error = "yes"
        else:
            error = "yes"

    d = {'error': error}
    return render(request,'recruiter_login.html',d)

def recruiter_signup(request):
    error = " "
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        con = request.POST['contact']
        gen = request.POST['gender']
        company = request.POST['company']
        try:
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
            Recruiter.objects.create(user=user, mobile=con, image=i, gender=gen,company=company, type="recruiter",status="pending")
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request,'recruiter_signup.html ',d)

def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login ')
    return render(request,'user_home.html ')

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login ')
    return render(request,'admin_home.html ')
def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login ')
    user=request.user
    recruiter=Recruiter.objects.get(user=user)
    error =" "
    if request.method =='POST':
        f=request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        gen = request.POST['gender']

        recruiter.user.first_name=f
        recruiter.user.last_name = l
        recruiter.mobile =con
        recruiter.gender=gen
        try:
           error="no"
        except:
            error="yes"

        try:
            i=request.FILES['image']
            recruiter.image=i
            recruiter.save()
            error="no"
        except:
           pass
    d={'recruiter':recruiter,'error':error}
    return render(request,'recruiter_home.html ',d)
def Healthcare(request):
    return render(request, 'Healthcare.html')
def Education(request):
    return render(request, 'Education.html')
def IT(request):
    return render(request, 'IT.html')

def Marketing(request):
    return render(request, 'marketing.html')
def Construction(request):
    return render(request, 'Construction.html')
def Finance(request):
    return render(request, 'Finance.html')
def ResumeTips(request):
    return render(request,'ResumeTips.html')
def logout_view(request):
    """
    Log out the user and completely flush the session.
    """
    logout(request)  # Logs out the user
    request.session.flush()  # Explicitly clear all session data
    return redirect('index')  # Redirect to login page

def user_signup(request):
    error =" "
    if request.method =='POST':
        f=request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        con = request.POST['contact']
        gen = request.POST['gender']
        try:
           user= User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
           StudentUser.objects.create(user=user,mobile=con,image=i,gender=gen ,type="student")
           error="no"
        except:
            error="yes"
    d= {'error':error}
    return render(request,'user_signup.html',d)

# def user_profile(request):
#     # Fetch the logged-in user's profile
#     student_user = get_object_or_404(StudentUser, user=request.user)
#
#     # Pass the profile data to the template
#     return render(request, 'profile.html', {
#         'student_user': student_user
#     })


def user_profile(request):
    try:
        # Attempt to get the StudentUser object for the logged-in user
        student_user = StudentUser.objects.get(user=request.user)
    except StudentUser.DoesNotExist:
        # Handle the case where no matching StudentUser is found
        return render(request, 'profile.html', {"message": "Profile not found. Please contact admin."})

    return render(request, 'profile.html', {'student_user': student_user})


def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=StudentUser.objects.all()
    d={'data':data}
    return render(request, 'view_users.html',d)
def contactus(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ContactForm()
    return render(request, 'contactus.html', {'form': form})
def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    student=StudentUser.objects.get(id=pid)
    student.delete()
    return redirect('view_users')

def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status='pending')
    d={'data':data}
    return render(request, 'recruiter_pending.html',d)

def change_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    recruiter=Recruiter.objects.get(id=pid)
    if request.method== "POST":
        s= request.POST['status']
        recruiter.status=s
        try:
            recruiter.save()
            error="no"
        except:
            error="yes"
    d={'recruiter':recruiter,'error':error}
    return render(request, 'change_status.html',d)

def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    if request.method== "POST":
        c= request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
              error="not"
        except:
             error="yes"
    d={'error':error}
    return render(request, 'change_passwordadmin.html',d)

def change_passworduser(request):

    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    if request.method== "POST":
        c= request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
              error="not"
        except:
             error="yes"
    d={'error':error}
    return render(request, 'change_passworduser.html',d)

def change_passwordrecruiter(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""
    if request.method== "POST":
        c= request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
              error="not"
        except:
             error="yes"
    d={'error':error}
    return render(request, 'change_passwordrecruiter.html',d)



def recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status= 'Accept')
    d={'data':data}
    return render(request, 'recruiter_accepted.html',d)
def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status= 'Reject')
    d={'data':data}
    return render(request, 'recruiter_rejected.html',d)

def recruiter_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.all()
    d={'data':data}
    return render(request, 'recruiter_all.html',d)

def add_job(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    error = ""
    if request.method == 'POST':
        jt = request.POST['jobtitle']
        sd = request.POST['startdate']
        ed = request.POST['enddate']
        sal = request.POST['salary']
        l = request.FILES['logo']
        exp = request.POST['experience']
        loc = request.POST['location']
        skills = request.POST['skills']
        des = request.POST['description']
        user = request.user

        try:
            # Try fetching the recruiter associated with the user
            recruiter = Recruiter.objects.get(user=user)

            # Create the job
            Job.objects.create(
                recruiter=recruiter,
                start_date=sd,
                end_date=ed,
                title=jt,
                salary=sal,
                image=l,
                description=des,
                experience=exp,
                location=loc,
                skills=skills,
                creationdate=date.today()
            )
            error = "no"
        except Recruiter.DoesNotExist:
            # Handle the case where the recruiter doesn't exist
            error = "Recruiter profile not found. Please complete your profile first."
        except Exception as e:
            # Handle any other exceptions (e.g., database issues)
            error = f"An error occurred: {str(e)}"

    d = {'error': error}
    return render(request, 'add_job.html', d)



def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Check if the user has already applied
    user_has_applied = Application.objects.filter(user=request.user, job=job).exists()
    if user_has_applied:
        # Send a message to the template
        messages.info(request, "You have already applied for this job.")
        return render(request, 'Apply_job.html', {'job': job, 'user_has_applied': True})

    # Handle form submission
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            postal_code = request.POST.get('postal_code')
            experience_level = request.POST.get('experience_level')
            cover_letter = request.FILES.get('cover_letter')
            resume = request.FILES.get('resume')

            if not resume:
                messages.error(request, 'Resume file is required.')
                return redirect('apply_job', job_id=job.id)

            # Create application
            Application.objects.create(
                user=request.user,
                job=job,
                name=name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                state=state,
                postal_code=postal_code,
                experience_level=experience_level,
                cover_letter=cover_letter,
                resume=resume
            )
            messages.success(request, 'Application submitted successfully!')
            return redirect('applied_jobs')

        except Exception as e:
            # Log the exception for debugging
            print(f"Error: {e}")
            messages.error(request, "Something went wrong. Please try again.")
            return redirect('apply_job', job_id=job.id)

    # Render the form for applying to a job
    return render(request, 'Apply_job.html', {'job': job, 'user_has_applied': False})




def applied_jobs(request):
    applications = Application.objects.filter(user=request.user)  # Filter by logged-in user
    return render(request, 'applied_jobs.html', {'applications': applications})

def listedjobs(request):
    jobs = Job.objects.all()  # Fetch all jobs from the database
    context = {'jobs': jobs}
    return render(request, 'listedjobs.html', context)



    return render(request, 'job_details.html', {'job': job, 'form': form})
def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    job = Job.objects.filter(recruiter=recruiter)
    context = {'job': job}
    return render(request, 'job_list.html', context)


def joblistadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    # Fetch all jobs with recruiter details for Admin
    jobs = Job.objects.select_related('recruiter').all()  # Efficient fetching with related recruiter
    context = {'jobs': jobs}
    return render(request, 'joblistadmin.html', context)


def edit_jobdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""
    job = Job.objects.get(id=pid)
    if request.method == 'POST':
        jt = request.POST['jobtitle']
        sd = request.POST['startdate']
        ed = request.POST['enddate']
        sal = request.POST['salary']
        exp = request.POST['experience']
        loc = request.POST['location']
        skills = request.POST['skills']
        des = request.POST['description']

        job.title = jt
        job.salary = sal
        job.experience = exp
        job.skills = skills
        job.description=des


        try:
            job.save()
            error = "no"
        except:
            error = "yes"
        if sd:
            try:
                job.start_date = sd
                job.save()
            except:
                pass
        if ed:
            try:
                job.end_date = ed
                job.save()
            except:
                pass
        else:
            pass


    d = {'error': error,'job':job}
    return render(request, 'edit_jobdetail.html',d)

def change_companylogo(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""
    job = Job.objects.get(id=pid)
    if request.method == 'POST':

        cl = request.FILES['logo']
        job.image=cl

        try:
            job.save()
            error = "no"
        except:
            error = "yes"

    d = {'error': error,'job':job}
    return render(request, 'change_companylogo.html',d)


def recruiter_dashboard(request):
    # Ensure the user is a recruiter
    if not hasattr(request.user, 'recruiter'):
        return HttpResponse("You are not authorized to view this page", status=403)

    recruiter = request.user.recruiter

    # Fetch jobs and applications
    recruiter_jobs = Job.objects.filter(recruiter=recruiter)
    job_applications = {
        job: Application.objects.filter(job=job)
        for job in recruiter_jobs
    }

    return render(request, 'recruiter_dashboard.html', {'job_applications': job_applications})

def view_application_details(request, application_id):
    application = Application.objects.get(id=application_id)
    return render(request, 'application_details.html', {'application': application})



def delete_jobdetail(request, job_id):
    if request.method == "POST":
        job = get_object_or_404(Job, id=job_id)

        job.delete()

        messages.success(request, "The job has been successfully deleted.")

        if request.user.is_staff:
            return redirect('joblistadmin')
        else:
            return redirect('recruiter_dashboard')


def shortlist_candidate(request, job_id, application_id):
    try:
        # Get the job and the application
        job = Job.objects.get(id=job_id)
        application = Application.objects.get(id=application_id)

        # Add the application to the shortlisted candidates list
        job.shortlisted_candidates.add(application)
        job.save()

        # Redirect back to the recruiter dashboard or the job details page
        return redirect('recruiter_dashboard')  # Use 'redirect' for simplicity
    except Job.DoesNotExist:
        return redirect('error')  # Redirect to an error page if the job doesn't exist
    except Application.DoesNotExist:
        return redirect('error')
# View to display shortlisted candidates for a specific job
def view_shortlisted_candidates(request, job_id):
    job = Job.objects.get(id=job_id)
    shortlisted_candidates = job.shortlisted_candidates.all()
    shortlisted_candidates = job.shortlisted_candidates.all()

    return render(request, 'shortlisted_candidates.html', {
        'job': job,
        'shortlisted_candidates': shortlisted_candidates
    })

def submit_recruiter_feedback(request):
    if request.method == 'POST':
        company = request.POST.get('company')
        email = request.POST.get('email')
        feedback = request.POST.get('feedback')

        # Save to the database
        new_feedback = RecruiterFeedback(company=company, email=email, feedback=feedback)
        new_feedback.save()

        # Redirect to the thank you page
        return render(request, 'thank_you.html', {'feedback_type': 'Recruiter'})

    # Handle GET request: render the feedback form
    return render(request, 'RecruiterFeedback.html')
# For Job Seeker Feedback
def submit_jobseeker_feedback(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        feedback = request.POST.get('feedback')

        # Save to the database
        new_feedback = JobSeekerFeedback(full_name=full_name, email=email, feedback=feedback)
        new_feedback.save()

        return render(request, 'thank_you.html', {'feedback_type': 'Job Seeker'})

    return render(request, 'JobseekerFeedback.html')
def job_seeker_feedback_view(request):
    feedbacks = JobSeekerFeedback.objects.all()  # Get all job seeker feedback
    return render(request, 'jobseekersfeedbackpage.html', {'job_seeker_feedback': feedbacks})

def recruiter_feedback_view(request):
    feedbacks = RecruiterFeedback.objects.all()  # Get all recruiter feedback
    return render(request, 'recruitersfeedback.html', {'recruiter_feedback': feedbacks})