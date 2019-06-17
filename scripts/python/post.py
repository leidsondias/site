from datetime import datetime
from enum import Enum

import json
import re
import requests


class AnchorType(Enum):
    USER = 2
    DEFAULT = 0


MEDIUM_CDN = 'https://cdn-images-1.medium.com/max/'
UNKNOWN_TYPES = []

def transform_to_json(text):
    return json.loads(text[text.find("{"):])


def get_mentioned_users(response_json):
    return response_json.get('payload').get('mentionedUsers')


def get_post_values(response_json):
    return response_json.get('payload').get('value')


def get_post_id(json_post):
    return json_post.get('id')


def get_post_title(json_post):
    return json_post.get('title')


def get_post_creation_date(json_post):
    milliseconds = json_post.get('createdAt')
    date = datetime.utcfromtimestamp(milliseconds/1000.0)
    return date.isoformat()


def get_post_slug(json_post):
    return json_post.get('slug')


def get_post_canonical_url(json_post):
    return json_post.get('canonicalUrl')


def get_post_tags(virtuals_values):
    tags = virtuals_values.get('tags')
    return [t.get('name') for t in tags]


def get_content(json_post):
    return json_post.get('content')


def get_post_subtitle(post_content):
    return post_content.get('subtitle')


def get_paragraphs(post_content):
    return post_content.get('bodyModel').get('paragraphs')


def get_embed_github(json_response):
    return '<script src="{}"></script>'.format(json_response.get('gist').get('gistScriptUrl'))


def get_embed_youtube(json_response):
    return '<iframe width="560" height="315" src="{}" frameborder="0" allowfullscreen>'\
           '</iframe>'.format(json_response.get('iframeSrc'))


def get_embed_twitter(json_response):
    url = json_response.get('href')
    json_twitter = requests.get('https://publish.twitter.com/oembed?url={}'.format(url))
    return json_twitter.json().get('html')


MEDIAS = {
    'gist.github.com': get_embed_github,
    'www.youtube.com': get_embed_youtube,
    'twitter.com': get_embed_twitter
}


def get_embed_media(media_resource_id):
    response = requests.get('https://medium.com/media/{}?format=json'.format(media_resource_id))
    json_response = transform_to_json(response.text)
    domain = json_response.get('payload').get('value').get('domain')

    embed_media = MEDIAS[domain](json_response.get('payload').get('value'))
    return embed_media


def get_user_url(users, user_id):
    user = [u for u in users if u.get('userId') == user_id][0]
    return 'https://medium.com/@{}'.format(user.get("username"))


def get_markup(markup, text, mentioned_users=[]):
    markup_type = markup.get('type')
    start = markup.get('start')
    end = markup.get('end')

    if markup_type == 1:
        text = '{}**{}**{}'.format(text[:start], text[start:end], text[end:])
    elif markup_type == 2:
        text = '{}*{}*{}'.format(text[:start], text[start:end], text[end:])
    elif markup_type == 3:
        is_mention = markup.get('anchorType') == AnchorType.USER.value
        url = get_user_url(mentioned_users, markup.get('userId')) if is_mention else markup.get('href')
        text = '{}[{}]({}){}'.format(text[:start], text[start:end], url, text[end:])
    elif markup_type == 10:
        text = '{}`{}`{}'.format(text[:start], text[start:end], text[end:])
    else:
        UNKNOWN_TYPES.append('Unknown markup format: {} for {} text'. format(markup_type, text))

    return text


def add_markups_into_paragraph(paragraph, mentioned_users=[]):
    formatted_text = paragraph.get('text')

    seen = set()

    markups = sorted(paragraph.get('markups'), key=lambda m: (m.get('start'), m.get('type')))
    markups = [mark for mark in markups if mark.get('start') not in seen and not seen.add(mark.get('start'))][::-1]

    for markup in markups:
        formatted_text = get_markup(markup, formatted_text, mentioned_users)

    return formatted_text


def format_paragraph_by_type(paragraph, mentioned_users=[]):
    paragraph_type = paragraph.get('type')
    text = add_markups_into_paragraph(paragraph, mentioned_users)

    markdown = None
    if paragraph_type == 1:
        markdown = ''
    elif paragraph_type == 2:
        markdown = '# '
        text = re.sub(r'\n', '#', text)
    elif paragraph_type == 3:
        markdown = '## '
        text = re.sub(r'\n', '##', text)
    elif paragraph_type == 4:
        img_width = paragraph.get('metadata').get('originalWidth')
        id = paragraph.get('metadata').get('id')
        markdown = '![{}]({}{}/{})'.format(text, MEDIUM_CDN, max(img_width*2, 2000), id)
        text = '*{}*'.format(text)
    elif paragraph_type == 6:
        markdown = '>'
    elif paragraph_type == 7:
        pass
    elif paragraph_type == 8:
        markdown = '```\n{}\n```'.format(text)
        text = ''
    elif paragraph_type == 9:
        markdown = '* '
    elif paragraph_type == 10:
        markdown = '1. '
    elif paragraph_type == 11:
        media_resource_id = paragraph.get('iframe').get('mediaResourceId')
        markdown = get_embed_media(media_resource_id)
        text = '*{}*'.format(text.strip()) if text else ''
    else:
        UNKNOWN_TYPES.append('Unknown paragraph format: {} for {} text'. format(paragraph_type, text))

    return '\n{}{}\n'.format(markdown, text)


def transform_paragraph(paragraph, mentioned_users=[]):
    return format_paragraph_by_type(paragraph, mentioned_users)


def process_paragraphs(paragraphs, mentioned_users=[]):
    return [transform_paragraph(p, mentioned_users) for p in paragraphs]


def get_post(url):
    url = '{}?format=json'.format(url)
    response = requests.get(url)
    return transform_to_json(response.text)


def process_post(url):
    json_post = get_post(url)
    values = get_post_values(json_post)
    mentioned_users = get_mentioned_users(json_post)
    post_content = get_content(values)
    paragraphs = get_paragraphs(post_content)
    text = process_paragraphs(paragraphs, mentioned_users)

    return {
        'abstract': ''.join(text[1:2] if len(text[1:2]) > 50 else text[1:3]),
        'canonical_url': get_post_canonical_url(values),
        'content': ''.join(text[2:] if len(text[1:2]) > 50 else text[3:]),
        'creation_date': get_post_creation_date(values),
        'full_text': ''.join(text),
        'slug': get_post_slug(values),
        'tags': get_post_tags(values.get('virtuals')),
        'title': get_post_title(values),
        'unknown_types': UNKNOWN_TYPES or ['All markups and paragraphs was process with success']
    }
