import re


def cut_into_blocks(page):
    pattern = re.compile(
        r'(<li data-id=".*?".*?<a title="<h5>.*?)<div class="crop">',
        re.DOTALL
    )
    return [x.group(1).strip() for x in re.finditer(pattern, page)]


def get_id_tags(page):
    pattern_id = r'''<li data-id="(?P<id>.*?)"'''
    pattern_tags = re.compile(
        r'Tags</h4><ul>(?P<tags>.*?)</ul>'
    )

    def make_list_for(string):
        string = string.replace('<li>', '').replace('</li>', ', ')
        string = string.strip()
        string = string.split(', ')
        return string

    def add_exceptions(pattern, page, string, groupdict_name):
        if re.search(pattern, page) is None:
            return 'No {} found'.format(string)
        else:
            return re.search(pattern, page).groupdict()[groupdict_name][:-5]

    list = []
    string_tags = add_exceptions(pattern_tags, page, 'tags', 'tags')
    list_tags = make_list_for(string_tags)
    int_id = int(re.search(pattern_id, page).groupdict()['id'])
    for i in range(len(list_tags)):
        list.append({'id': int_id, 'tags': list_tags[i]})
    return list


def make_tags_list(content):
    blocks = cut_into_blocks(content)
    list = []
    for i in range(len(blocks)):
        list += get_id_tags(blocks[i])
    return list
