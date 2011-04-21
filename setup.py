from setuptools import setup, find_packages

setup(
    name='django-newsletter',
    version=__import__('newsletter').__version__,
    license="BSD",

    install_requires = ['django-markup-mixin','django-extensions',],

    description='A simple reusable application for managing newsletters in a Django application.',
    long_description=open('README.rst').read(),

    author='Colin Powell',
    author_email='colin@onecardinal.com',

    url='http://github.com/powellc/django-newsletter',
    download_url='http://github.com/powellc/django-newsletter/downloads',

    include_package_data=True,

    packages=['newsletter'],

    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
