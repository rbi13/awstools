from setuptools import setup

setup(name='awstools',
      version='0.1',
      description='various scripts for managing aws deployments',
      url='http://github.com/rbi13/awstools',
      author='rbi13',
      license='MIT',
      packages=['awstools'],
      install_requires=[
          'boto3',
          'argparse'
      ],
      entry_points={
          'console_scripts': [
              'awstools = awstools.__main__:main'
          ]
      },
      zip_safe=False)
