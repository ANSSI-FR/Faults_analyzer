.. This is A COPY OF the main index.rst file which is rendered into the landing page of your documentation.
   Follow the inline instructions to configure this for YOUR next project.



Fault Analyzer Documentation
=========================================================
|

Put here some introduction to your project.

.. The source code is available `here <https://github.com/usrname/projectname>`_.

|

.. maxdepth = 1 means the Table of Contents will only links to the separate pages of the documentation.
   Increasing this number will result in deeper links to subtitles etc.

.. Below is the main Table Of Content
   You have below a "dummy" file, that holds a template for a class.
   To add pages to your documentation:
        * Make a file_name.rst file that follows one of the templates in this project
        * Add its name here to this TOC

.. toctree::
   :maxdepth: 1
   :name: projtoc
   :caption: Fault Analyzer

   introduction
   get_started
   architecture
   contribute

.. toctree::
   :maxdepth: 1
   :name: mastertoc
   :caption: Modules

   analyzer
   bin_utils
   carto_analyzer
   manip_info_formater
   manip
   manips_manager
   plot_manager
   prompt
   results_manager
   results
   utils

.. Delete this line until the * to generate index for your project: * :ref:`genindex`


|

This documentation was last updated on |today|.

.. Finished personalizing all the relevant details? Great! Now make this your main index.rst,
   And run `make clean html` from your documentation folder :)
