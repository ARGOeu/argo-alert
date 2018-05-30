from setuptools import setup

_NAME = 'argo-ams'
_VERSION = '0.0.1'


setup(
    name=_NAME,
    version=_VERSION,
    author='GRNET',
    author_email='kaggis@admin.grnet.gr',
    license='ASL 2.0',
    description= 'Publish alerta alerts to AMS',
    long_description='Alerta plugin to publish alerts to an AMS endpoint',
    url='https://github.com/ARGOeu/argo-alert',
    py_modules=['argo_ams'],
    include_package_data=True,
    zip_safe=True,
    entry_points={
        'alerta.plugins': [
            'ams = argo_ams:AmsPub'
        ]
    },
    install_requires=['argo-ams-library']
)
