from setuptools import setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

with open("requirements.txt", "r") as requirements_file:
    requirements = requirements_file.read().split('\n')

setup(
    name="projekt XI",
    version="0.0.1",
    author="Dominika Bober",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=requirements,
)
