from setuptools import setup, find_packages
setup(name='adminq',
      version='0.3',
      packages= find_packages(),
      install_requires=[
          'celery',
          'pymongo',
      ],
      include_package_data=True,
)
