from setuptools import setup

setup(
    name='ShV',
    version='1',
    description='Sort folder',
    url='https://github.com/shv833',
    author='https://github.com/shv833',
    author_email='shyra.volodymyr.833@gmail.com',
    license='MIT',
    entry_points={'console_scripts': ['cli_sort = cli_sort.sort:main']}
)