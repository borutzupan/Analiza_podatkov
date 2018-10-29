import requests
import re
import csv
import os
import html

spletna_stran = 'https://www.anime-planet.com/anime/all'
direktorij = 'Analiza_podatkov_pages'
direktorij_csv = 'Analiza_podatkov_csv'
csv_file = 'anime-planet.csv'
frontpage = 'anime-planet.html'


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
        r'''.*?iconYear'>(?P<year>.*?)(?: - .*?)?</li>.*?'tt'''
        r'''Rating'>(?P<rating>.*?)</div>.*?'''
        r'''<p>(?P<description>.*?)</p>''',
        re.DOTALL
    )
    pattern_2 = re.compile(
        r'''<li>(?P<studio>.*?)</li><li class='iconYear'>'''
    )
    pattern_3 = re.compile(
        r'Alt title: (?P<alt_title>.*?)</h6>'
    )
    patter_4 = re.compile(
        r'Tags</h4><ul>(?P<tags>.*?)</ul>'
    )

    def add_exceptions(pattern, page, string, groupdict_name):
        if re.search(pattern, page) is None:
            return 'No {} found'.format(string)
        else:
            return re.search(pattern, page).groupdict()[groupdict_name]

    def make_list_for(string):
        string = string.replace('<li>', '').replace('</li>', ', ')
        string = string.strip()[:-1]
        string = string.split(', ')
        return string

    def make_intiger_for(string):
        string = string.replace(' eps', '')
        string = string.replace(' ep', '')
        string = string.replace('+', '')
        return int(string)

    dict = {}
    dict['title'] = re.search(pattern, page).groupdict()['title']
    dict['alt_title'] = add_exceptions(pattern_3, page, 'alternative title', 'alt_title')
    dict['type'] = re.search(pattern, page).groupdict()['type']
    dict['num_of_ep'] = re.search(pattern, page).groupdict()['num_eps']
    dict['studio'] = add_exceptions(pattern_2, page, 'studio', 'studio')
    dict['year'] = int(re.search(pattern, page).groupdict()['year'])
    dict['rating'] = float(re.search(pattern, page).groupdict()['rating'])
    dict['description'] = re.search(pattern, page).groupdict()['description']
    dict['tags'] = add_exceptions(patter_4, page, 'tags', 'tags')

    # clear data

    if 'TV' in dict['type']:
        dict['type'] = dict['type'] + ' Series'

    dict['num_of_ep'] = make_intiger_for(dict['num_of_ep'])
    dict['description'] = html.unescape(dict['description'])
    dict['tags'] = make_list_for(dict['tags'])
    return dict


def dicts_in_list(content):
    blocks = cut_into_blocks(content)
    list = [get_data(blocks[i]) for i in range(len(blocks))]
    return list


def download_pages(num_of_pages):
    for i in range(1, num_of_pages + 1):
        filename = frontpage[:-5] + '_page_{}'.format(i) + frontpage[-5:]
        url = 'https://www.anime-planet.com/anime/all?page={}'.format(i)
        save_page(url, filename)
    return None


def get_content_on_one_page(num_of_pages):
    content = ''
    for i in range(1, num_of_pages + 1):
        filename = 'anime-planet_page_{}.html'.format(i)
        content = content + read_file_to_string(direktorij, filename)
    return content


def write_csv(fieldnames, rows, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return None


def write_data_in_csv(fieldnames):
    rows = dicts_in_list(get_content_on_one_page(50))
    return write_csv(fieldnames, rows, direktorij_csv, csv_file)


content_all = get_content_on_one_page(50)
d = dicts_in_list(content_all)
