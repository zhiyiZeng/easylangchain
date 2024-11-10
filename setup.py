from setuptools import setup, find_packages

setup(
    name="easylangchain",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain-community",
        "langchain-core",
        "langchain-openai",
    ],
    author="zengzhiyi",
    author_email="1694609389@qq.com",
    description="A simplified wrapper around LangChain for easy tool usage",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zengzhiyi/easylangchain", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
