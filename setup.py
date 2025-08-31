#!/usr/bin/env python3
"""
Setup script for Network Security Assessment Framework (NSAF)
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
try:
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
except FileNotFoundError:
    requirements = [
        'nmap-python>=1.5.4',
        'python-nmap>=0.7.1',
        'scapy>=2.5.0',
        'requests>=2.31.0',
        'beautifulsoup4>=4.12.2',
        'jinja2>=3.1.2',
        'pyyaml>=6.0.1',
        'colorama>=0.4.6',
        'rich>=13.7.0',
        'click>=8.1.7',
        'reportlab>=4.0.7',
        'matplotlib>=3.8.2',
        'pandas>=2.1.4',
        'netifaces>=0.11.0',
        'dnspython>=2.4.2',
        'cryptography>=41.0.8',
        'paramiko>=3.4.0',
        'validators>=0.22.0'
    ]

setup(
    name="nsaf",
    version="1.0.0",
    author="NSAF Development Team",
    author_email="contact@nsaf.security",
    description="A comprehensive network security assessment framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/network-security-assessment-framework",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/network-security-assessment-framework/issues",
        "Documentation": "https://yourusername.github.io/network-security-assessment-framework/",
        "Source": "https://github.com/yourusername/network-security-assessment-framework",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=22.0.0',
            'flake8>=5.0.0',
            'mypy>=1.0.0',
            'isort>=5.10.0',
        ],
        'docs': [
            'sphinx>=5.0.0',
            'sphinx-rtd-theme>=1.0.0',
            'myst-parser>=0.18.0',
        ],
        'all': [
            'shodan>=1.30.0',
            'nmap',
        ]
    },
    entry_points={
        "console_scripts": [
            "nsaf=nsaf_cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        'nsaf': [
            'templates/*.html',
            'templates/*.css', 
            'templates/*.js',
        ],
    },
    keywords=[
        "security", "network", "scanning", "vulnerability", "assessment",
        "penetration testing", "cybersecurity", "infosec", "networking"
    ],
    zip_safe=False,
)
