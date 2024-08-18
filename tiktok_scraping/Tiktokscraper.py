from crawlbase import CrawlingAPI
import requests
from bs4 import BeautifulSoup
import requests
import json
import os
import yt_dlp


class TiktokScraper:
    def __init__(self , keyword ):
        self.keyword = keyword
        self.base_url = "https://www.tiktok.com/search?q="
        self.search_url = f"{self.base_url}{requests.utils.quote(self.keyword)}"
        self.html_content = ""
        self.data = []

    def get_html_content(self):

        print("Get content for :" , self.search_url )
        crawling_api = CrawlingAPI({"token": "aoVpNf871f7Vrld29LACnA"})

        options = {
            'ajax_wait': 'true',
            'page_wait': 10000,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

        response = crawling_api.get(self.search_url, options)

        self.html_content = response["body"].decode("utf-8")

        soup = BeautifulSoup(self.html_content, 'html.parser')

        self.html_content = soup.prettify()

        with open('tiktok_page_crawling.html', 'w', encoding='utf-8') as file:
            file.write(self.html_content)

        return self.html_content

    def scrape_video_details(self, html_content=None):

        if html_content:
            with open(html_content , 'r', encoding='utf-8') as file:
                html_content = file.read()
        else :
            html_content = self.html_content

        #print(html_content)

        soup = BeautifulSoup(html_content, 'html.parser')
        Videos_cards = soup.find_all('div', class_='css-1soki6-DivItemContainerForSearch e19c29qe10')

        print(Videos_cards)

        if Videos_cards:
            for video_card in Videos_cards:
                video_data = {}

                # Video's ID
                Video_id_card = video_card.find('div', class_="tiktok-web-player no-controls")
                if Video_id_card:
                    Video_id = Video_id_card['id']
                    video_data['Video_id'] = Video_id if Video_id else None

                # Video's URL
                Video_url = video_card.find('a')
                video_data['Video_url'] = Video_url['href'] if Video_url['href'] else None

                # Video's Caption
                Video_caption = video_card.find('span', class_="css-j2a19r-SpanText efbd9f0")
                video_data['Video_caption'] = Video_caption.text.strip() if Video_caption else None

                # Video's Hashtags
                Video_hashtags = video_card.find_all('strong', class_="css-1p6dp51-StrongText ejg0rhn2")
                stripped_videos_hashtags = [hashtag.text.strip() for hashtag in Video_hashtags]
                video_data['Video_Hashtags'] = stripped_videos_hashtags

                # Video's Author
                Video_Author = video_card.find('a', class_="css-22xkqc-StyledLink er1vbsz0")
                video_data['Video_Author'] = Video_Author['href'] if Video_Author else None

                # Video's Views
                Video_views = video_card.find('strong', class_="css-ws4x78-StrongVideoCount etrd4pu10")
                video_data['Video_views'] = Video_views.text.strip() if Video_views else None

                # Upload Time
                Video_upload_time = video_card.find('div', class_="css-dennn6-DivTimeTag e19c29qe15")
                video_data['Video_upload_time'] = Video_upload_time.text.strip() if Video_upload_time else None

                self.data.append(video_data)
            print(self.data)

            with open('videos_data.json', 'w') as f:
                json.dump(self.data, f, indent=4)

    def download_tiktok_videos_with_metadata(self , json_data = None ,  save_path='tiktok_videos'):
        def download_tiktok_video(video_url, video_path):
            # Ensure the directory exists
            if not os.path.exists(video_path):
                os.makedirs(video_path)

            ydl_opts = {
                'outtmpl': os.path.join(video_path, '%(id)s.%(ext)s'),
                'format': 'best',
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=True)
                    filename = ydl.prepare_filename(info)
                    print(f"Video successfully downloaded: {filename}")

            except Exception as e:
                print(f"Error downloading video: {str(e)}")

        if json_data :
            with open(json_data , 'r') as f:
                data = json.load(f)
        else :
            data = self.data

        counter = 1
        for video in data:
            video_folder = os.path.join(save_path , str(counter))
            download_tiktok_video(video['Video_url'], video_folder)

            file_path = os.path.join(video_folder, 'metadata.txt')

            try:
                with open(file_path, 'w') as file:
                    for key, value in video.items():
                        file.write(f"{key}: {value}\n")
                print(f"Metadata saved to: {file_path}")
            except Exception as e:
                print(f"Error saving metadata: {str(e)}")

            counter += 1





