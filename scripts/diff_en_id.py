#!/usr/bin/env python

from pathlib import Path
import click

def get_files(path):
  files = set()
  for filename in Path(path).rglob('*.md'):
    files.add(str(filename))
  
  return files

def print_diff(source_files, target_files, source_language, target_language):
  for f in source_files:
    target_file = str(f).replace('/%s/' % source_language, '/%s/' % target_language)
    if target_file not in target_files:
      print(f)

@click.command()
@click.argument("repo")
def main(repo):
  """
  Find the diff between EN and ID docs in master branch

  ex:
    ./diff_en_id.py path/to/website-repo
  """
  en_path = "%s/content/en/docs" % (repo)
  id_path = "%s/content/id/docs" % (repo)

  en_files = get_files(en_path)
  id_files = get_files(id_path)

  print('These ID pages must be removed, since no longer exist in latest EN docs:')
  print_diff(id_files, en_files, 'id', 'en')

  print()
  print('These EN pages must be translated, since not yet exist in latest ID docs:')
  print_diff(en_files, id_files, 'en', 'id')

if __name__ == '__main__':
  main()
