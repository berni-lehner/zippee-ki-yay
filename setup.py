import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='zippeekiyay',
    version='0.1.1',
    author='Bernhard Lehner',
    author_email='berni.lehner@gmail.com',
    description='Python interfaces to extract the namelist from a zip archive without the need to download it first.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/berni-lehner/zippee-ki-yay',
    project_urls = {
        "Bug Tracker": "https://github.com/berni-lehner/zippee-ki-yay/issues"
    },
    license='Apache 2.0',
    packages=['zippeekiyay'],
    install_requires=[],
    package_dir={'src'}
)