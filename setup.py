from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="qpassword_manager",
        version="0.3.0",
        author="ShiNoNeko47",
        author_email="nikola.brezovec.32123@gmail.com",
        packages=find_packages(),
        include_package_data=True,
        install_requires=[
            "cryptography",
            "pycryptodome",
            "pyperclip",
            "PyQt5",
            "requests",
        ],
        entry_points={
            "gui_scripts": [
                "qpassword_manager = qpassword_manager.__main__:main"
            ]
        },
    )
