import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

REQUIREMENTS = [
    'pretty_tables == 2.*',
    'requests == 2.*',
    'woodchips == 0.2.*',
]

DEV_REQUIREMENTS = [
    'black',
    'coveralls == 3.*',
    'flake8',
    'isort',
    'mypy',
    'pytest == 6.*',
    'pytest-cov == 2.*',
    'types-requests',
]

setuptools.setup(
    name='homebrew-releaser',
    version='0.9.2',
    description='Release scripts, binaries, and executables directly to Homebrew via GitHub Actions.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/Justintime50/homebrew-releaser',
    author='Justintime50',
    license='MIT',
    packages=setuptools.find_packages(),
    package_data={'homebrew_releaser': ['py.typed']},
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
    python_requires='>=3.7, <4',
)
