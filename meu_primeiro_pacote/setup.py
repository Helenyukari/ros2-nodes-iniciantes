from setuptools import find_packages, setup

package_name = 'meu_primeiro_pacote'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='helen',
    maintainer_email='helen@todo.todo',
    description='Primeiro pacote ROS2 - Publisher e Subscriber basicos',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'publisher = meu_primeiro_pacote.publisher:main',
            'subscriber = meu_primeiro_pacote.subscriber:main',
            'random_publisher = meu_primeiro_pacote.random_publisher:main',
            'number_classifier = meu_primeiro_pacote.number_classifier:main',
        ],
    },
)
