import setuptools


setuptools.setup(
    name="ssa-datastore",
    description="Datastore for SSA-related data with a RESTful API",
    version="0.1.0",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    # package_data={
    #     "": ["default.config"],
    #     "external_data": ["*"],
    #     "example_data": ["*"],
    # },
    entry_points={
        'console_scripts': [
            'ssa-server=datastore.run:startApp',
            'ssa-migrate=datastore.db_migrate:performMigrate',
        ]
    }
)
