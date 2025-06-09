from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mektabati",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive library management system built with Flask",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mektabati",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Flask",
        "Topic :: Education",
        "Topic :: Database",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "mektabati=app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "mektabati": [
            "templates/*.html",
            "static/css/*.css",
            "static/js/*.js",
        ],
    },
)
