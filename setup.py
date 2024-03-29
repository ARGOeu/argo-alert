from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '1.0.0'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    name='argoalert',
    scripts=['bin/argo-alert-publisher','bin/argo-alert-rulegen'],
    version=__version__,
    description='Publisher of argo-streaming status events as alerts to an alerta service endpoint',
    long_description=long_description,
    url='https://github.com/ARGOeu/argoalert',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='GRNET',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email='argo@mailman.egi.eu'
)
