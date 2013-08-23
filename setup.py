# coding: utf-8

from distutils.core import setup


setup(name='strobo',
      version='0.1.1',
      author=u'Álvaro Justen',
      author_email='alvarojusten@gmail.com',
      url='https://github.com/turicas/strobo/',
      description='Create slideshows from images programatically with Python',
      py_modules=['strobo'],
      install_requires=['pil'],
      license='GPL',
      keywords=['slideshow', 'video'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
)
