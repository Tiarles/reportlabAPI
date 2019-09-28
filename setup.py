from setuptools import setup, find_packages

setup(
   name='reportlabAPI',
   packages=find_packages(where="src"),
   package_dir={"": "src"},
   install_requires=["pdfrw", "reportlab"],
   include_package_data=True,
   package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.ttf']}
)
