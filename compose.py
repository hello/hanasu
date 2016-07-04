from pydub import AudioSegment

import subprocess

def play_audio(audio_file_path):
    subprocess.call(["ffplay", "-nodisp", "-autoexit", audio_file_path])

playlist_songs = [
    #AudioSegment.from_wav('audio/sleep_sounds/sleep_sounds_19.150-21.550.wav'),
    #AudioSegment.from_wav('audio/sleep_sounds/sleep_sounds_85.150-86.400.wav'),

    AudioSegment.from_wav('audio/alarms/alarms_418.300-419.950.wav'),
    AudioSegment.from_wav('audio/alarms/alarms_1240.250-1241.350.wav') - 3
]

playlist = playlist_songs.pop(0)

for song in playlist_songs:
    playlist = playlist.append(song, crossfade=50)

playlist_length = len(playlist_songs) / (1000*60)


exported = 'audio/alarms/response.wav'
out_f = open(exported, 'wb')
playlist.export(out_f, format='wav')
play_audio(exported)
