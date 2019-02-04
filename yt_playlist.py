import sys
import requests
from pytube import YouTube
from bs4 import BeautifulSoup

get_url = input("Playlist Url : ")
r = requests.get(get_url)
content = r.content.decode("utf-8")
soup = BeautifulSoup(content, "html.parser")

video_list = soup.find_all("ul", {"id": "browse-items-primary"})[0]
video_list = video_list.find_all("tbody", {"id": "pl-load-more-destination"})[0].find_all("tr", {"class": "pl-video yt-uix-tile "})
video_dict = {}

for ind, video in enumerate(video_list, 0):
    video_dict[ind] = {}
    video_dict[ind]['id'] = video_list[ind]['data-video-id']
    video_dict[ind]['title'] = video_list[ind]['data-title']
url = "https://www.youtube.com/watch?v="

def show_progress_bar(stream, chunk, file_handle, bytes_remaining):
    global total_size, flag, batch_size, print_string
    toolbar_width = 20
    if flag:
        total_size = bytes_remaining
        batch_size = total_size
        flag = False
    if (batch_size - bytes_remaining) > total_size/toolbar_width:
        sys.stdout.flush()
        sys.stdout.write("#")
        batch_size = bytes_remaining
    return

for key, value in video_dict.items():
    try:
        total_size = 0
        flag = True
        batch_size = 0
        yt = YouTube(url + video_dict[key]['id'])
        sys.stdout.write("Downloading :: " + video_dict[key]['title'] + "\n[ ")
        yt.register_on_progress_callback(show_progress_bar)
        yt.streams.first().download()
        sys.stdout.write(" ]\n")
    except ValueError:
        sys.stdout.write("{} : Video not available.\n".format(video_dict[key]['title']))

print("\nCompleted.\n")
