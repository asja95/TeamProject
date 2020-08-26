from django.shortcuts import render, redirect
from search.models import Keywords, Theme, Chart, Name
import json
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from urllib.request import urlopen
import datetime
import time as mod_time
from urllib import parse
from django.core.paginator import Paginator
import re
import requests


# Create your views here.


def search(request):
    # 키워드 검색일 때.
    if request.method == 'POST' and request.POST['item'] == 'keyword':

        # 처음에 post방식으로 호출할 때.
        if request.method == 'POST':
            Keywords.objects.all().delete()

            parts = urlparse(
                'https://www.music-flo.com/api/search/v2/search?searchType=TRACK&sortType=ACCURACY&size=100&page=1')
            qs = dict(parse_qsl(parts.query))
            qs['keyword'] = request.POST['name']
            today = datetime.datetime.now()
            today_time = int((mod_time.mktime(today.timetuple())))
            today_unixtime = (today_time * 1000)
            qs['timestamp'] = today_unixtime
            parts = parts._replace(query=urlencode(qs))
            new_url = urlunparse(parts)

            u = urlopen(new_url)

            data = u.read()
            j = json.loads(data)

            if ('data' in j.keys()) and ('list' in j['data'].keys()) and (len(j['data']['list']) > 0) and (
                    'list' in j['data']['list'][0].keys()):

                obj = j['data']['list'][0]['list']

                for i in range(min(len(obj), 100)):
                    song = obj[i]['name'] if 'name' in obj[i].keys() else '노래 제목을 알 수 없습니다.'
                    album = obj[i]['album']['title'] if ('album' in obj[i].keys()) and (
                            'title' in obj[i]['album'].keys()) else '앨범명을 알 수 없습니다.'
                    artist = obj[i]['representationArtist']['name'] if ('representationArtist' in obj[i].keys()) and (
                            'name' in obj[i]['representationArtist'].keys()) else '아티스트를 알 수 없습니다.'
                    id = obj[i]['id'] if 'id' in obj[i].keys() else ''
                    try:
                        image = obj[i]['album']['imgList'][0]['url']
                    except:
                        image = '/static/img/noimg.jpg'

                    if id:
                        urls = str(
                            'https://www.music-flo.com/api/meta/v1/track/' + str(id))
                        parts_d = urlparse(urls)
                        qs_d = dict(parse_qsl(parts_d.query))
                        qs_d['timestamp'] = today_unixtime
                        parts_d = parts_d._replace(query=urlencode(qs_d))
                        new_url_d = urlunparse(parts_d)

                        u_d = urlopen(new_url_d)
                        data_d = u_d.read()
                        j_d = json.loads(data_d)

                        print(j_d)

                        if 'data' in j_d.keys():
                            obj_d = j_d['data']

                            lyrics = obj_d['lyrics'] if 'lyrics' in obj_d.keys() else '가사정보가 없습니다.'
                            try:
                                release = datetime.datetime.strptime(obj_d['album']['releaseYmd'], '%Y%m%d').strftime(
                                    '%Y.%m.%d') if ('album' in obj_d.keys()) and (
                                        'releaseYmd' in obj_d['album'].keys()) else '앨범 발매연도를 알 수 없습니다.'
                            except:
                                release = obj_d['album']['releaseYmd']
                            genre = obj_d['album']['genreStyle'] if ('album' in obj_d.keys()) and (
                                    'genreStyle' in obj_d['album'].keys()) else '장르정보가 없습니다.'

                        else:
                            lyrics = '가사정보가 없습니다.'
                            release = '앨범 발매연도를 알 수 없습니다.'
                            genre = '장르정보가 없습니다.'

                    else:
                        lyrics = '가사정보가 없습니다.'
                        release = '앨범 발매연도를 알 수 없습니다.'
                        genre = '장르정보가 없습니다.'

                    tmp = Keywords(song=song, album=album, artist=artist, lyrics=lyrics, release=release, genre=genre,
                                   image=image)
                    tmp.save()

            else:
                song = album = artist = ''
                image = '/static/img/noimg.jpg'
                lyrics, release, genre = '가사정보가 없습니다.', '앨범 발매연도를 알 수 없습니다.', '장르정보가 없습니다.'
                tmp = Keywords(song=song, album=album, artist=artist, lyrics=lyrics, release=release, genre=genre,
                               image=image)
                tmp.save()

            contents = Keywords.objects.all()

            page = request.GET.get('page', '1')
            paginator = Paginator(contents, 10)
            page_obj = paginator.get_page(page)

            return render(request, 'keyword.html',
                          {'contents': contents, 'keyword': request.POST['name'], 'song': page_obj})

        # 페이징을 위해 GET방식으로 호출할 때.
        else:
            return redirect('home2')

    # OST 검색일 때.
    if request.method == 'POST' and request.POST['item'] in ('movie', 'drama', 'musical'):

        if request.method == 'POST':

            if request.POST['item'] == 'movie':
                name = request.POST['name']
                type = 'movie'

            elif request.POST['item'] == 'drama':
                name = request.POST['name']
                type = 'drama'

            elif request.POST['item'] == 'musical':
                name = request.POST['name']
                type = 'musical'

            Theme.objects.filter(type=type).delete()

            # 1. 앨범 목록에서 검색.
            parts = urlparse(
                'https://www.music-flo.com/api/search/v2/search?searchType=ALBUM&sortType=ACCURACY')
            qs = dict(parse_qsl(parts.query))
            qs['keyword'] = name + 'ost'
            today = datetime.datetime.now()
            today_time = int((mod_time.mktime(today.timetuple())))
            today_unixtime = (today_time * 1000)
            qs['timestamp'] = today_unixtime
            parts = parts._replace(query=urlencode(qs))
            new_url = urlunparse(parts)

            u = urlopen(new_url)

            data = u.read()
            j = json.loads(data)

            if ('data' in j.keys()) and ('list' in j['data'].keys()) and (len(j['data']['list']) > 0) and (
                    'list' in j['data']['list'][0].keys()):

                obj = j['data']['list'][0]['list']
                album_id = ''

                # 전체 OST를 가지고 있는 앨범 탐색.
                if len(obj) == 1:
                    album_id = obj[0]['id']

                else:
                    for i in range(len(obj)):
                        if obj[i]['representationArtist']['name'] == 'Various Artists':
                            album_id = obj[i]['id']
                            break

                # 2. 해당하는 앨범의 id로 곡 list 검색.
                if album_id:

                    urls = str(
                        'https://www.music-flo.com/api/meta/v1/album/' + str(album_id) + '/track')
                    parts_d = urlparse(urls)
                    qs_d = dict(parse_qsl(parts_d.query))
                    qs_d['timestamp'] = today_unixtime
                    parts_d = parts_d._replace(query=urlencode(qs_d))
                    new_url_d = urlunparse(parts_d)

                    u_d = urlopen(new_url_d)
                    data_d = u_d.read()
                    j_d = json.loads(data_d)

                    if ('data' in j_d.keys()) and ('list' in j_d['data'].keys()):
                        obj = j_d['data']['list']

                        # 노래 하나마다 탐색.
                        for i in range(len(obj)):
                            song = obj[i]['name'] if 'name' in obj[i].keys() else '노래 제목을 알 수 없습니다.'
                            album = obj[i]['album']['title'] if ('album' in obj[i].keys()) & (
                                    'title' in obj[i]['album'].keys()) else '앨범명을 알 수 없습니다.'
                            artist = obj[i]['representationArtist']['name'] if ('representationArtist' in obj[i].keys()) & (
                                    'name' in obj[i]['representationArtist'].keys()) else '아티스트를 알 수 없습니다.'
                            id = obj[i]['id'] if 'id' in obj[i].keys() else ''

                            # 해당 노래의 상세정보 탐색.
                            urls = str('https://www.music-flo.com/api/meta/v1/track/' + str(id))
                            parts_d = urlparse(urls)
                            qs_d = dict(parse_qsl(parts_d.query))
                            qs_d['timestamp'] = today_unixtime
                            parts_d = parts_d._replace(query=urlencode(qs_d))
                            new_url_d = urlunparse(parts_d)

                            u_d = urlopen(new_url_d)
                            data_d = u_d.read()
                            j_d = json.loads(data_d)

                            if 'data' in j_d.keys():
                                obj_d = j_d['data']

                                lyrics = obj_d['lyrics'] if 'lyrics' in obj_d.keys() else '가사정보가 없습니다.'
                                try:
                                    release = datetime.datetime.strptime(obj_d['album']['releaseYmd'],
                                                                         '%Y%m%d').strftime(
                                        '%Y.%m.%d') if ('album' in obj_d.keys()) and (
                                            'releaseYmd' in obj_d['album'].keys()) else '앨범 발매연도를 알 수 없습니다.'
                                except:
                                    release = obj_d['album']['releaseYmd']
                                genre = obj_d['album']['genreStyle'] if ('album' in obj_d.keys()) and (
                                        'genreStyle' in obj_d['album'].keys()) else '장르정보가 없습니다.'
                            else:
                                lyrics = '가사정보가 없습니다.'
                                release = '앨범 발매연도를 알 수 없습니다.'
                                genre = '장르정보가 없습니다.'

                            tmp = Theme(song=song, album=album, artist=artist, lyrics=lyrics, release=release,
                                        genre=genre,
                                        type=type)
                            tmp.save()

                    else:
                        song = album = artist = ''
                        lyrics, release, genre = '가사정보가 없습니다.', '앨범 발매연도를 알 수 없습니다.', '장르정보가 없습니다.'
                        tmp = Theme(song=song, album=album, artist=artist, lyrics=lyrics, release=release, genre=genre)
                        tmp.save()

                # 조건을 만족하는 앨범이 없을 때.
                else:
                    song = album = artist = ''
                    lyrics, release, genre = '가사정보가 없습니다.', '앨범 발매연도를 알 수 없습니다.', '장르정보가 없습니다.'
                    tmp = Theme(song=song, album=album, artist=artist, lyrics=lyrics, release=release, genre=genre)
                    tmp.save()

            # 앨범 목록이 존재하지 않을 때.
            else:
                song = album = artist = ''
                lyrics, release, genre = '가사정보가 없습니다.', '앨범 발매연도를 알 수 없습니다.', '장르정보가 없습니다.'
                tmp = Theme(song=song, album=album, artist=artist, lyrics=lyrics, release=release, genre=genre)
                tmp.save()

            contents = Theme.objects.filter(type=type)

            return render(request, 'theme.html', {'contents': contents, 'keyword': name})


        # 페이징을 위해 GET방식으로 호출했을 때.
        else:
            return redirect('home2')

    # GET방식으로 잘못 불러올 때.
    else:
        return redirect('home2')


