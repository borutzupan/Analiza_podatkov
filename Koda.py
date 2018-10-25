import requests
import re
import csv
import os

spletna_stran = 'https://www.anime-planet.com/anime/all'
direktorij = 'Analiza_podatkov_pages'
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
            return 'No alternative titles'
        else:
            return re.search(pattern_2, page).groupdict()['alt_title']

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

    dict['num_of_ep'] = make_intiger_for(dict['num_of_ep'])
    dict['description'] = dict['description'].replace('&nbsp;', ' ')
    dict['tags'] = make_list_for(dict['tags'])
    return dict


def dicts_in_list(directory, filename):
    content = read_file_to_string(directory, filename)
    blocks = cut_into_blocks(content)
    list = [get_data(blocks[i]) for i in range(len(blocks))]
    return list


def write_csv(fieldnames, rows, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return None


def write_data_in_csv(fieldnames):
    rows = dicts_in_list(direktorij, frontpage)
    return write_csv(fieldnames, rows, direktorij, csv_file)


def download_pages(num_of_pages):
    for i in range(1, num_of_pages + 1):
        filename = frontpage[:-5] + '_page_{}'.format(i) + frontpage[-5:]
        url = 'https://www.anime-planet.com/anime/all?page={}'.format(i)
        save_page(url, filename)
    return None
