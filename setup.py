from setuptools import find_packages, setup


setup(
    name="tribev2",
    version="0.1.0",
    description="Deep multimodal brain encoding",
    packages=find_packages(include=["tribev2", "tribev2.*"]),
)
