import re
from distutils.core import setup

requires = ['requests']

version = ''
with open('pixivpy3/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)
if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='PixivPy',
    packages=['pixivpy3'],
    version=version,
    description='Pixiv API for Python',
    author='upbit',
    author_email='rmusique@gmail.com',
    install_requires=requires,
    url='https://github.com/upbit/pixivpy',
    download_url='https://github.com/upbit/pixivpy/releases',
    keywords=['pixiv', 'api', 'pixivpy'],
    classifiers=[],
)
