from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'quadrotor_sim'

setup(
    name=package_name,
    version='0.0.0',
    # We look for packages directly in the current folder (src)
    packages=find_packages(), 
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # These paths are now relative to where setup.py is (inside src/)
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'model'), glob('models/*')),
        (os.path.join('share', package_name, 'parameters'), glob('parameters/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Student',
    maintainer_email='student@example.com',
    description='Quadrotor Simulation',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'position_controller = controllers.position_controller:main',
            'data_plotter = plotters.data_plotter:main',
        ],
    },
)