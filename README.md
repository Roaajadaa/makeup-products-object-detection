# Makeup Products Object Detection project

**Overview**

This project aims to develop an object detection model capable of identifying specific makeup and beauty products from TikTok videos. 
The process includes scraping makeup-related videos, refining the dataset, annotating the products, and training the model using YOLOv8 Model .


**Workflow**

1. Scrape TikTok Videos
The project begins by scraping videos specifically related to makeup from TikTok. This is achieved by creating a custom package that serves as a service to fetch HTML content, parse it, and extract relevant metadata. The key functions include:

- get_html_content: Retrieves the HTML content of TikTok pages to allow for parsing and data extraction.

- scrape_video_details: Gathers metadata for each video, including title, creator, and views.

- download_tiktok_videos_with_metadata: Downloads the videos along with the extracted metadata for further processing.

File: feature/scraping-videos/tiktok_scraping/Tiktokscraper.py

2. Label Videos
Using the Label Studio tool, the selected videos are labeled to identify makeup products. During this process, labeled frames are saved as JSON files for each video. This is necessary because Label Studio does not support direct frame export. Each JSON file contains the annotations for the corresponding frames.

3. Extract Frames
Since Label Studio does not support direct export of frames, the labeled videos are first exported in JSON format. OpenCV is then used to extract frames from these videos, saving each frame along with its corresponding bounding box coordinates. This allows for a structured dataset that includes both the visual data and the necessary annotations for training.

File: prepare_data.ipynb

4. Convert to YOLO Format
The labeled data is converted into the YOLO format, which is essential for training the YOLOv8 model. This process involves creating two separate folders: one for images and another for labels. Each image in the images folder is accompanied by a corresponding text file in the labels folder, sharing the same filename. Additionally, the bounding box coordinates are normalized to ensure compatibility with the YOLO training requirements.

File : utils.py

5. Train YOLOv8 Model
The final step involves training the YOLOv8 model using the prepared dataset. Both pre-trained and custom-trained models are utilized to enhance performance and accuracy.

File: Yolov8.pt.ipynb

6. Load the Final Model
The final model, trained on the dataset, is saved as best.pt.

**Requirements**
Python 3.12.6
Required libraries: OpenCV , label-studio , pandas, numpy, ultralytics , beautifulsoup4 , crawlbase. 