'''
일단 페이징 부분은 보류. GET방식으로 호출하기 때문에 따로 고려해야 할 거 같음.
'''


def video(request):
    url = 'https://www.youtube.com/results?search_query=' + parse.quote(request.POST['video'])
    html = requests.get(url).text
    for w in re.findall('"url":"/watch\?v=(.*?)"', str(html)):
        if '=' not in w:
            link = w
            break
    url = 'https://www.youtube.com/embed/' + link

    return render(request, 'video.html', {'url': url})


'''
처음 보여지는 페이지에서는 차트의 종류만 크롤링해서 목록만 보여줄 수 있게 했음.
검색 버튼을 누르면 해당하는 차트의 데이터를 크롤링할 것.
'''


def fifth(request):
    # 차트 이름들이 이미 존재하면 크롤링을 반복하지 않고 존재하는 table을 사용할 것.
    if not Name.objects.all():
        url_base = 'https://www.music-flo.com/api/meta/v1/chart/track/'

        names = []
        for n in range(3550, 3576):
            url = url_base + str(n)
            u = urlopen(url)
            data = u.read()
            j = json.loads(data)

            genre = j['data']['name']
            names.append(genre)

        numbers = list(range(3550, 3576))

        for i in range(26):
            x = Name(number=str(numbers[i]), name=names[i])
            x.save()

    return render(request, 'fifth.html', {'names': Name.objects.all()})


