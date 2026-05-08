from setuptools import setup, find_packages

# Read requirements safely
def get_requirements(file_path: str):
    with open(file_path) as file:
        requirements = file.read().splitlines()

        # Remove empty lines and comments
        requirements = [
            req.strip() for req in requirements
            if req.strip() and not req.startswith("#")
        ]

        return requirements


setup(
    name="customer_churn_prediction",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="End-to-End Customer Churn Prediction ML System",
    long_description="A production-grade machine learning system to predict telecom customer churn using scikit-learn, Flask, and FastAPI.",
    long_description_content_type="text/plain",

    # Package discovery
    packages=find_packages(),

    # Dependencies
    install_requires=get_requirements("requirements.txt"),

    # Python version requirement
    python_requires=">=3.8",

    # Entry points (optional but useful)
    entry_points={
        "console_scripts": [
            "train_pipeline=scripts.train_pipeline:main",
        ],
    },

    # Additional metadata
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
