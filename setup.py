from setuptools import find_packages, setup

setup(
    name="obelisk-ai",
    version="1.0.0",
    description="Autonomous AI agent with computer vision, web automation, and complete system control.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Obelisk AI",
    author_email="contact@obelisk-ai.dev",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.31.0",
        "selenium>=4.15.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "pyautogui>=0.9.54",
        "pillow>=10.0.0",
    ],
    extras_require={
        "dev": ["black", "pytest", "flake8"],
        "full": [
            "numpy",
            "pandas",
            "openai",
            "anthropic",
            "tiktoken",
            "pytesseract",
        ]
    },
    entry_points={
        "console_scripts": [
            "obelisk=src.obelisk_agent:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="ai, automation, autonomous agent, ollama, llm, computer vision, web automation, gui automation",
    project_urls={
        "Documentation": "https://github.com/obelisk-ai/obelisk",
        "Source": "https://github.com/obelisk-ai/obelisk",
        "Bug Reports": "https://github.com/obelisk-ai/obelisk/issues",
    },
    python_requires=">=3.8",
)
