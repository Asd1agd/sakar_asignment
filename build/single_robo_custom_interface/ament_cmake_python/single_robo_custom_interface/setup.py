from setuptools import find_packages
from setuptools import setup

setup(
    name='single_robo_custom_interface',
    version='0.0.0',
    packages=find_packages(
        include=('single_robo_custom_interface', 'single_robo_custom_interface.*')),
)
