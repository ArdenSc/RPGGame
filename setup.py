from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="RPGGame",
      version="0.0.1",
      author="Arden Sinclair",
      description="A terminal roleplay game",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/ArdenSinclair/RPGGame",
      packages=find_packages(),
      classifiers=[
          "Development Status :: 1 - Planning",
          "Environment :: Console",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3.8",
          "Typing :: Typed",
      ],
      python_requires=">=3.6")
