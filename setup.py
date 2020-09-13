from setuptools import find_packages, setup

setup(
      name='robotframework-historic',
      version="0.2.2",
      description='Custom report to display robotframework historical execution records',
      long_description='Robotframework Historic is custom report to display historical execution records using MySQL + Flask',
      classifiers=[
          'Framework :: Robot Framework',
          'Programming Language :: Python',
          'Topic :: Software Development :: Testing',
      ],
      keywords='robotframework historical execution report',
      author='Shiva Prasad Adirala',
      author_email='adiralashiva8@gmail.com',
      url='https://github.com/adiralashiva8/robotframework-historic',
      license='MIT',

      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,

      install_requires=[
          'robotframework',
          'config',
          'flask',
          'flask-mysqldb'
      ],
      entry_points={
          'console_scripts': [
              'rfhistoric=robotframework_historic.app:main',
              'rfhistoricparser=robotframework_historic.runner:main',
          ]
      },
)