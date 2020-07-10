#!/usr/bin/env python3

from pathlib import Path
import click

def get_files(path):
  files = set()
  for filename in Path(path).rglob('*.md'):
    files.add(str(filename))
  
  return files

def pprint(bad_links):
  print(bad_links)
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
    
def find_links(id_files, en_links):
  result = {}
  for idf in id_files:
    bad_links = []
    with open(idf) as f:
      fread = f.read()
      for l in en_links:
        lmd = "(" + l
        if lmd in fread:
          bad_links.append(l)
    result.update({idf: bad_links})
  return result

@click.command()
@click.argument("repo")
def main(repo):
  """
  find docs that use EN links, although the ID link already localized

  ex:
    ./localize_url.py path/to/website-repo
  """

  id_path_prefix = "%s/content/id" % (repo)
  id_path = id_path_prefix + "/docs"

  id_files = get_files(id_path)
  en_links = get_en_links(id_files, id_path_prefix)

  result = find_links(id_files, en_links)
  pprint(result)

if __name__ == '__main__':
  main()
