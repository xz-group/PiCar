GitHub Basics
=============

What is GitHub?
---------------
`GitHub <https://github.com/>`_ is a code hosting platform for version control,
backups and collaboration. It lets you and others work together on projects
from anywhere.

Getting Started
----------------
Procedure
^^^^^^^^^
1. If you haven't already, create a `GitHub <https://github.com/>`_ account.
2. On a browser, navigate to the `PiCar GitHub Repository
   <https://github.com/xz-group/PiCar>`_
3. ``Fork`` the repo to create a copy of the master PiCar repo on your account.
4. Under your repositories navigate to your version of the PiCar repo.
5. ``Clone`` (download) the repo to your computer

   Windows
    * Download and install `GitHub Desktop <https://desktop.github.com/>`_
    * Login to your GitHub account

   Linux / Mac
    * Copy the cloning link from your forked repo.
    * Install Git:

    .. code-block:: bash

       sudo apt-get install git

    * Make a new directory and navigate to it:

    .. code-block:: bash

       mkdir projects/github
       cd projects/github

    * Clone the repo (replace ``<username>`` with your GitHub username)

    .. code-block:: bash

       git clone https://github.com/<username>/PiCar.git

6. Once you have made changes to the code or documentation, you need to commit
   the changes to the remote repo.

   Windows
     * `GitHub Desktop` will automatically track changes you have made to the
       local repo.
     * Click on the ``pull`` repository icon to update your local branch with
       the remote branch
     * Enter a commit message and hit the ``Commit`` button
     * Click on the ``push`` repository icon to update the remote branch with
       your local branch

   Linux / MacOS
     * Inside the PiCar repository, using terminal:

     .. code-block:: bash

        git pull
        git add *
        git commit -m "your message here"

     * ``git pull`` updates your local repo with the remote repo
     * ``git add *`` checks your local repo for changes and aggregates them
       for commits
     * ``git commit`` saves the new version and has a unique hash identifier
     * If you want to find that hash, you can use ``git rev-parse --short
       HEAD`` to fetch it.

  .. note:: It is helpful to leave useful commit messages so that other
            contributors can see what you have done.

7. Push your changes to the master branch of your forked repo.

   .. code-block:: bash

      git push

   * It will prompt you for your username and password, enter them.

8. Once the local changes have been pushed to remote successfully, go back to
   the original `Picar GitHub Repository <https://github.com/xz-group/PiCar>`_.
9. Click on ``Pull Requests`` >> ``New Pull Request`` >> ``Compare against
   forks``
10. The base fork should be ``xz-group/PiCar``; change the headfork to
    ``<username>/PiCar``
11. You can see what changes (additions and deletions) will be created with
    the Pull Request. Add a title and a short description and submit the Pull
    Request.
12. If you are a direct contributor on the main repo, you can navigate to
    `Picar GitHub Repository <https://github.com/xz-group/PiCar>`_
    >> ``Pull Requests`` >> ``Merge Pull Request`` as long as there are
    no conflicts. If you're not a direct contributor, you will need to
    wait until your Pull Request is merged with the master branch.

.. note:: Google and `StackOverflow <https://stackoverflow.com/>`_ are your
          friends. Use them when you run into an issue with git (merge
          conflicts, etc.).

Resources
---------
- `GitHub Guide <https://guides.github.com/activities/hello-world/>`_
- `Forking repositories <https://help.github.com/articles/fork-a-repo/>`_
- `Syncing a fork <https://stackoverflow.com/a/19506355>`_
- `Pushing to remote <https://help.github.com/articles/pushing-to-a-remote/#pushing-a-branch>`_
- `Do not be afraid to commit <http://dont-be-afraid-to-commit.readthedocs.io>`_
