from django.shortcuts import render
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


DEVELOPER_KEY = 'AIzaSyApT_e4T6p4V0FPNBQ0_5C_KL-GJdwtyaI'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def index(request):
    data = []
    if 'q' in request.GET:
        data = search(request.GET['q'])
    return render(request, 'yousearch/searchform.html', { 'videos': data })

def search(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
        q=query,
        type='video',
        part='id,snippet',
        maxResults=10
    ).execute()

    search_videos = []

    for search_result in search_response.get('items', []):
        search_videos.append(search_result['id']['videoId']) 
  
    video_ids = ','.join(search_videos)

    video_response = youtube.videos().list(
        id=video_ids,
        part='snippet,id '
    ).execute()

    videos = []

    for video_result in video_response.get('items', []):
        videos.append('%s' % (video_result['snippet']['title']))

    return videos 
