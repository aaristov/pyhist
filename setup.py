from setuptools import setup

setup(
    name='pyhist',
    version='0.1.1',
    packages=['pyhist'],
    install_requires=[
        'scikit-image',
        'numpy',
        'scipy',
        'matplotlib',
        'read-roi',
        'pandas'
    ],
    url='https://github.com/aaristov/py-hist.git',
    license='MIT',
    author='Andrey Aristov',
    author_email='aaristov@pasteur.fr',
    description='Plot localization histograms'
)
