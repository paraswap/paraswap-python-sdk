from setuptools import find_packages, setup

requirements_file = open("./requirements.txt")
requirements = requirements_file.readlines()
requirements_file.close()


setup(
    name="paraswap",
    packages=find_packages(
        include=["paraswap", "paraswap.abi", "paraswap.orders", "examples"]
    ),
    version="0.0.1",
    description="ParaSwap python sdk",
    author="Louis AMAS",
    license="MIT",
    install_requires=requirements,
    setup_requires=[""],
    tests_require=[""],
    test_suite="tests",
)