# 각 검색 버튼을 눌렀을 때 수행할 것.
def chart(request):
    if request.method == 'POST':
        genre = Name.objects.get(number=str(request.POST['number'])).name

        # 이미 해당 차트의 데이터가 존재하면 크롤링을 반복하지 않을 것.
        if not Chart.objects.filter(genre=genre):
            url = str('https://www.music-flo.com/api/meta/v1/chart/track/' + str(request.POST['number']))
            u = urlopen(url)
            data = u.read()
            j = json.loads(data)

            genre = Name.objects.get(number=str(request.POST['number'])).name

            obj = j['data']['trackList']

            for i in range(len(obj)):
                song = obj[i]['name'] if 'name' in obj[i].keys() else '노래 제목을 알 수 없습니다.'
                artist = obj[i]['representationArtist']['name'] if ('representationArtist' in obj[i].keys()) and (
                        'name' in obj[i]['representationArtist'].keys()) else '아티스트를 알 수 없습니다.'
                try:
                    release = datetime.datetime.strptime(obj[i]['album']['releaseYmd'], '%Y%m%d').strftime(
                        '%Y.%m.%d') if ('album' in obj[i].keys()) and (
                            'releaseYmd' in obj[i]['album'].keys()) else '앨범 발매연도를 알 수 없습니다.'
                except:
                    release = obj[i]['album']['releaseYmd']

                tmp = Chart(song=song, artist=artist, release=release, genre=genre)
                tmp.save()

        contents = Chart.objects.filter(genre=genre)

        return render(request, 'chart.html', {'contents': contents, 'keyword': genre})
