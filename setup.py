from setuptools import setup
from setuptools import find_packages

setup(
    name='pystoi',
    version='0.2.0',
    description='Computes Short Term Objective Intelligibility measure',
    author='Manuel Pariente',
    author_email='pariente.mnl@gmail.com',
    url='https://github.com/mpariente/pystoi',
    license='MIT',
    install_requires=['numpy', 'scipy', 'resampy'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ],
    packages=find_packages()
)
