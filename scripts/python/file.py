import os


def write_header(title, tags, date):
    header = '---\ntitle: "{}"\ntags: {}\ndate: {}\n---\n'.format(title, tags, date)
    return header


def write_abstract(abstract):
    return '{}\n\n<!--more-->\n'.format(abstract)


def write_content(content):
    return '{}\n'.format(content)


def write_footer(url):
    return 'The original post is {}'.format(url)


def process_file(post_content, slug):
    with open('{}/content/post/{}.md'.format(os.getenv('SITE_DIR', os.getcwd()), slug), 'w') as reader:
        reader.write(
            write_header(post_content.get('title'), post_content.get('tags'), post_content.get('creation_date')))
        reader.write(write_abstract(post_content.get('abstract')))
        reader.write(write_content(post_content.get('content')))
        reader.write(write_footer(post_content.get('canonical_url')))
        reader.close()

    return True
