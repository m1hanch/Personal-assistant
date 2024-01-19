from django.shortcuts import render, redirect

from .forms import ContactForm
from .models import Contact


# Create your views here.
def index(request):
    contacts = Contact.objects.filter(user=request.user) # noqa
    return render(request, 'addressbook/index.html', context={'contacts': contacts})

def add_contact(request):
    contacts = Contact.objects.filter(user=request.user)  # noqa
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=Contact())
        if form.is_valid():
            new_contact = form.save(commit=False)
            new_contact.user_id = request.user.id
            form.save()
        else:
            return render(request, 'addressbook/index.html', context={'form': form,'contacts': contacts})
    return redirect(to='addressbook:index')