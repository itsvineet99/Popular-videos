from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

#loading dot envirnments and accessing api key
load_dotenv() 
api_key = os.getenv("api_key")

#building service(youtube) object by using build function
youtube = build("youtube", "v3", developerKey=api_key)

playlist_id = input("Enter the plylist id: ")#enter the playlist id copied from youtube


videos = []
nextPageToken = None #it will get updated on each iteration until there is no respone on nextpage and then loop will break
while True:
    pl_request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=playlist_id,
        maxResults=50,
        pageToken=nextPageToken
    )

    pl_response = pl_request.execute()

    vid_ids = []
    for items in pl_response["items"]:
        vid_ids.append(items["contentDetails"]["videoId"])

    vid_request = youtube.videos().list(
        part="statistics",
        id=",".join(vid_ids)
    )
    vid_response = vid_request.execute()

    
    for item in vid_response["items"]:
        view_count = item["statistics"]["viewCount"]
        vid_id = item["id"]
        vid_link = f"https://youtu.be/{vid_id}"

        videos.append(
            {
                "views" : int(view_count),
                "url" :  vid_link
            }
        )


    nextPageToken = pl_response.get("nextPageToken")
    if not nextPageToken:
        break

#this sorts our videos on the basis of our view count 
videos.sort(key=lambda vid: vid["views"], reverse=True)

#prints the number of videos you want
for video in videos:
    print(video["url"],video["views"])  
print(len(videos))
