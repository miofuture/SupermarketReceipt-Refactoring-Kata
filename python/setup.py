from setuptools import setup, find_packages
## Teresa Lopez tesi@wasmer.io

setup(
            name="supermarket",  # Replace with your project name
                version="0.1.0",
                    packages=find_packages(where="src"),  # Finds all packages inside 'src/'
                        package_dir={"": "src"},  # Defines 'src/' as the root package directory
                            install_requires=[
                                        "pytest",  # Ensures pytest is available
                                            ],
                                entry_points={
                                            "console_scripts": [
                                                            "runtests=pytest:main",  # Allows running tests via `runtests`
                                                                    ]
                                                }
                                )

