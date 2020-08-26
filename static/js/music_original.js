(function create_waveform(){

var wavesurfer = WaveSurfer.create({
    // id="waveform" 인 오브젝트에 파형 생성
    // 필수 옵션
    container: '#waveform_original',
    // 선택 옵션들
    //waveColor: 'violet',
    //progressColor: 'purple'
    barWidth: 2,
    progressColor: '#E2B026',
    cursorColor: 'transparent',
    waveColor: '#333533'


});

//wavesurfer.on('ready', function () {
//    wavesurfer.play();
//});

wavesurfer.load($('#audiofile_original').attr('src'));

    $('.controls_original .btn').on('click', function(){
      var action = $(this).data('action');
      console.log(action);
      switch (action) {
        case 'play':
          wavesurfer.playPause();
          break;
        case 'back':
          wavesurfer.skipBackward();
          break;
        case 'forward':
          wavesurfer.skipForward();
          break;
        case 'mute':
          wavesurfer.toggleMute();
          break;
      }
    });
}());