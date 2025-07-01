from setuptools import setup, find_packages

setup(
    name="api-project",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "Flask==2.0.1",
        "Werkzeug==2.0.3",
        "requests==2.26.0",
        "pytest==6.2.5",
        "locust==2.8.6",
        "pytest-mock==3.6.1"
    ],
)