import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aaaai",
    version="0.1.2",
    author="Mahdi Nouri",
    author_email="algo.mahdi.nouri@gmail.com",
    description="all agents and AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/algonouir/aaaai",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "annotated-types==0.7.0",
        "anyio==4.9.0",
        "certifi==2025.7.14",
        "charset-normalizer==3.4.2",
        "greenlet==3.2.3",
        "h11==0.16.0",
        "httpcore==1.0.9",
        "httpx==0.28.1",
        "idna==3.10",
        "jsonpatch==1.33",
        "jsonpointer==3.0.0",
        "langchain==0.3.26",
        "langchain-core==0.3.69",
        "langchain-ollama==0.3.4",
        "langchain-text-splitters==0.3.8",
        "langsmith==0.4.6",
        "ollama==0.5.1",
        "orjson==3.11.0",
        "packaging==25.0",
        "pydantic==2.11.7",
        "pydantic_core==2.33.2",
        "PyYAML==6.0.2",
        "requests==2.32.4",
        "requests-toolbelt==1.0.0",
        "sniffio==1.3.1",
        "SQLAlchemy==2.0.41",
        "tenacity==9.1.2",
        "typing-inspection==0.4.1",
        "typing_extensions==4.14.1",
        "urllib3==2.5.0",
        "zstandard==0.23.0",
    ]
)