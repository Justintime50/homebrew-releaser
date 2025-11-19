import re

import setuptools


# Inspiration: https://stackoverflow.com/a/7071358/6064135
with open('homebrew_releaser/_version.py', 'r') as version_file:
    version_groups = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_groups:
        version = version_groups.group(1)
    else:
        raise RuntimeError('Unable to find version string!')

REQUIREMENTS = [
    'chevron == 0.14.*',
    'pretty-tables == 2.*',
    'requests == 2.*',
    'woodchips == 1.*',
]

DEV_REQUIREMENTS = [
    'bandit == 1.8.*',
    'black == 25.*',
    'flake8 == 7.*',
    'isort == 7.*',
    'mypy == 1.18.*',
    'pytest == 8.*',
    'pytest-cov == 7.*',
]

setuptools.setup(
    name='homebrew-releaser',
    version=version,
    description='Release scripts, binaries, and executables directly to Homebrew via GitHub Actions.',
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
    python_requires='==3.13.*',
)
