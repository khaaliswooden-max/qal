from setuptools import setup, find_packages

setup(
    name="qawm",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "pymc>=5.0.0",
        "networkx>=3.0",
        "neo4j>=5.0.0",
        "psycopg2-binary>=2.9.0",
        "pymongo>=4.3.0",
        "pandas>=2.0.0",
        "plotly>=5.14.0",
        "pydantic>=2.0.0",
        "fastapi>=0.95.0",
    ],
    author="Antigravity",
    description="Quantum Archeological World Model",
)
