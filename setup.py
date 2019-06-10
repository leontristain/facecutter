from setuptools import setup, find_packages

setup(name='facecutter',
      packages=find_packages(exclude=['test']),
      version='0.1.0',
      description='facecutter',
      author='leontristain',
      keywords=[],
      classifiers=[],
      setup_requires=[],
      install_requires=['click>=7.0'],
      tests_require=['pytest==4.3.0'],
      test_suite='test',
      entry_points='''
          [console_scripts]
          facecutter=facecutter.cli.facecutter:cli
      ''')
