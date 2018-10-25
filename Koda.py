import requests
import re
import csv
import os

spletna_stran = 'https://www.anime-planet.com/anime/all'
direktorij = 'Analiza_podatkov_pages'
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


def cut_into_blocks(page):
    pattern = re.compile(
        r'(<a title="<h5>.*?)<div class="crop">',
        re.DOTALL
    )
    return [x.group(1).strip() for x in re.finditer(pattern, page)]


def get_data(page):
    pattern = re.compile(
        r'''<a title="<h5>(?P<title>.*?)</h5>.*?'''
        r'''<li class='type'>(?P<type>.*?) \((?P<num_eps>.*?)\)</li>'''
        r'''<li>(?P<studio>.*?)</li>.*?'''
        r'''iconYear'>(?P<year>.*?)(?: - .*?)?</li>.*?'ttRating'>'''
        r'''(?P<rating>.*?)</div>.*?'''
        r'''<p>(?P<description>.*?)</p>.*?'''
        r'''Tags</h4><ul>(?P<tags>.*?)</ul>''',
        re.DOTALL
    )
    pattern_2 = re.compile(
        r'Alt title: (?P<alt_title>.*?)</h6>'
    )

    def add_alt_title(page):
        if re.search(pattern_2, page) is None:
            return 'No alternative title'
        else:
            return re.search(pattern_2, page).groupdict()['alt_title']

    def make_list_for(string):
        string = string.replace('<li>', '').replace('</li>', ', ')
        string = string.strip()[:-1]
        string = string.split(', ')
        return string

    dict = {}
    dict['title'] = re.search(pattern, page).groupdict()['title']
    dict['alt_title'] = add_alt_title(page)
    dict['type'] = re.search(pattern, page).groupdict()['type']
    dict['num_of_ep'] = re.search(pattern, page).groupdict()['num_eps']
    dict['studio'] = re.search(pattern, page).groupdict()['studio']
    dict['year'] = int(re.search(pattern, page).groupdict()['year'])
    dict['rating'] = float(re.search(pattern, page).groupdict()['rating'])
    dict['description'] = re.search(pattern, page).groupdict()['description']
    dict['tags'] = re.search(pattern, page).groupdict()['tags']

    # clear data

    if 'TV' in dict['type']:
        dict['type'] = dict['type'] + ' Series'

    dict['num_of_ep'] = dict['num_of_ep'].replace(' eps', '')
    dict['num_of_ep'] = int(dict['num_of_ep'].replace(' ep', ''))
    dict['description'] = dict['description'].replace('&nbsp;', ' ')
    dict['tags'] = make_list_for(dict['tags'])
    return dict


vsebina = read_file_to_string(direktorij, frontpage)
bloki = cut_into_blocks(vsebina)
b0 = get_data(bloki[0])
