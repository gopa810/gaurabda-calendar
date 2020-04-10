from distutils.core import setup
setup(
  name = 'gaurabda',         # How you named your package folder (MyLib)
  packages = ['gaurabda', 'gaurabda.GCEnums'],   # Chose the same as "name"
  include_package_data = True,
  package_data = {'gaurabda': ['res/*.*']},
  version = '0.7.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Calculation of Gaurabda calendar (Gaudiya Vaishnava calendar)',   # Give a short description about your library
  author = 'Gopal',                   # Type in your name
  author_email = 'root@gopal.home.sk',      # Type in your E-Mail
  url = 'https://github.com/gopa810/gaurabda',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/gopa810/gaurabda-calendar/archive/0.7.3.tar.gz',    # I explain this later on
  keywords = ['gaurabda', 'vaisnava', 'vaishnava', 'ISKCON', 'GCAL'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
