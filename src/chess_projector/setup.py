from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'chess_projector'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.json')),
    ],
    install_requires=['setuptools', 'pygame', 'numpy'],
    zip_safe=True,
    maintainer='Fiona',
    maintainer_email='fkprendergast@wpi.edu',
    description='Projects chess piece movement hints onto a physical chess board',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'projector_node = chess_projector.projector_node:main',
            'combined_node = chess_projector.combined_node:main',
        ],
    },
)
