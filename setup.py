from setuptools import setup, find_packages

setup(
    name='my_package',
    version='0.1.0',
    author='Your Name',
    author_email='harshchudasama4739s@gmail.com',
    install_requires=["google-generativeai","langchain","streamlit","python-dotenv","pyPDF2"],
    packages=find_packages()
)