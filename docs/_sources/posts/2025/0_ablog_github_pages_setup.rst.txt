
.. post:: Feb 14, 2025
   :tags: Guides
   :author: Kasper Junge

How to create a free blog with Sphinx and ablog hosted on GitHub Pages
===============================================================

*This blog post will show you have to create a free blog hosted on GitHub Pages using the Python documentation generator Sphinx and the ablog extension.*

Story (skip if you just want the guide)
---------------------------------------

When it comes to blogging, I have always been a wannabe.

First I got fascinated by Sam Altman's blogging style. You know, the tech-AI visionary who writes thoughtful posts about the future of technology and society. 
The feel of Sam's blog is kind of late 00's minimalist vibe. 
`Sam's blog <https://blog.samaltman.com/>`_ is hosted on Posthaven, which is a paid service for hosting blogs, so also used Posthaven for my blog 🫠

However, recently I stumbled upon `Simon Willison's blog <https://simonwillison.net/>`_ and got fascinated by his blogging style. 
He's more of a hacker-builder type, who writes about his projects and the tools he uses. 
The feel of Simon's blog is more of a early 00's code docs vibes.
I have no idea how Simon hosts his blog, but since he is the `co-creator of Django <https://en.wikipedia.org/wiki/Simon_Willison>`_, I assume he built it with that and self-hosts it.

Totally unrelated to blogging I also recently became interested in writing Python documentation (who doesn't get excited about that?). 
I quickly discovered that `Sphinx <https://www.sphinx-doc.org/en/master/>`_ is the go-to tool for writing Python documentation.
So I started reading the `Getting Started guide on the Sphinx website <https://www.sphinx-doc.org/en/master/usage/quickstart.html>`_, and there was one line in the intro that I got stuck in my head:

*"Sphinx focuses on documentation, in particular handwritten documentation, however, Sphinx can also be used to generate blogs, homepages and even books."*

This was my moment of enlightenment. I could use Sphinx to create a blog that had the early 00's code docs vibe of my new idol, Simon Willisons blog! 🎉 
This was litterally the reasoning that went through my head about shutting down my Posthaven blog and starting a new one with Sphinx.
I started doing research of how use sphinx for blogging and quickly found the `ablog <https://ablog.readthedocs.io/en/latest/>`_ extension for Sphinx that could be hosted free on GitHub Pages.

It turned out to be quite tedious to setup. And to be honest, I'm not sure that ablog is the best option at all, but now I'm too deep into it now to turn back 😂
To help my fellow blog-wannabes out there, I decided to write this guide to help others who want to create a blog with Sphinx and ablog.


Step 1: Create GitHub repository for your blog
----------------------------------------------
Create a new repository on GitHub named <username>.github.io. This will be the repository where your blog will be hosted.

When you have create the repository, clone it to your local machine:

.. code-block:: bash
    
   git clone git@github.com:<username>./<username>..github.io.git

For this guide to work, you’ll also need to open your repository’s Settings on GitHub, navigate to Pages, and under Build and deployment > Branch, change the build folder from /(root) to /docs.

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

    > Root path for your project (path has to exist) [.]:

    > Project name: Kasper Junge
    
    > Author name(s): Kasper Junge

    > Base URL for your project: 

Note that I inserted no base URL for the project.

Now we have a some new files and directories in the project:

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
- **first-post.rst** : example blog post, which you can edit to be your first blog post 🎉
- **conf.py** : configuration file for sphinx and ablog
- **_static/ and _templates/** : directories for static files and templates that sphinx/ablog uses

Your first auto-generated example blog post is going to look something like this:


.. code-block:: rst
    

   .. Kasper Junge post example, created by `ablog start` on Feb 14, 2025.

   .. post:: Feb 14, 2025
      :tags: atag
      :author: Kasper Junge

   First Post
   ==========

   World, hello again! This very first paragraph of the post will be used
   as excerpt in archives and feeds. Find out how to control how much is shown
   in `Post Excerpts and Images
   <https://ablog.readthedocs.io/manual/post-excerpts-and-images/>`__. Remember
   that you can refer to posts by file name, e.g. ``:ref:`first-post``` results
   in :ref:`first-post`. Find out more at `Cross-Referencing Blog Pages
   <https://ablog.readthedocs.io/manual/cross-referencing-blog-pages/>`__.

As far as I understood, ablog will automatically pick up any .rst files with the post directive (the "..post::"" thing) and add them to the blog. 
Thus, it should not matter too much where the blog posts are kept, but for keeping things organized, I like to move the first-post.rst file to a posts directory and create a 2025 directory in it:

.. code-block:: bash
    
   mkdir posts
   mkdir posts/2025
   mv first-post.rst posts/2025

Now we're almost ready for deploying our blog to GitHub Pages, but before we do that, we need one last thing.

Since we have our .venv/ directory in the project we need to add some files to the exclude_patterns in the conf.py file to avoid sphinx interpreting the files in the .venv/ directory as blog post material.

.. code-block:: python
   exclude_patterns = [""
      '**/site-packages/**',
      '**/*.dist-info/**',
   ]

Step 4: Deploy your blog
----------------------------------
To deploy your blog to GitHub Pages, you need to build the blog and push the build files to the repository. 

To do that we have to execute the following steps:

1. Build the blog to a build directory called "docs/"" using ablogs CLI command: ablog build
2. Commit the repository changes to git
3. Push the changes to GitHub using ablogs CLI command: ablog deploy
