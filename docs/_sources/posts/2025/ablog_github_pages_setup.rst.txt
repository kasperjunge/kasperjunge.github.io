
.. post:: Feb 14, 2025
   :tags: Guides
   :author: Kasper Junge

How to Setup ablog for GitHub Pages
========================================

*This blog post will show you have to create a free blog hosted on GitHub Pages using the Python documentation generator Sphinx and the ablog extension.*

I recently became interested in writing code documentation (who doesn't get excited about that?).

I tried to figure out how what the big Python projects used for writing their documentation, and I found out that a lot of them use Sphinx.

I started reading the `Getting Started guide on the Sphinx website <https://www.sphinx-doc.org/en/master/usage/quickstart.html>`_, and I there was a line in the intro that I couldn't get out of my head:


*"Sphinx focuses on documentation, in particular handwritten documentation, however, Sphinx can also be used to generate blogs, homepages and even books."*

For some time I have been using posthaven for my blog (mostly because I'm a Sam Altman wannabe).

But recently I have become a Simon Willison wannabe also, and wanted to create an oldschool selfhosted blog like him for a while.

Step 1: Create GitHub repository for your blog
----------------------------------------------
Create a new repository on GitHub named <username>.github.io. This will be the repository where your blog will be hosted.

When you have create the repository, clone it to your local machine:

.. code-block:: bash
    
   git clone git@github.com:<username>./<username>..github.io.git

Step 2: Setup Python environment with uv
-----------------------------------------
Next step is to create a Python environment for your blog. 

We will use uv to manage the environment because it is nice <3. 

Change directory (yes that is why the command is called "cd") to the repository you just cloned in the previous step and run:

.. code-block:: bash
    
   uv init .

Your project will now look like this:

.. code-block:: bash
        
    .
    ├── .git
    ├── .gitignore
    ├── .python-version
    ├── README.md
    ├── hello.py
    └── pyproject.toml

Then add ablog to the environment by running:

.. code-block:: bash
    
   uv add ablog

Now a virtial environment has been created in the .venv directory and ablog has been installed in it.

.. code-block:: bash
    
    .
    ├── .git
    ├── .gitignore
    ├── .python-version
    ├── .venv
    ├── README.md
    ├── hello.py
    ├── pyproject.toml
    └── uv.lock

We wont't need hello.py, so let's remove it:

.. code-block:: bash
    
   rm hello.py

Step 3: Setup ablog
-------------------
Now that we have a Python environment with ablog installed, we can setup ablog.

Run the following command to setup ablog:

.. code-block:: bash
    
   uv run ablog start

You are going to be prompted with a few questions. Here are the questions and the answers I used:

.. code-block:: console
    
    Welcome to the ABlog 0.11.12 quick start utility.

    Please enter values for the following settings (just press Enter to accept a
    default value, if one is given in brackets).

    Enter the root path for your blog project (path has to exist).
    > Root path for your project (path has to exist) [.]:

    Project name will occur in several places in the website, including blog archive
    pages and atom feeds. Later, you can set separate names for different parts of
    the website in configuration file.
    > Project name: Kasper Junge
    
    This of author as the copyright holder of the content. If your blog has multiple
    authors, you might want to enter a team name here. Later, you can specify
    individual authors using `blog_authors` configuration option.
    > Author name(s): Kasper Junge

    Please enter the base URL for your project. Blog feeds will be generated
    relative to this URL. If you don't have one yet, you can set it in configuration
    file later.
    > Base URL for your project: 

    Creating file ./conf.py.
    Creating file ./index.rst.
    Creating file ./about.rst.
    Creating file ./first-post.rst.
    Finished: An initial directory structure has been created.

Note that I inserted no base URL for the project.

Now we have a few new files and directories in the project:

.. code-block:: bash
    
    .
    ├── .git
    ├── .gitignore
    ├── .python-version
    ├── .venv
    ├── README.md
    ├── _static
    ├── _templates
    ├── about.rst
    ├── conf.py
    ├── first-post.rst
    ├── index.rst
    ├── pyproject.toml
    └── uv.lock


The .rst files are reStructuredText files, which is the markup language used by ablog, which you will quickly get used to. 

Here's a quick overview of the files:

- **index.rst** : index page for your blog, like index.html on websites I guess
- **about.rst** : you guessed it, an example about page
- **first-post** : example blog post, which you can edit to be your first blog post 🎉
- **conf.py** : configuration file for sphinx and ablog

 

.. ablog_website = "docs"
.. github_pages = "kasperjunge"

.. # List of patterns, relative to source directory, that match files and
.. # directories to ignore when looking for source files.
.. exclude_patterns = [""
..     '**/site-packages/**',
..     '**/*.dist-info/**',
.. ]

.. Step 4: Deploy Blog to GitHub Pages
.. commit build files to the repository:
.. uv run ablog deploy --github-branch main -w kasperjunge.github.io -g kasperjunge -p docs/
-----------------










.. Step 0:
.. Create a project directory, cd inside it and initialize a uv project and install ablog.
.. 0.1 - `uv init .`
.. 0.2 - `uv add ablog`

.. Step 1:
.. `uv run ablog start`

.. Setup 2:
.. Edit conf.py file:

.. from this:

.. exclude_patterns = [""]

.. to this: 

.. exclude_patterns = [
..     '**/site-packages/**',
..     '**/*.dist-info/**',
.. ]

.. For me `uv run ablog build` was failing with the error because it was interpreting some files in the site-packages directory as a blog post material. This change fixed it.

.. Step 3:
.. Make a posts directory and a 2025 directory in it, to group posts on year.

.. Step 4:
.. Move ablogs auto-generated first-post.rst file to the posts directory and rewrite it to be a hello world post.

.. Step 5:
.. Build the blog by running: 
.. uv run ablog build

.. Step 6:
.. Serve the blog on localhost:8000 with reload on changes by running: 
.. uv run ablog serve -r

.. Step 7:
.. Create a github repo named <username>.github.io

.. Step 8:



.. Other conf.py edits:
.. - theme
.. - html_title


.. ???
.. uv run ablog deploy --github-branch main
.. No place to deploy.a
