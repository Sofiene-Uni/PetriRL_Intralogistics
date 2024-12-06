from setuptools import setup, find_packages

# Load README.md for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="petrirl",
    version="0.1.0",
    author="Sofiene Lassoued",
    author_email="lassoued.sofiene@fh-swf.de",
    description="PetriRL : Flexible manufacturing systems with Petri Nets and Reinforcement learning dynamic version",
    long_description=long_description ,
    long_description_content_type="text/markdown",
    install_requires=["gymnasium", "pandas", "numpy"],
    packages=find_packages(),
    package_data={
        'ptrl': [
            'callbacks/*',
            'common/*',
            'common/instances/**/*',
            'envs/fms/*',
            'render/*',  
            'utils/*',
        ],
    },
    url="https://www.fh-swf.de/de/forschung___transfer_4/labore_3/labs/labor_fuer_automatisierungstechnik__soest_1/standardseite_57.php",
    project_urls={
        "Documentation": "https://www.researchgate.net/publication/386198263_Flexible_Manufacturing_Systems_Intralogistics_Dynamic_Optimization_of_AGVs_and_Tool_Sharing_Using_Coloured-Timed_Petri_Nets_and_Actor-Critic_RL_with_Actions_Masking",
        "Repository": "https://github.com/Sofiene-Uni/Intralogistics"
    },
)