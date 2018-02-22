from setuptools import setup, find_packages

with open('README.org') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name="pys3viewer",
    version="0.1.0",
    description="pys3viewer Django REST service",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Flask>=0.12",
                      "Click>=6.0",
                      "BrokenPackage>=0.7,<=1.0"],
    extras_require={
        "test": [
            "colorama>=0.3.3",
            "coverage>=4.0.3",
            "django-nose>=1.4.2",
            "nose>=1.3.7",
            "pinocchio>=0.4.2"
        ]
    }
)
