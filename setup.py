import re

import setuptools


with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

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
    'bandit == 1.7.*',
    'black == 24.*',
    'flake8 == 7.*',
    'isort == 5.*',
    'mypy == 1.10.*',
    'pytest == 8.*',
    'pytest-cov == 5.*',
    'types-requests',
]

setuptools.setup(
    name='homebrew-releaser',
    version=version,
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
    python_requires='==3.12.*',
)
