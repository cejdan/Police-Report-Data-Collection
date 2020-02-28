from setuptools import setup, find_packages

setup(
            name = "project0",
            version = "1.0",
            author = "Nicholas Cejda",
            author_email = "ncejda@gmail.com"
            packages = find_packages(exclude = ('tests', 'docs')),
            tests_require = ['pytest']
            )
