import os
from typing import List
from setuptools import find_packages, setup


HYPHEN_E_DOT = "-e ."

def get_requirements(file_path:str) -> List[str]:
    """
    This function will return the list of requirements
    """
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements


setup(
    name="pytorch_cnn",
    version="0.0.1",
    author="jeanettepoh",
    author_email="jeanettepoh19@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements_dev.txt")
)