import codecs
from setuptools import setup


with codecs.open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="zproxy",
    version="0.1.0",
    #license='http://www.apache.org/licenses/LICENSE-2.0',
    description="A Zookeeper client used for loadbalancing and disaster tolerating",
    author='wei',
    author_email='rovluo@gmail.com',
    url='https://github.com/cultcode/zproxy',
    packages=['zproxy'],
    package_data={
        'zproxy': ['README.md']
    },
    install_requires=[],
    entry_points="""
    [console_scripts]
    zproxy = zproxy.zproxy:main
    """,
    classifiers=[
        #'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: Proxy Servers',
    ],
    long_description=long_description,
)
