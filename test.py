from tiktok_scraping import TiktokScraper


scraper = TiktokScraper("huda beauty makeup")
# scraper.get_html_content()
scraper.scrape_video_details('tiktok_page_crawling.html')
scraper.download_tiktok_videos_with_metadata('videos_data.json')


# OR you can  get the html ,  scrap video details , and save the videos like that :

"""
scraper = TiktokScraper("huda beauty makeup")
scraper.get_html_content()
scraper.scrape_video_details()
scraper.download_tiktok_videos_with_metadata()
"""