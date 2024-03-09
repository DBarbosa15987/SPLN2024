#!/usr/bin/env python3

"""
docs
"""

from tabnanny import verbose
import jjcli
import jinja2
from glob import glob

def main():
    modes = glob("*.py")
    if len(modes) > 1:
        name = modes[0].replace(".py","")
    else:
        name = input("Módulo?")

    v = jjcli.qx(f"grep __version__ '{name}.py'")
    print(v)
    version = "0.0.1"

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

    out = pp.render({"name":name,"autor":"Diogo","email":"dbarbosa15987@gmail.com","version":"0.0.1"})
    print(out)
    f = open("pyproject.toml","w")
    f.write(out)
    f.close()

if __name__ == "__main__":
    main()
