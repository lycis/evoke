from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='evoke',
      version='0.0.1',
      description='evoke is a tool to store, share and run code snippets and evoke their power from anywhere.',
      long_description=readme(),
      url='http://github.com/lycis/evoke',
      author='Daniel Eder',
      author_email='daniel@deder.at',
      license='GPL 3.0',
      packages=['evoke'],
      install_requires=[
        'argparse'
      ],
      entry_points={
          'console_scripts': [
              'evoke=evoke.main:main',
          ]
      },
      classifiers=[
          'Development Status :: 1 - Planning',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Information Technology',
          'Intended Audience :: System Administrators',
          'Programming Language :: Python :: 3.5',
          'Topic :: Utilities'
      ])