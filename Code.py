import requests
import re
import csv
import os
import html
import sys
import tags
import json

first_page_url = 'https://www.anime-planet.com/anime/all'
directory_p = 'Pages'
directory_csv = 'Csv_files'
directory_json = 'Json'
csv_file = 'anime-planet.csv'
csv_tags = 'anime-planet_tags.csv'
json_file = 'anime-planet.json'
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
    return save_string_to_file(text, directory_p, filename)


def read_file_to_string(directory, filename):
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        return file_in.read()


def cut_into_blocks(page):
    pattern = re.compile(
        r'(<li data-id=".*?".*?<a title="<h5>.*?)<div class="crop">',
        re.DOTALL
    )
    return [x.group(1).strip() for x in re.finditer(pattern, page)]


def get_data(page):
    pattern = re.compile(
        r'''<li data-id="(?P<id>.*?)".*?'''
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

    def add_exceptions(pattern, page, string, groupdict_name):
        if re.search(pattern, page) is None:
            return 'No {} found'.format(string)
        else:
            return re.search(pattern, page).groupdict()[groupdict_name]

    def make_intiger_for(string):
        string = string.replace(' eps', '')
        string = string.replace(' ep', '')
        string = string.replace('+', '')
        return int(string)

    dict = {}
    dict['id'] = int(re.search(pattern, page).groupdict()['id'])
    dict['title'] = re.search(pattern, page).groupdict()['title']
    dict['alt_title'] = add_exceptions(pattern_3, page, 'alternative title', 'alt_title')
    dict['type'] = re.search(pattern, page).groupdict()['type']
    dict['num_of_ep'] = re.search(pattern, page).groupdict()['num_eps']
    dict['studio'] = add_exceptions(pattern_2, page, 'studio', 'studio')
    dict['year'] = int(re.search(pattern, page).groupdict()['year'])
    dict['rating'] = float(re.search(pattern, page).groupdict()['rating'])
    # dict['description'] = re.search(pattern, page).groupdict()['description']

    # clear data
    if 'TV' in dict['type']:
        dict['type'] = dict['type'] + ' Series'

    dict['title'] = html.unescape(dict['title'])
    dict['title'] = dict['title'].replace(';', ' ')
    dict['alt_title'] = html.unescape(dict['alt_title'])
    dict['alt_title'] = dict['alt_title'].replace(';', ' ')
    dict['num_of_ep'] = make_intiger_for(dict['num_of_ep'])
    # dict['description'] = html.unescape(dict['description'])
    return dict


def dicts_in_list(content, function_for_getting_data):
    blocks = cut_into_blocks(content)
    list = [function_for_getting_data(blocks[i]) for i in range(len(blocks))]
    return list


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


def get_content_on_one_page(num_of_pages):
    content = ''
    for i in range(1, num_of_pages + 1):
        filename = 'anime-planet_page_{}.html'.format(i)
        content = content + read_file_to_string(directory_p, filename)
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


def write_data_in_csv(fieldnames, list, csv_filename):
    return write_csv(fieldnames, list, directory_csv, csv_filename)


def write_json(list, directory, filename):
    '''Iz danega objekta ustvari JSON datoteko.'''
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as json_file:
        json.dump(list, json_file, indent=4, ensure_ascii=False)
    return None


content_all = get_content_on_one_page(50)
d = dicts_in_list(content_all, get_data)
# keys_d = d[0].keys()
l = tags.make_tags_list(content_all)
# keys_l = l[0].keys()
write_data_in_csv(d[0].keys(), d, csv_file)
write_data_in_csv(l[0].keys(), l, csv_tags)
write_json(d, directory_json, json_file)
