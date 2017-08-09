from . import local

def get_posts(search_string, min_score, uploaded_after, page_number, max_results, session):
    request = 'https://e621.net/post/index.json?' + \
        'tags=' + search_string + \
        ' date:>=' + str(uploaded_after) + \
        ' score:>=' + str(min_score) + \
        '&page=' + str(page_number) + \
        '&limit=' + str(max_results)

    local.print_log('remote', 'debug', 'Post request URL: \"' + request + '\".')

    return session.get(request).json()

def get_tag_alias(user_tag, session):
    prefix = ''

    if ':' in user_tag:
        return user_tag

    if user_tag[0] == '~':
        prefix = '~'
        user_tag = user_tag.strip('~')

    if user_tag[0] == '-':
        prefix = '-'
        user_tag = user_tag.strip('-')

    request = 'https://e621.net/tag/index.json?name=' + user_tag
    results = session.get(request).json()

    for tag in results:
        if user_tag == tag['name']:
            return prefix + user_tag

    request = 'https://e621.net/tag_alias/index.json?query=' + user_tag + '&approved=true'
    results = session.get(request).json()

    for tag in results:
        if user_tag == tag['name']:
            request = 'https://e621.net/tag/show.json?id=' + str(tag['alias_id'])
            results = session.get(request).json()

            return prefix + results['name']

    print('')
    local.print_log('remote', 'error', 'The tag ' + prefix + user_tag + ' is spelled incorrectly or does not exist.')
    exit()

def download_post(url, path, session):
    with open(path, 'wb') as outfile:
        for chunk in session.get(url, stream = True).iter_content(chunk_size = 1024):
            if chunk:
                outfile.write(chunk)
