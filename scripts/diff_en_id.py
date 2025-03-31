#!/usr/bin/env python

from pathlib import Path
import click

def get_files(path):
    files = set()
    for filename in Path(path).rglob('*.md'):
        files.add(str(filename))
    return files

def write_diff(source_files, target_files, source_language, target_language, output_file):
    for f in source_files:
        target_file = str(f).replace(f'/{source_language}/', f'/{target_language}/')
        if target_file not in target_files:
            output_file.write(f + '\n')

@click.command()
@click.argument("repo")
def main(repo):
    """
    Find the diff between EN and ID docs in master branch

    ex:
      ./diff_en_id.py path/to/website-repo
    """
    en_path = f"{repo}/content/en/docs"
    id_path = f"{repo}/content/id/docs"

    en_files = get_files(en_path)
    id_files = get_files(id_path)

    output_path = Path(__file__).parent / "diff_en_id_result.txt"

    with open(output_path, "w") as output_file:
        output_file.write("These ID pages must be removed, since they no longer exist in latest EN docs:\n")
        write_diff(id_files, en_files, "id", "en", output_file)

        output_file.write("\nThese EN pages must be translated, since they do not yet exist in latest ID docs:\n")
        write_diff(en_files, id_files, "en", "id", output_file)

    print(f"Diff results saved to {output_path}. Please check the file for details.")

if __name__ == '__main__':
    main()
