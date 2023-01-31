import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()

REQUIREMENTS = [
    'chevron == 0.14.*',
    'pretty-tables == 2.*',
    'requests == 2.*',
    'woodchips == 0.2.*',
]

DEV_REQUIREMENTS = [
    'bandit == 1.7.*',
    'black == 22.*',
    'build == 0.10.*',
    'flake8 == 6.*',
    'isort == 5.*',
    'mypy == 0.991',
    'pytest == 7.*',
    'pytest-cov == 4.*',
    'twine == 4.*',
    'types-requests',
]

setuptools.setup(
    name='homebrew-releaser',
    version='0.14.3',
    description='Release scripts, binaries, and executables directly to Homebrew via GitHub Actions.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/Justintime50/homebrew-releaser',
    author='Justintime50',
    license='MIT',
    packages=setuptools.find_packages(
        exclude=[
            'examples',
            'test',
        ]
    ),
    package_data={
        'homebrew_releaser': [
            'py.typed',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIREMENTS,
    extras_require={
        'dev': DEV_REQUIREMENTS,
    },
    entry_points={
        'console_scripts': [
            'homebrew-releaser=homebrew_releaser.releaser:main',
        ]
    },
    python_requires='==3.11',
)
