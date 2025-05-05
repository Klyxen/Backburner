from setuptools import setup, find_packages

setup(
    name="backburner",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "colorama>=0.4.6",
        "asyncio",
        "ipaddress",
    ],
    author="Klyxen",
    author_email="your-email@example.com",
    description="A fast, asynchronous port scanner with banner grabbing and risk highlighting",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Klyxen/Backburner",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "backburner = backburner.cli:main",
        ],
    },
    project_urls={
        "Bug Tracker": "https://github.com/Klyxen/Backburner/issues",
        "Source Code": "https://github.com/Klyxen/Backburner",
        "Documentation": "https://github.com/Klyxen/Backburner#readme",
    },
)
