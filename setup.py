import setuptools

current_version = "0.8.2"

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='gaurabda',
    version=current_version,
    author="Gopal",
    author_email="root@gopal.home.sk",
    license="MIT",
    description="Calculation of Gaurabda calendar (Gaudiya Vaishnava calendar)",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/gopa810/gaurabda-calendar",
    download_url='https://github.com/gopa810/gaurabda-calendar/archive/' + current_version + '.tar.gz',
    keywords=['gaurabda', 'vaisnava', 'vaishnava', 'ISKCON', 'GCAL'],
    packages=setuptools.find_packages(),
    package_data={'gaurabda': ['res/*.*']},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Topic :: Software Development :: Build Tools',
    ],
    python_requires='>=3.4',
)
