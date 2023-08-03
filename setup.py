from setuptools import setup
from setuptools import find_namespace_packages

setup(
    include_package_data=True,
    name='AutoPart-text-classifiers',
    version='1.0.0',
    author='Florian Runkel',
    author_email='f.runkel@yahoo.com',
    description=' Classifier zur Klassifikation von Unternehmen ',
    packages=find_namespace_packages(),

    # Here is the URL where you can find the code
    url='https://github.com/FloRunkel/AutoPart-text-classifiers/tree/main/src',

    install_requires=[
        'scikit-learn',
        'simpletransformers==0.63.11',
        'selenium',
        'webdriver_manager',
        'bs4',
        'pandas',
        'urllib3',
        'requests',
        'wikipedia-api',
        'sentence_transformers',
        'matplotlib',
        'sklearn',
        'spacy',
        'flair',
        'transformers==4.31.0',
    ],

    python_requires='>=3.7',

    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Topic :: Textklassifikation',
    ]
)
