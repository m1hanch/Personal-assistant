from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .forms import ContactForm
from .models import Contact


@login_required
def index(request):
    contacts = Contact.objects.filter(user=request.user)

    query = request.GET.get('q')
    if query:
        contacts = contacts.filter(Q(first_name__icontains=query) |
                                   Q(last_name__icontains=query) |
                                   Q(phone__icontains=query))

    days_param = request.GET.get('days')
    try:
        days = int(days_param)
    except (TypeError, ValueError):
        days = None

    if days is not None:
        today = timezone.now().date()
        future_date = today + timedelta(days=int(days))

        end_of_year_birthdays = Q(birthday__month=today.month, birthday__day__gte=today.day) | Q(
            birthday__month__gt=today.month)

        start_of_year_birthdays = Q(birthday__month=future_date.month, birthday__day__lte=future_date.day) | Q(
            birthday__month__lt=future_date.month)

        if future_date.year > today.year:
            contacts = contacts.filter(
                end_of_year_birthdays |
                start_of_year_birthdays
            )
        else:
            contacts = contacts.filter(
                end_of_year_birthdays & start_of_year_birthdays
            )

    return render(request, 'addressbook/index.html', context={'contacts': contacts})

@login_required
def add_contact(request):
    contacts = Contact.objects.filter(user=request.user)  # noqa
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=Contact())
        if form.is_valid():
            new_contact = form.save(commit=False)
            new_contact.user_id = request.user.id
            form.save()
        else:
            return render(request, 'addressbook/index.html', context={'form': form, 'contacts': contacts})
    return redirect('addressbook:index')

@login_required
def edit_contact(request, contact_id):
    if request.user.is_authenticated:
        contact = get_object_or_404(Contact, id=contact_id, user=request.user)
        if request.method == 'POST':
            form = ContactForm(request.POST, instance=contact)
            if form.is_valid():
                form.save()
                return redirect('addressbook:index')
        else:
            form = ContactForm(instance=contact)
        return render(request, 'addressbook/edit_contact.html', {'form': form, 'contact': contact})
    else:
        return redirect('addressbook:index')

@login_required
def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, user=request.user)

    if request.method == 'POST':
        contact.delete()
        return redirect('addressbook:index')

    return render(request, 'addressbook/confirm_delete.html', {'contact': contact})
