from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

#GET #GET #GET
#GET #GET #GET
#GET #GET #GET

def catch_all(request, url):
    return render(request, "catch_all.html")

def login(request):
    return render(request, "login.html")

def index(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'all_polls': Poll.objects.all(),
    }    
    return render(request, "index.html", context)

def your_polls(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        #current_user = User.objects.get(id=request.session['user_id'])
        context = {
            'current_user': User.objects.get(id=request.session['user_id']),
            'user_polls': User.objects.get(id=request.session['user_id']).Polls.all()
        }
        return render(request, "your_polls.html", context)
    return redirect("/")

def poll_form(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        # 'all_polls': Poll.objects.all(),
    }
    return render(request, "create_poll.html", context)         

def poll_view(request, poll_id):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        this_poll = Poll.objects.get(id=poll_id)
        this_poll_answers = this_poll.answers.all()
        this_user = User.objects.get(id=request.session['user_id'])#THE USER
        participant_filter = Poll.objects.get(id=poll_id).participants.filter(id=request.session['user_id'])
        print(participant_filter)
        if len(participant_filter) >= 1:
            return poll_results(request, poll_id)
        author = Poll.objects.get(id=poll_id).author
        if author == this_user:
            return poll_results(request, poll_id)
        else:
            context = {
                'this_poll':this_poll,
                'this_poll_answers':this_poll_answers,
            }
            return render(request, "view_poll.html", context)
        return redirect("/index")
    return redirect("/index")

def poll_results(request, poll_id):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        this_poll = Poll.objects.get(id=poll_id)
        this_poll_answers = this_poll.answers.all()
        total_part = len(this_poll.participants.all())
        print(total_part)
        # total_part = len(Poll.objects.get(id=poll_id).participants.all())
        for answer in this_poll_answers:
            if total_part:
                total_percent = (len(answer.chooser.all())/total_part)*100
            else:
                total_percent = 0
            print (total_percent)
            answer.percentage = total_percent
            answer.save()            
        context = {
            'this_poll_answers':this_poll_answers,
            'this_polls_name':this_poll.question_text,
            'current_user':User.objects.get(id=request.session['user_id'])
        }
        return render(request, "results.html", context)
    return redirect('/')

#POST #POST #POST
#POST #POST #POST
#POST #POST #POST

def create_user(request):
    if request.method == "POST":
        print(request.POST)
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['user_password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()   
            print(pw_hash)
            user = User.objects.create(f_name=request.POST['first_name'], l_name=request.POST['last_name'], email=request.POST['user_email'], password=pw_hash)
            request.session['user_id'] = user.id
            return redirect('/index')
    return redirect('/')

def login_user(request):
    if request.method == "POST":
        user_with_email = User.objects.filter(email=request.POST['existing_email'])
        if user_with_email:
            user = user_with_email[0]
            if bcrypt.checkpw(request.POST['user_password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/index')
        messages.error(request, "Email or password is incorrect")
    return redirect('/')

def logout_user(request):
    request.session.flush()
    return redirect('/')

#Polls #Polls #Polls #Polls #Polls #Polls

def create_poll(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        print(request.POST)
        errors = Poll.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/index')
        else:
            poll = Poll.objects.create(question_text=request.POST['question_text'], author=User.objects.get(id=request.session['user_id']))
            request.session['poll_id'] = poll.id
            #You can have a success message here by saying: messages.success(request, "Your comment has been submitted.")
            Answer.objects.create(answer_text=request.POST['answer_text1'], related_poll=Poll.objects.get(id=request.session['poll_id']))
            Answer.objects.create(answer_text=request.POST['answer_text2'], related_poll=Poll.objects.get(id=request.session['poll_id']))
            return redirect('/index')
    return redirect('/index')

def vote(request, answer_id, poll_id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        # this_answer = Answer.objects.filter(id=answer_id)
        this_answer = Answer.objects.get(id=request.POST['answer'])#THE ANSWER THE USER SELECTED
        this_user = User.objects.get(id=request.session['user_id'])#THE USER
        participant_filter = Poll.objects.get(id=poll_id).participants.filter(id=request.session['user_id'])
        print(participant_filter)
        #this_users_answers = this_user.chosen_answers.all()#ALL THE ANSWERS THE USER HAS SELECTED
        #ans_in_this_poll = this_users_answers.filter(id=answer_id)
        #if len(ans_in_this_poll) >= 1:
        if len(participant_filter) >= 1:
            return poll_results(request, poll_id)
        author = Poll.objects.get(id=poll_id).author
        if author == this_user:
            return poll_results(request, poll_id)
        else:
            this_answer.chooser.add(this_user)
            this_poll = this_answer.related_poll
            this_poll.participants.add(this_user)
            return poll_results(request, poll_id)
    return redirect("/index")
    

def delete_poll(request, poll_id, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        this_poll = Poll.objects.get(id=poll_id)
        this_poll.delete()
        return (your_polls(request, user_id))
    return ("/index")


