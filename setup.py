from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="cpsvis",
    version="0.0.22",
    description="Convex Projective Surface Visualisation Tool",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sepehrsaryazdi/cpsvis",
    author="Sepehr Saryazdi",
    author_email="sepehr.saryazdi@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy >= 1.21.5", "matplotlib >= 3.5.2"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.8",
)