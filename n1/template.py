import jinja2
from glob import glob

modes = glob("*.py")
if len(modes) > 1:
    name = modes[0].replace(".py","")
else:
    name = input("Módulo?")

pp = jinja2.Template("""

[build-system]
requires = ["flit_core >=3.2,<4"]
build-backend = "flit_core.buildapi"


[project]
name = "{{name}}"
authors = [{ name = "{{autor}}", email = "{{email}}" }]
classifiers = ["License :: OSI Approved :: MIT License"]
readme = "README.md"
requires-python = ">=3.8"
dynamic = ["version", "description"]
dependencies = ["FIXME"]


[project.scripts]
{{name}} = "{{name}}:main"


""")

a = pp.render({"name":name,"autor":"Diogo","email":"dbarbosa15987@gmail.com"})
print(a) 