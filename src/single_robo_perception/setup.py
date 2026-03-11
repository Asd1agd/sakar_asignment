from setuptools import find_packages, setup

package_name = 'single_robo_perception'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='asd',
    maintainer_email='a93054223@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_feed = single_robo_perception.camera_feed:main',
            'camera_feed_old = single_robo_perception.camera_feed_old:main',
            'camera_feed_edit = single_robo_perception.camera_feed_edit:main',
            'rviz_point_visualiser = single_robo_perception.rviz_point_visualiser:main',
        ],
    },
)
