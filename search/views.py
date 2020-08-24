from django.shortcuts import render, redirect, get_object_or_404
from search.models import Keywords, Theme, Chart, Name
import json
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from urllib.request import urlopen
import datetime
from urllib import parse
from django.core.paginator import Paginator
# Create your views here.


def keyword(request):
    if request.method == 'POST':
        Keywords.objects.all().delete()

        parts = urlparse(
            'https://www.music-flo.com/api/search/v2/search?keyword=%EB%B2%84%EC%A6%88&searchType=TRACK&sortType=ACCURACY&size=100&page=1&timestamp=1597282813278')
        qs = dict(parse_qsl(parts.query))
        qs['keyword'] = request.POST['name']
        parts = parts._replace(query=urlencode(qs))
        new_url = urlunparse(parts)

        u = urlopen(new_url)

        data = u.read()
        j = json.loads(data)
        obj = j['data']['list'][0]['list']

        for i in range(min(len(obj), 100)) :
            song = obj[i]['name'] if 'name' in obj[i].keys() else '노래 제목을 알 수 없습니다.'
            album = obj[i]['album']['title'] if ('album' in obj[i].keys()) & ('title' in obj[i]['album'].keys()) else '앨범명을 알 수 없습니다.'
            artist = obj[i]['representationArtist']['name'] if ('representationArtist' in obj[i].keys()) & ('name' in obj[i]['representationArtist'].keys()) else '아티스트를 알 수 없습니다.'
            id = obj[i]['id'] if 'id' in obj[i].keys() else ''
            image = obj[i]['album']['imgList'][0]['url']

            if id:
                urls = str('https://www.music-flo.com/api/meta/v1/track/' + str(id) + '?timestamp=1597384768991')
                parts_d = urlparse(urls)
                qs_d = dict(parse_qsl(parts_d.query))
                parts_d = parts_d._replace(query=urlencode(qs_d))
                new_url_d = urlunparse(parts_d)

                u_d = urlopen(new_url_d)
                data_d = u_d.read()
                j_d = json.loads(data_d)

                if 'data' in j_d.keys():
                    obj_d = j_d['data']
                    lyrics = obj_d['lyrics'] if 'lyrics' in obj_d.keys() else '가사정보가 없습니다.'
                    try:
                        release = datetime.datetime.strptime(obj_d['album']['releaseYmd'], '%Y%m%d').strftime('%Y.%m.%d') if ('album' in obj_d.keys()) & ('releaseYmd' in obj_d['album'].keys()) else '앨범 발매연도를 알 수 없습니다.'
                    except:
                        release = obj_d['album']['releaseYmd']
                    genre = obj_d['album']['genreStyle'] if ('album' in obj_d.keys()) & ('genreStyle' in obj_d['album'].keys()) else '장르정보가 없습니다.'
                else:
                    lyrics = '가사정보가 없습니다.'
                    release = '앨범 발매연도를 알 수 없습니다.'
                    genre = '장르정보가 없습니다.'

            else:
                lyrics = '가사정보가 없습니다.'
                release = '앨범 발매연도를 알 수 없습니다.'
                genre = '장르정보가 없습니다.'

            tmp = Keywords(song=song, album=album, artist=artist, lyrics=lyrics, release=release, genre=genre, image=image)
            tmp.save()

        contents = Keywords.objects.all()

        """
        pybo 목록출력
        """
        # ---------------------------------------- [edit] ---------------------------------------- #
        # 입력 파라미터
        page = request.GET.get('page', '1')  # 페이지

        # 조회
        song = Keywords.objects.order_by('-id')

        # 페이징처리
        paginator = Paginator(song, 10)  # 페이지당 10개씩 보여주기
        page_obj = paginator.get_page(page)

        return render(request, 'keyword.html', {'contents': contents, 'keyword': request.POST['name'], 'song': page_obj,
                                                'video': 'https://www.youtube.com/embed/nM0xDI5R50E'})


import re  # 정규표현식
import requests

def video(request):
    url = 'https://www.youtube.com/results?search_query=' + parse.quote(request.POST['video'])
    html = requests.get(url).text
    for w in re.findall('"url":"/watch\?v=(.*?)"', str(html)):
        if '=' not in w:
            link = w
            break
    url = 'https://www.youtube.com/embed/' + link

    return render(request, 'video.html', {'url': url})


