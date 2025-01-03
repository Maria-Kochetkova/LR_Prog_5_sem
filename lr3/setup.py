import setuptools

setuptools.setup(
    name='OpenweatherApp',
    version='0.1',
    packages=setuptools.find_packages(),
    install_requires=['requests', 'json'],
    entry_points={'console_scripts': [
        'weather_app = weather_app.main:main'
    ]},
    author='MouseM',
    author_email='testingprog900@gmail.com',
    description='Приложение для получения данных с openweather посредством API ',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Maria-Kochetkova/LR_Prog_5_sem/tree/main/lr3',
    pyton_requires='>=3.6'
)
