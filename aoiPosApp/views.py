from django.shortcuts import redirect, render
from aoiPosApp.forms import LoginForm, RegisterForm

# Create your views here.
def login(request):
    if request.session.get('user_id'):
        return redirect('/pos')

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.user_cache
            
            request.session['user_id'] = user.id
            request.session['user_username'] = user.username
            
            return redirect('/pos')
    else:
        form = LoginForm()

    return render(request, 'aoiPosApp/login.html', {'form': form})

def register (request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            request.session['user_id'] = user.id
            request.session['user_username'] = user.username
            return redirect('pos')

    return render(request, 'aoiPosApp/register.html', {
        'form': form,
    })

def pos (request):
    return render(request, 'aoiPosApp/pos-dashboard.html')

def catalogue (request):
    return render(request, 'aoiPosApp/catalogue.html')

def summary (request):
    return render(request, 'aoiPosApp/summary.html')

def view (request):
    return render(request, 'aoiPosApp/view.html')


def logout (request):
    request.session.flush()
    return redirect('login')