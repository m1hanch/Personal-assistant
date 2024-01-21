from django.shortcuts import render
from .utils import get_news, get_tech_news, get_sport_news, get_politics_news


# Create your views here.
def index(request):
    news_objects = get_news()
    return render(request, 'news/index.html', context={'news_objects': news_objects})


def tech_news(request):
    news_objects = get_tech_news('technology')
    return render(request, 'news/news_sections.html', context={'news_objects': news_objects})


def science_news(request):
    news_objects = get_tech_news('science_and_environment')
    return render(request, 'news/news_sections.html', context={'news_objects': news_objects})


def sports_news(request):
    news_objects = get_sport_news()
    return render(request, 'news/news_sections.html', context={'news_objects': news_objects})


def politics_news(request):
    news_objects = get_politics_news()
    return render(request, 'news/news_sections.html', context={'news_objects': news_objects})
