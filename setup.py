from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'UK Oil Terminals'
LONG_DESCRIPTION = 'Functions and modules related to data of UK oil terminals'

# Setting up
setup(
        name="UK-oil-terminals", 
        version=VERSION,
        author="Vardhan Raj Modi",
        author_email="vardhan609@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages()
)