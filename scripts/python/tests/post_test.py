import unittest
import json
from unittest import mock

from post import (transform_to_json, get_post_values, get_post_title, get_post_creation_date, get_content,
                  get_post_subtitle, get_post_slug, get_post_canonical_url, get_post_tags, get_paragraphs,
                  process_paragraphs, get_post_id, get_mentioned_users)


def read_files(name):
    with open('fixtures/{}'.format(name), 'r') as file:
        data = file.read()

    return data


class TestPost(unittest.TestCase):
    def setUp(self):
        self.response_text = read_files('response_text.txt')
        self.response_json = json.loads(read_files('response_json.json'))
        self.values = self.response_json.get('payload').get('value')
        self.mentioned_users = self.response_json.get('payload').get('mentionedUsers')
        self.post_content = self.values.get('content')
        self.virtuals_values = self.values.get('virtuals')
        self.paragraphs = self.post_content.get('bodyModel').get('paragraphs')

    def test_transform_to_json(self):
        json_response = transform_to_json(self.response_text)
        self.assertTrue(json_response.get('success'))

    def test_get_post_values(self):
        values = get_post_values(self.response_json)
        self.assertEqual(self.values, values)

    def test_get_mentioned_users(self):
        mentioned_users = get_mentioned_users(self.response_json)
        self.assertTrue(any(users for users in mentioned_users if users.get('userId') == "e8066e7af3d3"))

    def test_get_post_id(self):
        post_id = get_post_id(self.values)
        self.assertEqual('9e7c2da45602', post_id)

    def test_get_title(self):
        title = get_post_title(self.values)
        self.assertEqual('Web Components with Redux', title)

    def test_get_creation_date(self):
        creation_date = get_post_creation_date(self.values)
        self.assertEqual('2019-05-22T20:12:49.717000', creation_date)

    def test_get_slug(self):
        slug = get_post_slug(self.values)
        self.assertEqual('web-components-with-redux', slug)

    def test_get_canonical_url(self):
        canonical_url = get_post_canonical_url(self.values)
        self.assertEqual('https://medium.com/@leidsoncruz/web-components-with-redux-9e7c2da45602', canonical_url)

    def test_get_tags(self):
        tags = get_post_tags(self.virtuals_values)
        self.assertEqual(['Web Components', 'JavaScript', 'Redux', 'Event Driven Architecture'], tags)

    def test_get_content(self):
        content = get_content(self.values)
        self.assertTrue(self.post_content, content)

    def test_get_subtitle(self):
        subtitle = get_post_subtitle(self.post_content)
        expected = 'You need use Web Components in the your application? No you don’t need. '\
                   'I’am totally against from the hype. You should use if only you…'
        self.assertEqual(expected, subtitle)

    def test_get_paragraphs(self):
        paragraphs = get_paragraphs(self.post_content)
        self.assertTrue(len(paragraphs) > 0)

    def test_process_paragraphs_type_1(self):
        markdown = process_paragraphs(self.paragraphs[1:2])
        expected = ['\nYou need use Web Components in the your application? No you don’t need. '\
                    'I’am totally against from the hype. You should use if only you need. I see some '\
                    'advantages to use if you really need. For example: componentization and your '\
                    'advantages, very small final bundle size and etc.\n']
        self.assertEqual(expected, markdown)

    def test_process_paragraphs_type_3(self):
        markdown = process_paragraphs(self.paragraphs[:1])
        self.assertEqual(['\n## Web Components with Redux\n'], markdown)

    def test_process_paragraphs_type_4(self):
        markdown = process_paragraphs(self.paragraphs[66:67])
        expected = ['\n![cap da imagem](https://cdn-images-1.medium.com/max/2744/1*X-X8xve-7LRf2f_IVhQCbg.png)*cap '\
                    'da imagem*\n']
        self.assertEqual(markdown, expected)

    def test_process_paragraphs_type_6(self):
        markdown = process_paragraphs(self.paragraphs[68:69])
        expected = ['\n>quotes de alguém com youtube abaixo\n']
        self.assertEqual(markdown, expected)

    def test_process_paragraphs_type_8(self):
        markdown = process_paragraphs(self.paragraphs[73:74])
        expected = ['\n```\nTeste de code aqui sem syntex highligh\n```\n']
        self.assertEqual(markdown, expected)

    @mock.patch('requests.get')
    def test_process_paragraphs_type_11_gist(self, mock_get_embed_media):
        mock_get_embed_media.return_value.text = read_files('response_media_gist_text.txt')

        markdown = process_paragraphs(self.paragraphs[8:9])
        expected = '<script src="https://gist.github.com/leidsondias/fec20e1535c4bb832a85321f84fb08d9.js"></script>'
        self.assertTrue(expected in markdown[0])

    @mock.patch('requests.get')
    def test_process_paragraphs_type_11_youtube(self, mock_get_embed_media):
        mock_get_embed_media.return_value.text = read_files('response_media_youtube_text.txt')
        markdown = process_paragraphs(self.paragraphs[69:70])
        expected = ['\n<iframe width="560" height="315" src="https://cdn.embedly.com/widgets/media.html?src=https%3A'\
                    '%2F%2Fwww.youtube.com%2Fembed%2FN6ZfqHGeN9Q%3Fstart%3D4631%26feature%3Doembed%26start%3D4631&ur'\
                    'l=http%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DN6ZfqHGeN9Q&image=https%3A%2F%2Fi.ytimg.com%2Fvi%2F'\
                    'N6ZfqHGeN9Q%2Fhqdefault.jpg&key=a19fcc184b9711e1b4764040d3dc5c07&type=text%2Fhtml&schema=youtube'\
                    '" frameborder="0" allowfullscreen></iframe>\n']
        self.assertEqual(markdown, expected)

    def test_process_paragraphs_type_11_twitter(self):
        # multiples mocks here
        markdown = process_paragraphs(self.paragraphs[71:72])
        expected = ['\n<blockquote class="twitter-tweet"><p lang="pt" dir="ltr">Só Vem, Amigos!!! RT <a href="https:'\
                    '//t.co/z9DFfPHN3s">https://t.co/z9DFfPHN3s</a> <a href="https://t.co/F0151AeovH">pic.twitter.com/'\
                    'F0151AeovH</a></p>&mdash; FIFA TRADE CHANNEL Oficial 🌀 (@FIFATRADECHANN1) <a href="https://twitt'\
                    'er.com/FIFATRADECHANN1/status/1057437847274303488?ref_src=twsrc%5Etfw">October 31, 2018</a></bloc'\
                    'kquote>\n<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>\n\n']
        self.assertEqual(markdown, expected)

    def test_process_paragraphs_markup_type_1(self):
        markdown = process_paragraphs(self.paragraphs[2:3])
        expected = '**Stories** like **Instagram**'
        self.assertTrue(expected in markdown[0])

    def test_process_paragraphs_markup_type_2(self):
        markdown = process_paragraphs(self.paragraphs[6:7])
        expected = '*name, oldValue *and* newValue*'
        self.assertTrue(expected in markdown[0])

    def test_process_paragraphs_markup_type_3(self):
        markdown = process_paragraphs(self.paragraphs[75:76])
        expected = '[https://domchristie.github.io/turndown/](https://domchristie.github.io/turndown/)'
        self.assertTrue(expected in markdown[0])

    def test_process_paragraphs_markup_type_10(self):
        markdown = process_paragraphs(self.paragraphs[72:73])
        expected = ['\n`code aqui amigo` e aqui:\n']
        self.assertEqual(markdown, expected)

    def test_process_paragraphs_with_same_word_in_phrase(self):
        markdown = process_paragraphs(self.paragraphs[23:24])
        expected = ['\nWhy will use **Redux**? Using **Redux** my code became is very simple and very easy to get data '\
                    'an another components. With it my problems for events control is over as like bugs create by we '\
                    'on the migration progress (**Vanilla** > **Web Components**) haha.\n']

        self.assertEqual(expected, markdown)

    def test_process_paragraph_with_multiples_markups_in_same_word(self):
        markdown = process_paragraphs(self.paragraphs[6:7])
        print(markdown)
