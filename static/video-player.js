/**
 * Created by jun-young on 14. 7. 12.
 */

var tag = document.createElement('script');
tag.src = "http://www.youtube.com/player_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function onYouTubePlayerAPIReady() {
    ytplayer = new YT.Player('player', {
        height: '390',
        width: '640',
        videoId: '9bZkp7q19f0',
        playerVars: { 'autoplay': 1, 'controls': 0 },
	events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
}

function updateHTML(elmId, value) {
    document.getElementById(elmId).innerHTML = value;
}

function updatePlayerInfo() {
    if (ytplayer && ytplayer.getDuration) {
        updateHTML("videoDuration", ytplayer.getDuration());
        updateHTML("videoCurrentTime", ytplayer.getCurrentTime());

        var videoDuration = ytplayer.getDuration();
        var videoCurrent = ytplayer.getCurrentTime();
    }
}

function playVideo() {
	ytplayer.playVideo();
}

function pauseVideo() {
	ytplayer.pauseVideo();
}

function loadVideoById(id) {
	ytplayer.loadVideoById(id);
}

function onPlayerReady(event) {
	setInterval(updatePlayerInfo, 250);
}

function onPlayerStateChange(event) {

}