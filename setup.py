import io
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requires = [pkg.strip() for pkg in open('requirements.txt', 'r').readlines()]

version = ''
with open('pixivpy3/__init__.py', 'r') as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)
if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='PixivPy',
    packages=['pixivpy3'],
    version=version,
    description='Pixiv API for Python (with 6.x AppAPI supported)',
    long_description=io.open('README.md', mode='r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author='upbit',
    author_email='rmusique@gmail.com',
    install_requires=requires,
    url='https://github.com/upbit/pixivpy',
    download_url='https://github.com/upbit/pixivpy/releases',
    keywords=['pixiv', 'api', 'pixivpy'],
        classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
