
from codecs import open
import json
from os import path
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

with open(path.join(here, "config.json"), "rt") as f:
    conf = json.load(f)

# Generate meta.yaml
metayaml = conf["metayaml"]
metayaml["package"]["version"] = conf["setuppy"]["version"]
metayaml["source"]["git_rev"] = conf["setuppy"]["version"]
metayaml["about"]["home"] = conf["setuppy"]["url"]
metayaml["about"]["license"] = conf["setuppy"]["license"]

with open(path.join(here, "./conda-recipe/meta.yaml"), "wt") as f:
    json.dump(metayaml, f)

# setup
setup_dict = conf["setuppy"]
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    setup_dict["long_description"] = f.read()

setup_dict["packages"] = find_packages(exclude=["pygosemsim.test*"])

setup(**setup_dict)
