
from setuptools import setup

setup(
    name='twentyc.tools',
    version='0.1',
    author='Twentieth Century',
    author_email='code@20c.com',
    description='various python tool libraries / helpers',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['twentyc.tools'],
    install_requires=open("requirements.txt").read().split("\n"),
    namespace_packages=['twentyc'],
    zip_safe=False
)