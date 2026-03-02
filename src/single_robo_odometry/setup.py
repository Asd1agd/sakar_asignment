from setuptools import find_packages, setup

package_name = 'single_robo_odometry'

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
            'odometry_calculation = single_robo_odometry.odometry_calculation:main',
            'odom_tf_pub = single_robo_odometry.odom_tf_pub:main',
            'odometry_error = single_robo_odometry.odometry_error:main',
            'odom_tf_pub_w_error = single_robo_odometry.odom_tf_pub_w_error:main',
            'odom_tf_pub_inv = single_robo_odometry.odom_tf_pub_inv:main',
            'odom_tf_pub_w_error_inv = single_robo_odometry.odom_tf_pub_w_error_inv:main',
            'imu_republisher = single_robo_odometry.imu_republisher:main',
        ],
    },
)
