import argparse
import subprocess
import os

import file
import post


parser = argparse.ArgumentParser("url")
parser.add_argument("url", help="The medium url post.", type=str)
parser.add_argument("--hugo", help="Create post for Hugo framework <https://gohugo.io/>", action="store_true")
parser.add_argument("--hugo-update", "-hu", help="Update the Hugo post", action="store_true")
parser.add_argument("--debug", "-d", help="Print the unknown formats when process the paragraphs and markups", action="store_true")
url = parser.parse_args().url

post_content = post.process_post(url)
slug = post_content.get('slug')

if parser.parse_args().hugo:
    result = subprocess.run('cd {}; hugo new post/{}.md'.format(os.getenv('SITE_DIR', os.getcwd()), slug),
                            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    if 'post/{}.md created'.format(slug) in str(result.stdout):
        was_process = file.process_file(post_content, slug)

        if was_process:
            print('Post created with markdown')
    else:
        raise ValueError("Post is not create \n {}".format(str(result.stdout)))
elif parser.parse_args().hugo_update:
    was_process = file.process_file(post_content, slug)

    if was_process:
        print('Post updated with success')
else:
    print(post_content.get('full_text'))

if parser.parse_args().debug:
    print('\n\n----------------\n\n','DEBUG CONSOLE','\n\n----------------\n\n',
            '\n'.join(post_content.get('unknown_types')))
