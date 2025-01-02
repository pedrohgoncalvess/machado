from setuptools import setup, find_packages

setup(
    name="machado",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    package_data={
        'machado': ['templates/machado.conf'],
    },
    entry_points={
        'console_scripts': [
            'machado=machado.cli:main'
        ],
    },
)