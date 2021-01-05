import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIREMENTS = [
    'requests >= 1.0.0'
]

setuptools.setup(
    name='homebrew-releaser',
    version='0.2.1',
    description='Release scripts, binaries, and executables directly to Homebrew via GitHub Actions.',  # noqa
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
        'dev': [
            'pytest >= 6.0.0',
            'pytest-cov >= 2.10.0',
            'coveralls >= 2.1.2',
            'flake8 >= 3.8.0',
            'mock >= 4.0.0',
        ]
    },
    entry_points={
        'console_scripts': [
            'homebrew-releaser=homebrew_releaser.releaser:main'
        ]
    },
    python_requires='>=3.6',
)
