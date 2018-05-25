Read the Docs Basics
======================

What is Read the Docs?
----------------------
`Read the Docs <http://docs.readthedocs.io/en/latest/index.html>`_ simplifies
software documentation by automating building,versioning, and hosting of your
docs for you. We use it to keep the PiCar documentation organized
and updated. If you make a significant change to the PiCar repository or
project, you are recommended
to update the Read the Docs documentation for PiCar.
It uses `reStructuredText <http://docutils.sourceforge.net/rst.html>`_ file
format to build the HTML files using `Sphinx
<http://www.sphinx-doc.org/en/master/>`_.

How to update the Docs?
-----------------------
1. Fork and clone the `PiCar Github repository
   <https://github.com/xz-group/PiCar>`_
2. Navigate to the ``../readthedocs`` directory:

   .. code-block:: bash

     cd PiCar/docs/readthedocs

3. The documentation is currently ordered as the following:

   ::

     index.rst
     conf.py
     chapters/
       introduction.rst
       tutorials.rst
       usage.rst
       tutorials/
         raspberry_pi_tutorial.rst
         arduino_tutorial.rst
         github_tutorial.rst
         linux_tutorial.rst
         readthedocs_tutorial.rst
       usage/
         mechanical
         electronics
         software
       changelogs.rst
       contributors.rst

4. It is recommended to use a comprehensive text editor like Atom or Sublime
   text. Atom can be installed by:

   .. code-block:: bash

     sudo add-apt-repository ppa:webupd8team/atom
     sudo apt-get update
     sudo apt-get install atom

   * Atom can be launched in the ``../readthedocs`` directory by:

   .. code-block:: bash

     atom .

.. note:: For more information on the different commands available
          for .rst type files, check out the `Rest and Sphinx memo
          <http://rest-sphinx-memo.readthedocs.io/en/latest/ReST.html>`_.

5. After making a change in an .rst , go back to ../readthedocs
   and enter the command to build the html pages:

   .. code-block:: bash

      make html

6. To preview the changes, navigate to ``../readthedocs/_build/html``
   and open ``index.html`` in a browser.

.. note:: The PiCar Read the Docs is using the ``sphinx_rtd_theme`` theme.
          This can be change in the ``../readthedocs/conf.y`` file. The version
          number, project name, authors, language support can be changed here
          too.

.. warning:: ReadtheDocs is very strict with indentation and formating. Check
             warning messages (with the associated line number) to fix issues.

7. Once you have made changes without errors and warnings and are satisfied
   with the updated documentation, submit a pull request to the latest Github
   branch.

.. warning:: You have to run ``make html`` and check the HTML output before
             pushing your changes, otherwise the expected HTML changes will not
             be rendered.

.. note:: If you want to create readthedocs style documentation for an entirely
          new repository, or you want to test and see how the HTML pages looks
          online, you will need to create a `readthedocs
          <https://readthedocs.org/>`_ account (either import your GitHub
          account or create a new one), and import that specific repository.
          This ensures that when new commits are submitted, the docs are
          updated automatically as well.

Resources
---------
- `Rest and Sphinx Memo <http://rest-sphinx-memo.readthedocs.io/en/latest/ReST.html>`_
