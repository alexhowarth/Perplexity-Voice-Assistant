from setuptools import setup, find_packages

setup(
    name="perplexity-voice-assistant",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here, or use requirements.txt
    ],
    entry_points={
        "console_scripts": [
            "perplexity-voice-assistant=perplexity_voice_assistant.perplexity_voice_assistant:main",
        ],
    },
    author="Alex Howarth",
    author_email="alex.howarth@gmail.com",
    description="A voice assistant powered by Perplexity AI.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/alexhowarth/Perplexity-Voice-Assistant",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)