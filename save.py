import requests
import os
import sys


first_page_url = 'https://www.anime-planet.com/anime/all'
frontpage = 'anime-planet.html'
directory_p = 'Pages'


def download_url_to_string(url):
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('Could not access page ' + url)
        return ''
    return r.text


def save_string_to_file(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None


def save_page(url, filename):
    text = download_url_to_string(url)
    return save_string_to_file(text, directory_p, filename)


def download_pages(num_of_pages):
    for i in range(1, num_of_pages + 1):
        filename = frontpage[:-5] + '_page_{}'.format(i) + frontpage[-5:]
        url = 'https://www.anime-planet.com/anime/all?page={}'.format(i)
        path = os.path.join(directory_p, filename)
        print('Shranjujem {} ...'.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(path) is True:
            print(' Shranjeno že od prej!')
        else:
            save_page(url, filename)
            print(' Shranjeno!')
    return None
