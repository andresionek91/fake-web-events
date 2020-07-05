from setuptools import setup

setup(
    name='fake_web_events',
    version='0.1.0',
    description='Generator of semi-random fake web events. ',
    author='Andre Sionek',
    author_email='andresionek91@gmail.com',
    url="https://github.com/andresionek91/fake-web-events",
    project_urls={
        "Documentation": "https://github.com/andresionek91/fake-web-events/blob/master/README.md"
    },
    packages=['fake_web_events'],
    install_requires=['pyaml==20.4.0', 'pytest==5.4.3', 'faker==4.1.1']
)
