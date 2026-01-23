from setuptools import find_packages, setup
from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'quadrotor_sim'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('src/launch/*')), # Changed
        (os.path.join('share', package_name, 'model'), glob('src/models/*')), # Changed
        (os.path.join('share', package_name, 'parameters'), glob('src/parameters/*')), # Changed
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ky_ode',
    maintainer_email='ky_ode@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'position_controller = src.controllers.position_controller:main', # Changed
            'data_plotter = src.plotters.data_plotter:main', # Changed
        ],
    },
)
