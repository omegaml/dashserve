import os

from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

dev_deps = ['pytest', 'twine']

setup(
    name='dashserve',
    version='0.1.7',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',  # example license
    description='develop and serve Plotly Dash apps in Jupyter Notebook',
    long_description=README,
    url='https://omegaml.github.io/dashserve/',
    author='Patrick Senti',
    author_email='patrick.senti@omegaml.io',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Database :: Front-Ends',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Widget Sets'
    ],
    install_requires=[
        'dash>=1.0',
        'dash-daq>=0.1.0',
        'dill>=0.3.2,<0.3.6', # due to issue https://github.com/uqfoundation/dill/issues/332
        'requests',
    ],
    extras_require={
        'dev': dev_deps,
    },
)
