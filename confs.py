#!/usr/bin/env python3
import os
from pathlib import Path
import jinja2
import yaml

CONFIG_PATH = (Path(__file__).parent / 'config.yml').resolve()
TEMPLATE_PATH = (Path(__file__).parent / 'templates').resolve()
DESTINATION_PATH = Path('/var/lib/liquid/')

jinja_loader = jinja2.FileSystemLoader(str(TEMPLATE_PATH))
jinja_env = jinja2.Environment(loader=jinja_loader)

def files_under(path):
    def _generate(path, root):
        for sub in path.iterdir():
            if sub.is_dir():
                yield from _generate(sub, root)
            else:
                yield sub.relative_to(root)

    return set(_generate(path, path))

def install_template(configs, relative_path):
    template = (TEMPLATE_PATH / relative_path)
    destination = (DESTINATION_PATH / relative_path)

    # if the file exists in the destination, but not in the template
    # then remove it from the destination.
    if not template.exists():
        try:
            print("Removing", str(relative_path),
                  "from the destination")
            os.remove(str(destination.resolve()))
        except OSError:
            print("Tried to remove", str(destination),
                  "but it did not exist in the destination")
        finally:
            return

    payload = jinja_env.get_template(str(relative_path)).render(configs)

    if not destination.parent.exists():
        print("Creating the parent directory", str(destination.parent))
        destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists():
        with destination.open() as f:
            current_payload = f.read()
        if current_payload == payload:
            print("Skipping unchanged file", str(relative_path))
            return

    print("Writing to", str(relative_path))
    with destination.open('w') as f:
        f.write(payload)

def install_templates(configs):
    templates = files_under(TEMPLATE_PATH)
    existing_destinations = files_under(DESTINATION_PATH)
    for template in templates.union(existing_destinations):
        install_template(configs, template)

def main():
    with CONFIG_PATH.open() as f:
        configs = yaml.load(f)
    print(configs)
    install_templates(configs)

if __name__ == '__main__':
    main()
