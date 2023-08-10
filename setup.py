import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="kvk_api_client",
    version="0.0.6",
    author="Ugurcan Akpulat",
    description="Simple python wrapper for KVK api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['kvk_api_client'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest==7.2.1",
            "pytest-asyncio==0.21.1"
        ]
    }
)

