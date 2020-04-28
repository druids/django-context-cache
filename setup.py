from setuptools import setup, find_packages


setup(
    name='django-context-cache',
    version='0.0.1',
    description="Django context cache library.",
    keywords='django, cache, request cache',
    author='Lubos Matl',
    author_email='matllubos@gmail.com',
    url='https://github.com/druids/django-context-cache',
    license='MIT',
    package_dir={'context_cache': 'context_cache'},
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Czech',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
    install_requires=[
        'django>=2.0',
    ],
    zip_safe=False
)
