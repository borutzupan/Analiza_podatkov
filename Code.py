import requests
import re
import csv
import os

spletna_stran = 'http://mangakakalot.com/manga_list?type=topview&category=all&state=all&page=1'
direktorij = 'Analiza_podatkov'
csv_file = 'Analiza_csv'
frontpage = 'frontpage.html'


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


def save_frontpage(url):
    text = download_url_to_string(url)
    return save_string_to_file(text, direktorij, frontpage)

with open('frontpage.html', encoding="utf-8") as fp:
    vsebina = fp.read()


def find_names(page):
    regex = re.compile(r'<a.*? href="https?://.*?\.com/manga/(.*?)" title="(.*?)">\2</a>', flags=re.DOTALL)
    return [x.group(2) for x in re.finditer(regex, page)][20:]


print(find_names(vsebina))
regex = re.compile(r'<a.*? href="(https?://.*?\.com/manga/.*?)" title="(.*?)">\2</a>', flags=re.DOTALL)
seznam = [x.group(1) for x in re.finditer(regex, vsebina)]
