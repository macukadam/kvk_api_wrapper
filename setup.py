import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kvk_api_client",
    version="0.0.1",
    author="Ugurcan Akpulat",
    description="Simple python wrapper for KVK api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["kvk_api_client"],
    package_dir={'': 'kvk/src'},
    install_requires=[
        'requests',
        'python-dotenv'
    ],)
