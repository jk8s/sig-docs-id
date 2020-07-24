#!/usr/bin/env python3

from pathlib import Path
import click

def get_files(path):
  files = set()
  for filename in Path(path).rglob('*.md'):
    files.add(str(filename))
  
  return files

def pprint(bad_links):
  for k,v in bad_links.items():
    if len(v) > 0:
      print(k)
      for vv in v:
        print("--> " + vv)
      print()

def get_en_links(id_files, path):
  links = set()
  for f in id_files:
    links.add(f[len(path):-3])
  return links
    
def find_links(id_files, id_path_prefix, overwrite=False):
  en_links = get_en_links(id_files, id_path_prefix)

  result = {}
  for idf in id_files:
    bad_links = []
    with open(idf, "r") as f:
      fread = f.read()
      f.close()
      for en_link in en_links:
        en_link_md = "(" + en_link
        id_link_md = "(/id" + en_link
        if en_link_md in fread:
          bad_links.append(en_link)
          fread = fread.replace(en_link_md, id_link_md)
      if overwrite==True:
        w = open(idf, "w")
        w.write(fread)
        w.close()
    result.update({idf: bad_links})
  return result

@click.command()
@click.argument("repo")
@click.option("-o","--overwrite",default=False,type=bool,help='overwrite current file to use ID links')
def main(repo, overwrite):
  """
  find docs that use EN links, although the ID link already localized

  ex:
    ./localize_url.py path/to/website-repo
  """

  id_path_prefix = "%s/content/id" % (repo)
  id_path = id_path_prefix + "/docs"

  id_files = get_files(id_path)

  result = find_links(id_files, id_path_prefix, overwrite)
  pprint(result)

if __name__ == '__main__':
  main()
