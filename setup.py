from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="Hero of the Village",
      version="1.0.0",
      author="Arden Sinclair",
      description="A terminal roleplay game",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/ArdenSinclair/RPGGame",
      install_requires=[
          "typing_extensions",
      ],
      packages=find_packages(),
      classifiers=[
          "Development Status :: 2 - Pre-Alpha",
          "Environment :: Console",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3.7",
          "Typing :: Typed",
      ],
      python_requires=">=3.7")
