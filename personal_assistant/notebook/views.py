from .forms import TagForm, NoteForm
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import *

# Create your views here.

# головна сторінка
def main(request):
    notes = Note.objects.all()
    return render(request, 'notebook/index.html', {"notes": notes})

# додавання тегу
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='notebook:main')
        else:
            return render(request, 'notebook/add_tag.html', {'form': form})

    return render(request, 'notebook/add_tag.html', {'form': TagForm()})

def add_note(request):
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)

            return redirect(to='notebook:main')
        else:
            return render(request, 'notebook/add_note.html', {"tags": tags, 'form': form})

    return render(request, 'notebook/add_note.html', {"tags": tags, 'form': NoteForm()})

# Сторінка відображення нотатки
def detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    return render(request, 'notebook/detail.html', {"note": note})


# видалення нотатки
def delete_note(request, note_id):
    Note.objects.get(pk=note_id).delete()
    return redirect(to='notebook:main')
