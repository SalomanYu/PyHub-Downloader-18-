import youtube_dl
import json
import sys


def get_info(url):
    options = {
        'simulate': True, # параметр, говорящий о том, что нам нужна только информация о видео. Скачивать не нужно
        'quiet': True
    }

    ydl = youtube_dl.YoutubeDL(options)

    try:
        video = ydl.extract_info(url) # Забираем словарь с информацией о видео
        # video_data_json = json.dumps(video) #

        formats = video.get('formats', None)
        valid_formats = {}
        count = 1

        for format in formats:
            if format['protocol'] == 'https':
                valid_formats[count] = format['format_id']
                count += 1
    
        video_data = {
            'title' : video.get('title', None),
            'thumbnail' : video.get('thumbnail', None), # картинка
            'formats': valid_formats   
        }
        return video_data

    except Exception as error:
        print('CHECK YOUR URL VIDEO')


def download_video(url, format):
    options = {
        'format' : format,
    }
    try:
        
        ydl = youtube_dl.YoutubeDL(options)
        ydl.extract_info(url=url)
    except Exception as error:
        print('Something wrong!')
    return 'Video Downloaded!'

def main():
    url = input('Enter the URL video: ').strip()
    video = get_info(url=url)
    title = video['title']
    avaible_formats = video['formats']
    image = video['thumbnail']

    print(f'[INFO:]\n\nVideo Title: {title}\nVideo Formats:')
    for key, value in avaible_formats.items():
        print(f'{key}. {value}')

    quality_video = int(input(f'Select video quality (Example: 2): '))

    if quality_video not in avaible_formats:
        print('This format not found!')
        sys.exit()

    print(download_video(url, avaible_formats[quality_video]))

if __name__ == '__main__':
    main()
