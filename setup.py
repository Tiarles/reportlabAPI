from setuptools import setup, find_packages

setup(
    name='reportlabAPI',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["pdfrw", "reportlab", "numpy", "pandas", "matplotlib"],
    package_data = {"": ['fonts/*.ttf', 'logo1.png']}
)
