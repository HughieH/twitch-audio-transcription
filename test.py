import streamlink

stream = streamlink.streams("https://www.twitch.tv/nick_shox")
url = stream['audio_only'].url
print(url)