def theme(request):
    if request.method == 'POST':

        if request.POST.get('movie'):
            name = request.POST['movie']
            type = 'movie'

        elif request.POST.get('drama'):
            name = request.POST['drama']
            type = 'drama'

        elif request.POST.get('musical'):
            name = request.POST['musical']
            type = 'musical'

        Theme.objects.filter(type=type).delete()

        #1
        parts = urlparse(
            'https://www.music-flo.com/api/search/v2/search?searchType=ALBUM&sortType=ACCURACY&timestamp=1597825544349')
        qs = dict(parse_qsl(parts.query))
        qs['keyword'] = name + 'ost'
        parts = parts._replace(query=urlencode(qs))
        new_url = urlunparse(parts)

        u = urlopen(new_url)

        data = u.read()
        j = json.loads(data)
        obj = j['data']['list'][0]['list']

        if len(obj) == 1:
            album_id = obj[0]['id']

        else:
            for i in range(len(obj)) :
                if obj[i]['representationArtist']['name'] == 'Various Artists':
                    album_id = obj[i]['id']

        urls = str('https://www.music-flo.com/api/meta/v1/album/' + str(album_id) + '/track?timestamp=1597824172509')
        u_d = urlopen(urls)
        data_d = u_d.read()
        j_d = json.loads(data_d)
        obj = j_d['data']['list']

        for i in range(len(obj)):
            song = obj[i]['name'] if 'name' in obj[i].keys() else '노래 제목을 알 수 없습니다.'
            album = obj[i]['album']['title'] if ('album' in obj[i].keys()) & ('title' in obj[i]['album'].keys()) else '앨범명을 알 수 없습니다.'
            artist = obj[i]['representationArtist']['name'] if ('representationArtist' in obj[i].keys()) & ('name' in obj[i]['representationArtist'].keys()) else '아티스트를 알 수 없습니다.'
            id = obj[i]['id'] if 'id' in obj[i].keys() else ''

            urls = str('https://www.music-flo.com/api/meta/v1/track/' + str(id) + '?timestamp=1597824526912')
            u_d = urlopen(urls)
            data_d = u_d.read()
            j_d = json.loads(data_d)
            obj_d = j_d['data']

            if 'data' in j_d.keys():
                obj_d = j_d['data']
                lyrics = obj_d['lyrics'] if 'lyrics' in obj_d.keys() else '가사정보가 없습니다.'
                try:
                    release = datetime.datetime.strptime(obj_d['album']['releaseYmd'], '%Y%m%d').strftime('%Y.%m.%d') if ('album' in obj_d.keys()) & ('releaseYmd' in obj_d['album'].keys()) else '앨범 발매연도를 알 수 없습니다.'
                except:
                    release = obj_d['album']['releaseYmd']
                genre = obj_d['album']['genreStyle'] if ('album' in obj_d.keys()) & ('genreStyle' in obj_d['album'].keys()) else '장르정보가 없습니다.'
            else:
                lyrics = '가사정보가 없습니다.'
                release = '앨범 발매연도를 알 수 없습니다.'
                genre = '장르정보가 없습니다.'

            tmp = Theme(song=song, album=album, artist=artist, lyrics=lyrics, release=release, genre=genre, type=type)
            tmp.save()

        contents = Theme.objects.filter(type=type)

        return render(request, 'theme.html', {'contents': contents, 'keyword': name})



def fifth(request):

    if not Chart.objects.all():
        url_base = 'https://www.music-flo.com/api/meta/v1/chart/track/'

        for n in range(3550, 3576):
            url = url_base + str(n)
            u = urlopen(url)
            data = u.read()
            j = json.loads(data)

            obj = j['data']['trackList']
            genre = j['data']['name']

            for i in range(len(obj)):
                song = obj[i]['name']
                artist = obj[i]['representationArtist']['name']
                release = obj[i]['album']['releaseYmd']

                tmp = Chart(song=song, artist=artist, release=release, genre=genre)
                tmp.save()

        numbers = list(range(3550, 3576))
        names = ['가', '나', '다', '라', '마', '바', '사', '아', '자', '차', '카', '타', '파', '하', '아', '야', '어', '여', '오', '요',
                 '우', '유', '으', '이', '얘', '예']

        for i in range(26):
            x = Name(number=str(numbers[i]), name=names[i])
            x.save()

    return render(request, 'fifth.html', {'ints': [str(x) for x in range(3550, 3576)], 'names': Name.objects.all()})



def chart(request):
    if request.method == 'POST':
        url = str('https://www.music-flo.com/api/meta/v1/chart/track/' + str(request.POST['number']))
        u = urlopen(url)
        data = u.read()
        j = json.loads(data)

        obj = j['data']['trackList']
        genre = j['data']['name']

        Chart.objects.filter(genre=genre).delete()

        for i in range(len(obj)):
            song = obj[i]['name']
            artist = obj[i]['representationArtist']['name']
            release = obj[i]['album']['releaseYmd']

            tmp = Chart(song=song, artist=artist, release=release, genre=genre)
            tmp.save()

        contents = Chart.objects.filter(genre=genre)

        return render(request, 'chart.html', {'contents': contents, 'keyword': genre})
