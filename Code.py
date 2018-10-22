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


def save_page(url, filename):
    text = download_url_to_string(url)
    return save_string_to_file(text, direktorij, filename)


def read_file_to_string(directory, filename):
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        return file_in.read()


def find_names(page, num_of_names_from_right):
    regex = re.compile(
        r'<a.*? href="https?://.*?\.com/manga/.*?" title="(.*?)">\1</a>'
    )
    return [x.group(1) for x in re.finditer(regex, page)][-num_of_names_from_right:]


def find_links(page, num_of_links_from_right):
    regex = re.compile(
        r'<a.*? href="(https?://.*?\.com/manga/.*?)" title="(.*?)">\2</a>'
    )
    return [x.group(1) for x in re.finditer(regex, page)][-num_of_links_from_right:]


def make_dictionary(list_1, list_2):
    dict = {}
    for i in range(len(list_1)):
        dict[list_1[i]] = list_2[i]
    return dict


def save_following_pages(dictionary):
    for link in dictionary:
        save_page(dictionary[link], link + '.html')
    return None


def get_data(page):
    re_author = re.compile(r"<a rel='nofollow' href=.*?>(?P<author>.*?)</a>, (?:.*?)?</li>")
    re_status = re.compile(r'<li>Status : (?P<status>.*?)</li>')
    re_view = re.compile(r'<li>View : (?P<st_ogleda>.*?)</li>')
    re_ocena = re.compile(r'<em property="v:average">(?P<ocena>.*?)</em>/')
        #r"<li>Genres :"
        #r"<a rel='nofollow' href=.*?>(.*?)</a>, <a rel='nofollow' href='http://mangakakalot.com/manga_list?type=newest&category=4&state=all&page=1'>Adventure</a>, <a rel='nofollow' href='http://mangakakalot.com/manga_list?type=newest&category=6&state=all&page=1'>Comedy</a>, <a rel='nofollow' href='http://mangakakalot.com/manga_list?type=newest&category=10&state=all&page=1'>Drama</a>, <a rel='nofollow' href='http://mangakakalot.com/manga_list?type=newest&category=12&state=all&page=1'>Fantasy</a>, <a rel='nofollow' href='http://mangakakalot.com/manga_list?type=newest&category=14&state=all&page=1'>Harem</a>, <a rel='nofollow' href='http://mangakakalot.com/manga_list?type=newest&category=44&state=all&page=1'>Manhua</a>, <a rel='nofollow' href='http://mangakakalot.com/manga_list?type=newest&category=27&state=all&page=1'>Romance</a>, <a rel='nofollow' href='http://mangakakalot.com/manga_list\?type=newest&category=33&state=all&page=1'>Shounen</a>,
    dictionary = {'author': re.search(re_author, page).groupdict()['author'],
                  'status': re.search(re_status, page).groupdict()['status'],
                  'view': int((re.search(re_view, page).groupdict()['st_ogleda']).replace(',', '')),
                  'rating': float(re.search(re_ocena, page).groupdict()['ocena'])}
    return dictionary


def save_data(dictionary):
    dict = {}
    for i in range(len(dictionary)):
        name = list(dictionary.keys())[i]
        page_name = name + '.html'
        dict[name] = get_data(read_file_to_string(direktorij, page_name))
    return dict


save_page(spletna_stran, frontpage)
vsebina = read_file_to_string(direktorij, frontpage)
imena = find_names(vsebina, 24)
linki = find_links(vsebina, 24)
link_slovar = make_dictionary(imena, linki)
save_following_pages(link_slovar)
data = save_data(link_slovar)
