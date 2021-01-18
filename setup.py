from setuptools import setup

setup(
    name='Dataset-Downloader-Tool',
    version='1.0',
    packages=[
        'src'
    ],
    install_requires=[
        'requests',
        'tqdm',
        'paramiko'
    ],
     
    entry_points={
        'console_scripts': [
            'downloadtool = src.run:main',
        ],
    },
    python_requires='>=3.6'
)