from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fake_web_events',
    version='0.1.2',
    description='Generator of semi-random fake web events. ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['fake', 'web events', 'events'],
    license='MIT',
    author='Andre Sionek',
    author_email='andresionek91@gmail.com',
    url="https://github.com/andresionek91/fake-web-events",
    packages=['fake_web_events'],
    install_requires=['pyaml==20.4.0', 'pytest==5.4.3', 'faker==4.1.1'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)

