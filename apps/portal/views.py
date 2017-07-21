from django.shortcuts import render, redirect, HttpResponse
from .models import User, Quote
from django.contrib import messages
import bcrypt
# Create your views here.

# LANDING PAGE
def landing(request):
    return render(request, 'portal/landing.html')


def login(request):
    if request.method == 'POST':
        try:
            get_email = User.objects.get(email = request.POST['email'])
            if bcrypt.checkpw(request.POST['password'].encode(), get_email.password.encode()):
                request.session['user_id'] = get_email.id

                current_user = User.objects.get(id=request.session['user_id'])              
                return redirect('/quotes')
        except:
            messages.error(request, 'Your Login information does not match our database. Please try again.')
        
    return redirect('/')

def register(request):
    if request.method == 'POST':
        # validate our form data
        errors = User.objects.the_awesome_validator(request.POST)

        # populate messages with errors if true
        if len(errors):
            for error in errors:
                messages.error(request, error)
            return redirect('/register')
        else:
        # if no errors
            try:
                # check email if it already exists in the database.
                check_email = User.objects.get(email = request.POST['email'])
                messages.error(request, 'This email already exists.')
                return redirect('/')
            except:
                # hash password
                hash_it = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

                # insert user into database
                user = User(first_name=request.POST['first_name'], last_name=request.POST['last_name'],email=request.POST['email'],password=hash_it,birthday=request.POST['birthday'])       
                user.save()
                messages.success(request, 'You have successfully registered')
    return redirect('/')



# LOGOFF
def logoff(request):
    request.session.clear()
    return redirect('/')


# HOME
def success(request):
    if 'user_id' not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])

    #  displays all quotes
    quotes = Quote.objects.exclude(favorited_bys=user)

    # displays all favorites
    favorites = user.favorite_quotes.all()



    context = {
        'quotes' : quotes,
        'current_user_id' : request.session['user_id'],
        'favorites' : favorites,
        'user' : user
    }

    return render(request, 'portal/success.html', context)

def process(request):
    if request.method == 'POST':
        errors = Quote.objects.quote_validator(request.POST)
        if len(errors):
            for error in errors:
                messages.error(request, error)
            return redirect('/quotes')
        else:
            user = User.objects.get(id=request.session['user_id'])
            quote = Quote(title=request.POST['title'],content=request.POST['content'],user=user)
            quote.save()
    return redirect('/quotes')

def add_favorite(request, user_id):
    if request.method == 'POST':
        recipient = User.objects.get(id=user_id)
        favorite_quote = Quote.objects.get(id=request.POST['quote'])
        favorite_quote.favorited_bys.add(recipient)
        favorite_quote.save()
    return redirect('/quotes')


def remove_favorite(request, user_id):
    if request.method == 'POST':
        recipient = User.objects.get(id=user_id)
        favorite_quote = Quote.objects.get(id=request.POST['quote'])
        recipient.favorite_quotes.remove(favorite_quote)
    return redirect('/quotes')


# USER

def profile(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')

    # query the user
    user = User.objects.get(id=user_id)
    
    # get all quotes posted by the user
    quotes = user.quotes.all()

    context = {
        'user' : user,
        'quotes': quotes
    }

    return render(request, 'portal/profile.html', context)