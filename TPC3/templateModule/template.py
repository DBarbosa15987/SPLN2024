#!/usr/bin/env python3

"""
docs
"""
from tabnanny import verbose
import jjcli
import jinja2
from glob import glob
import os
import json

def main():

    modes = glob("*.py")
    version = "0.0.1"
    metadata = {}
    if len(modes) > 1:
        modes.remove("template.py")
        name = modes[0].replace(".py","")
        version = jjcli.qx(f"grep __version__ '{name}.py'")
    else:
        name = input("Insert the Module Name:")
        

    file_path = os.path.expanduser("~/.METADATA.json")

    if not os.path.exists(file_path):
        print(f"{file_path} not found, creating new METADATA.json")
        with open(file_path, "w") as f:
            author = input("Name:")
            email = input("email:")
            metadata = {"autor":author,"email":email}
            json.dump(metadata, f,ensure_ascii=False)
    else:
        with open(file_path, "r") as f:
            metadata = json.load(f)

    metadata['name'] = name
    metadata["version"] = version
    pp = jinja2.Template("""

    [build-system]
    requires = ["flit_core >=3.2,<4"]
    build-backend = "flit_core.buildapi"


    [project]
    name = "{{name}}"
    authors = [{ name = "{{autor}}", email = "{{email}}" }]
    version = "{{version}}"
    classifiers = ["License :: OSI Approved :: MIT License"]
    requires-python = ">=3.8"
    dynamic = ["description"]
    dependencies = []


    [project.scripts]
    {{name}} = "{{name}}:main"


    """)

    out = pp.render(metadata)
    print(out)
    f = open("pyproject.toml","w")
    f.write(out)
    f.close()

if __name__ == "__main__":
    main()
