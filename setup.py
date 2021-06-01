import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

REQUIREMENTS = [
    'pretty_tables == 1.*',
    'requests == 2.*',
]

DEV_REQUIREMENTS = [
    'coveralls == 3.*',
    'flake8',
    'mock == 4.*',
    'pytest == 6.*',
    'pytest-cov == 2.*',
]

setuptools.setup(
    name='homebrew-releaser',
    version='0.6.0',
    description='Release scripts, binaries, and executables directly to Homebrew via GitHub Actions.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/Justintime50/homebrew-releaser',
    author='Justintime50',
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIREMENTS,
    extras_require={
        'dev': DEV_REQUIREMENTS
    },
    entry_points={
        'console_scripts': [
            'homebrew-releaser=homebrew_releaser.releaser:main'
        ]
    },
    python_requires='>=3.6',
)
