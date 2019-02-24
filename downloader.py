#!/usr/bin/python3
import os
import sys
import requests
import optparse
from pytube import YouTube
from bs4 import BeautifulSoup
from requests.exceptions import MissingSchema


def show_progress_bar(stream, chunk, file_handle, bytes_remaining):
    global total_size, flag, batch_size, print_string
    toolbar_width = 20
    #percentage = batch_size/total_size
    if flag:
        total_size = bytes_remaining
        batch_size = total_size
        flag = False
    if (batch_size - bytes_remaining) > (total_size/toolbar_width):
        sys.stdout.flush()
        sys.stdout.write("▋")
        batch_size = bytes_remaining
    return


def downloadAll(get_url, type):

    video_dict = {}

    r = requests.get(get_url)
    content = r.content.decode("utf-8")
    soup = BeautifulSoup(content, "xml")

    if type == "Playlist":

        video_list = soup.find_all("ul", {"id": "browse-items-primary"})[0]
        video_list = video_list.find_all("tbody", {"id": "pl-load-more-destination"})[0].find_all(
            "tr", {"class": "pl-video yt-uix-tile "})
        for ind, video in enumerate(video_list, 0):
            video_dict[ind] = {}
            video_dict[ind]['id'] = video_list[ind]['data-video-id']
            video_dict[ind]['title'] = video_list[ind]['data-title']

    elif type == "Mix":

        video_list = soup.find_all("ol", {"class": "playlist-videos-list"})[0]
        video_list = video_list.find_all("li", {"class": "vve-check"})
        for ind, video in enumerate(video_list, 0):
            video_dict[ind] = {}
            video_dict[ind]['id'] = video_list[ind]['data-video-id']
            video_dict[ind]['title'] = video_list[ind]['data-video-title']

    for key, value in video_dict.items():
        try:
            downloadVideo(id=video_dict[key]['id'], title=video_dict[key]['title'])
        except:
            sys.stdout.write("{} : Video not available.\n".format(video_dict[key]['title']))


def downloadVideo(id=None, title=None, url=None):
    global base_url, total_size, flag, batch_size

    total_size = 0
    flag = True
    batch_size = 0

    if id and title:
        yt = YouTube(base_url + id)
        sys.stdout.write("Downloading :: " + title + "\n[ ")
        yt.register_on_progress_callback(show_progress_bar)
        yt.streams.first().download()
        sys.stdout.write(" ]\n")
    elif url:
        r = requests.get(url)
        soup = BeautifulSoup(r.content.decode("utf-8"), 'lxml')
        title = soup.find_all("h1", {"class": "watch-title-container"})[0].find("span", {"class": "watch-title"})['title']
        yt = YouTube(url)
        sys.stdout.write("Downloading :: " + title + "\n[ ")
        yt.register_on_progress_callback(show_progress_bar)
        yt.streams.first().download()
        sys.stdout.write(" ]\n")


def download(get_url):

    if "watch" in get_url and "index" in get_url and "list" in get_url:
        choice = input("Entire Playlist [1] or Current Video [2] : ")
        if choice == "1":
            downloadAll(get_url, type="Mix")
        elif choice == "2":
            get_url = get_url.split("&index")[0]
            downloadVideo(url=get_url)
    elif "watch" in get_url and ("list" in get_url or "start_radio" in get_url):
        choice = input("Entire Playlist [1] or Current Video [2] : ")
        if choice == "1":
            downloadAll(get_url, type="Mix")
        elif choice == "2":
            get_url = get_url.split("&list")[0]
            downloadVideo(url=get_url)
    elif "playlist" in get_url:
        downloadAll(get_url, type="Playlist")
    else:
        try:
            downloadVideo(url=get_url)
        except MissingSchema:
            print("Invalid URL. Please Recheck.")
            return


if __name__ == "__main__":
    print(os.getcwd())
    path_of_downloaded_video = os.getenv("HOME")+"/Downloads/Youtube"
    if not os.path.exists(path_of_downloaded_video):
        os.makedirs(path_of_downloaded_video)
    os.chdir(path_of_downloaded_video)
    print(os.getcwd())

    base_url = "https://www.youtube.com/watch?v="

    if len(sys.argv)==1:
        get_url = input("Url : ")
    elif len(sys.argv)>2:
        print("Too Many Arguments!!")
        get_url = input("Enter Url : ")
    else:
        get_url = sys.argv[1]

    download(get_url)
    
    print("Downloaded Successfully.")
