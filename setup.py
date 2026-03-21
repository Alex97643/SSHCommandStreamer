from setuptools import setup, find_packages

setup(
    name="sshcommandstreamer",
    version="1.0.0",
    description="SSH command streamer with real-time output and file upload support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    packages=find_packages(),
    install_requires=["paramiko"],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
