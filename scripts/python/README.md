# Transform Medium to Markdown

Transform your Medium publications to Markdown.

If you use [hugo](http://gohugo.io), you can pass argument `--hugo` and create the post for hugo.

## Usage

```
python main {url}
  --hugo - create post for Hugo framework <https://gohugo.io/>
  -hu, --hugo-update - Update the Hugo post
  -d, --debug - shows all errors when process the paragraphs and markups
```

### Hugo

For create automatically the post for Hugo, you need pass the `--hugo` argument.

The command needs know where Hugo project is.

So, you can Export `SITE_DIR` variable.
```
╰─$ export SITE_DIR='/path/to/your/site/project'
```

Or run the command where are your the website it:
```
cd /path/to/your/site/project && python /path/to/script.py <MEDIUM_URL> --hugo
```
