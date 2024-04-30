import os
from setuptools import find_packages, setup


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


def read_file(rel_path):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(current_dir, rel_path), "r") as f:
        return f.read()
    

def get_version(rel_path):
    for line in read_file(rel_path).splitlines():
        if line.startswith("__version__"):
            return line.split("'")[1]
    raise RuntimeError("Unable to find version string")


with open("requirements.txt", "r") as requirements:
    setup(
        name="pytorch_cnn",
        version=get_version("src/__init__.py"),
        author="jeanettepoh",
        author_email="jeanettepoh19@gmail.com",
        install_requires=list(requirements.read().splitlines()),
        package=find_packages(),
        description="CNN image classification",
        long_description=long_description,
        long_description_content_type="text/markdown"
    )