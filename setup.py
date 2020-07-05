from setuptools import setup

setup(
    name='fake_web_events',
    version='0.1.0',
    description='Generator of semi-random fake web events. ',
    keywords=['fake', 'web events', 'events'],
    license='MIT',
    author='Andre Sionek',
    author_email='andresionek91@gmail.com',
    url="https://github.com/andresionek91/fake-web-events",
    project_urls={
        "Documentation": "https://github.com/andresionek91/fake-web-events/blob/master/README.md"
    },
    packages=['fake_web_events'],
    install_requires=['pyaml==20.4.0', 'pytest==5.4.3', 'faker==4.1.1'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)

