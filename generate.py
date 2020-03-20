# generate site from static pages, loosely inspired by Jekyll
# run like this:
#   ./generate.py test/source output
# the generated `output` should be the same as `test/expected_output`

import os
import logging
import jinja2
import sys
import json
import filecmp

log = logging.getLogger(__name__)


def list_files(folder_path):
    for name in os.listdir(folder_path):
        base, ext = os.path.splitext(name)
        if ext != '.rst':
            continue
        yield os.path.join(folder_path, name)

def read_file(file_path):
    with open(file_path, 'r') as f:
        raw_metadata = ""
        for line in f:
            if line.strip() == '---':
                break
            raw_metadata += line
        content = ""
        for line in f:
            content += line
    return json.loads(raw_metadata), content

def write_output(name, html):
    with open(name+'.html', "w") as f:
        f.write(html)

# function to make the filename for the output file
def filename_output(folder_path, file_path, output_folder):
    name = os.path.split(file_path)[1]
    name, ext = os.path.splitext(name)
    folder_name = os.path.split(folder_path)[0]
    folder_name = os.path.join(folder_name, output_folder)
    # create the output folder, if it doesn't exist
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    name = os.path.join(folder_name, name)
    return name

def generate_site(folder_path, output_folder):
    log.info("Generating site from %r", folder_path)
     # should enable trim_blocks and lstrip_blocks to remove whitespaces in the html created
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(folder_path + '/layout'), trim_blocks = True, lstrip_blocks = True)
    for file_path in list_files(folder_path):
        metadata, content = read_file(file_path)
        template_name = metadata['layout']
        template = jinja_env.get_template(template_name)
        data = dict(metadata, content=content)
        # create the html from the template
        html = template.render(data)
        # get the filename for the output file
        name = filename_output(folder_path, file_path, output_folder)
        # write the html to the output file
        write_output(name, html)
        log.info("Writing %r with template %r", name, template_name)

def test_output1():
    assert filecmp.cmp("test/output/contact.html", "test/expected_output/contact.html"), "Files should be identical"

def test_output2():
    assert filecmp.cmp("test/output/index.html", "test/expected_output/index.html"), "Files should be identical"

def main():
    generate_site(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    logging.basicConfig()
    main()
    """
    test_output1()
    test_output2()
    print("Everything passed")
    """