let audios = document.querySelectorAll('audio');

const APIController = (function () {
  const clientId = '982b5eff3b2e4aeb91756e5de416f734';
  const clientSecret = '68083fb1d45244ec9bb7c480fd22bdc4';

  const getToken = async () => {
    const result = await fetch('https://accounts.spotify.com/api/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        Authorization: 'Basic ' + btoa(clientId + ':' + clientSecret),
      },
      body: 'grant_type=client_credentials',
    });

    const data = await result.json();
    return data.access_token;
  };

  const getPlaylist = async (token, playlist_id) => {
    const result = await fetch(
      `https://api.spotify.com/v1/playlists/${playlist_id}/tracks`,
      {
        method: 'GET',
        headers: { Authorization: 'Bearer ' + token },
      }
    );

    const data = await result.json();
    console.log(data.items[0])
    return data.items[Math.round(Math.random() * 10)].track.preview_url;
  };

  return {
    getToken() {
      return getToken();
    },
    getPlaylist(token, playlist_id) {
      return getPlaylist(token, playlist_id);
    },
  };
})();

const loadPlaylist = async () => {
  const token = await APIController.getToken();
  const lovePlaylist = await APIController.getPlaylist(
    token,
    '3sCQjOcQ2OM9ubafs3cuOm'
  );
  const motivationalPlaylist = await APIController.getPlaylist(
    token,
    '2zZ6WRxzy9aByUvHRGc3Sw'
  );
  const inspirationalPlaylist = await APIController.getPlaylist(
    token,
    '3li1XfQKJnor5pi1TrEIop'
  );
  const happinessPlaylist = await APIController.getPlaylist(
    token,
    '4gWQkYXJODwOgk9ay6uuWF'
  );

  audios.forEach((audio) => {
    if (audio.className === 'happiness') {
      audio.src = happinessPlaylist;
    }
    if (audio.className === 'motivational') {
      audio.src = motivationalPlaylist;
    }
    if (audio.className === 'love') {
      audio.src = lovePlaylist;
    }
    if (audio.className === 'inspirational') {
      audio.src = inspirationalPlaylist;
    }
  });
};

loadPlaylist();

let audioPlayers = document.querySelectorAll(".audio-player");

if (audioPlayers.length) {
    audioPlayers.forEach(function(audioPlayer, i) {
      let audio = audioPlayer.querySelector("audio");
      let playerButton = audioPlayer.querySelector(".player-button");
      playerButton.addEventListener("click", function(e) {
        let current = e.currentTarget;
        let audio = current.closest(".audio-player").querySelector("audio");
        let btnSvg = current.querySelector(".useBtn");
        if (!audio.paused) {
          btnSvg.setAttribute("href", "#icon-play");
          audio.pause();
        } else {
          btnSvg.setAttribute("href", "#icon-pause");
          audio.play();
        }
      });
  
      let timeline = audioPlayer.querySelector('.timeline');
      timeline.addEventListener('change', function(e) {
        let time = (timeline.value * audio.duration) / 100;
        audio.currentTime = time;
      });
  
      audio.addEventListener('ended', function(e) {
        console.log('audio finished');
        timeline.value = 0;
      });
  
      audio.addEventListener('timeupdate', function(e) {
        let percentagePosition = (100 * audio.currentTime) / audio.duration;
        timeline.value = percentagePosition;
      });
    });
  }