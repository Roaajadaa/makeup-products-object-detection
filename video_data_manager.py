from mongoengine import Document, StringField, ListField, connect

# Connect to MongoDB
connect(
    db='tiktok_videos',
    host='mongodb://localhost:27017/'
)

class Video(Document):
    Video_url = StringField(required=True)
    Video_caption = StringField()
    Video_Hashtags = ListField(StringField())
    Video_Author = StringField()
    Video_views = StringField()
    Video_upload_time = StringField()

    meta = {
        'collection': 'video'  # Specify the collection name
    }


def create_and_save_video(video_url, video_caption, video_hashtags, video_author, video_views, video_upload_time):
    new_video = Video(
        Video_url=video_url,
        Video_caption=video_caption,
        Video_Hashtags=video_hashtags,
        Video_Author=video_author,
        Video_views=video_views,
        Video_upload_time=video_upload_time
    )
    new_video.save()
    print("Document saved successfully!")


"""
# example
create_and_save_video(
    video_url="https://www.tiktok.com/@newuser/video/1234567890",
    video_caption="Check out this amazing video!",
    video_hashtags=["#amazing", "#newvideo"],
    video_author="/@newuser",
    video_views="1K",
    video_upload_time="2024-08-16"
)
"""


def update_video_details(video_url, new_caption=None, new_hashtags=None, new_author=None, new_views=None, new_upload_time=None):
    video = Video.objects(Video_url=video_url).first()

    if video:
        if new_caption is not None:
            video.Video_caption = new_caption
        if new_hashtags is not None:
            video.Video_Hashtags = new_hashtags
        if new_author is not None:
            video.Video_Author = new_author
        if new_views is not None:
            video.Video_views = new_views
        if new_upload_time is not None:
            video.Video_upload_time = new_upload_time

        video.save()

        print("Document updated successfully!")
    else:
        print("No document found with the given video URL.")


"""
#example
update_video_details(
    video_url="https://www.tiktok.com/@glambymehak/video/6938905013653605637",
    new_caption="Updated caption for the video!",
)

"""


def read_document_by_url(video_url):
    video = Video.objects(Video_url=video_url).first()
    if video:
        print(video.to_mongo().to_dict())
    else:
        print("No document found with the given video URL.")



"""
#example
read_document_by_url('https://www.tiktok.com/@glambymehak/video/6938905013653605637')
"""


def delete_document_by_url(video_url):
    video = Video.objects(Video_url=video_url).first()
    if video:
        video.delete()
        print(f"Document with video URL '{video_url}' has been deleted.")
    else:
        print(f"No document found with the given video URL '{video_url}'.")

"""
#example
delete_document_by_url(video_url="https://www.tiktok.com/@newuser/video/1234567890")
"""