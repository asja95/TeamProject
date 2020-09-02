from django.shortcuts import render, redirect
import librosa
from django.core.files.storage import FileSystemStorage
from scipy.io.wavfile import write
import os
from team import settings

# Create your views here.


def upload(request):
    if request.method == 'POST':
        myfile = request.FILES['audio']
        fs = FileSystemStorage()
        if fs.exists(myfile.name):
            os.remove(os.path.join(settings.MEDIA_ROOT, myfile.name))
        filename = fs.save(myfile.name, myfile)
        filename_only = filename.split('.')[-2]

        x, sr = librosa.load('media/' + filename, duration=60)

        onset_env = librosa.onset.onset_strength(y=x, sr=sr)
        tempo, beat_times = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr, start_bpm=120, units='time')
        total_time = len(x) / sr

        original_music = 'media/' + filename


        beat_times_file = 'static/outputs/beats/' + filename_only + '_beat.txt'
        with open(beat_times_file, 'w') as f:
            for item in beat_times:
                f.write("%s\n" % round(item, 2))
            f.close()

        return render(request, 'list.html', {'filename': filename_only, 'tempo': int(tempo), 'time': int(total_time),
                                             'beat_times': '/' + beat_times_file, 'soundfile': '/' + original_music})

    return redirect('home1')

