import unittest

import file


class TestFile(unittest.TestCase):
    def setUp(self):
        self.title = 'Transform Medium to Markdown'
        self.tags = ['Python', 'Markdown', 'Medium']
        self.date = '2019-05-27T08:05:48.870000'

    def test_write_header(self):
        expected = '---\ntitle: "{}"\ntags: {}\ndate: {}\n---\n'.format(self.title, self.tags, self.date)
        header = file.write_header(self.title, self.tags, self.date)
        self.assertEqual(expected, header)

    def test_write_abstract(self):
        expected = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas in.\n\n<!--more-->\n'
        abstract = file.write_abstract('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas in.')
        self.assertEqual(expected, abstract)

    def test_write_content(self):
        expected = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas in.\n'
        content = file.write_content('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas in.')
        self.assertEqual(expected, content)

    def test_write_footer(self):
        expected = 'The original post is http://www.medium.com.br/@leidson.cruz'
        footer = file.write_footer('http://www.medium.com.br/@leidson.cruz')
        self.assertEqual(expected, footer)
