from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
from interest.models import Interest
from urllib.request import urlopen
import datetime

# Create your views here.


def interest(request):
    if request.method == 'POST':

        if request.POST['date'] == '':
            return redirect('interest:third')

        Interest.objects.all().delete()

        year = request.POST['date'].split('-')[0]
        month = request.POST['date'].split('-')[1]
        day = request.POST['date'].split('-')[2]
        date = year + month + day


        url = urlopen('https://music.bugs.co.kr/chart/track/day/total?chartdate=' + date)
        soup = BeautifulSoup(url, 'lxml')

        artists = []
        titles = []

        for link1 in soup.find_all(name='p', attrs={'class': 'artist'}):
            artists.append(link1.find('a').text)

        for link2 in soup.find_all(name='p', attrs={'class': 'title'}):
            titles.append(link2.text.split('\n')[1])

        result = zip(artists, titles)

        for a, t in result:
            obj = Interest(title=t, artist=a)
            obj.save()

        interests = Interest.objects.all()

        return render(request, 'index.html', {'charts': interests, 'date': year+'.'+month+'.'+day})
