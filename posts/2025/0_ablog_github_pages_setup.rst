Here's the corrected version:

---

.. post:: Feb 14, 2025  
   :tags: Guides  
   :author: Kasper Junge

How I Created a Free Blog using Python and GitHub Pages
=====================================================================

*This blog post will show you how to create a free blog hosted on GitHub Pages using the Python documentation generator Sphinx and the ablog extension.*

Story (Skip If You Just Want the Guide)
-----------------------------------------

When it comes to blogging, I have always been a wannabe.

First, I got fascinated by Sam Altman's blogging style. You know, the tech-AI visionary who writes thoughtful posts about the future of technology and society.  
The feel of Sam's blog is reminiscent of the late 00’s minimalist vibe.  
`Sam's blog <https://blog.samaltman.com/>`_ is hosted on Posthaven, which is a paid service for hosting blogs, so I also used Posthaven for my blog 🫠

However, recently I stumbled upon `Simon Willison's blog <https://simonwillison.net/>`_ and became fascinated by his blogging style.  
He's more of a hacker-builder type, writing about his projects and the tools he uses.  
The feel of Simon's blog is more reminiscent of early 00’s code documentation vibes.  
I have no idea how Simon hosts his blog, but since he is the `co-creator of Django <https://en.wikipedia.org/wiki/Simon_Willison>`_, I assume he built it with Django and self-hosts it.

Totally unrelated to blogging, I also recently became interested in writing Python documentation (who doesn't get excited about that?).  
I quickly discovered that `Sphinx <https://www.sphinx-doc.org/en/master/>`_ is the go-to tool for writing Python documentation.  
So I started reading the `Getting Started guide on the Sphinx website <https://www.sphinx-doc.org/en/master/usage/quickstart.html>`_, and there was one line in the intro that stuck with me:

*"Sphinx focuses on documentation, in particular handwritten documentation; however, Sphinx can also be used to generate blogs, homepages, and even books."*

This was my moment of enlightenment. I could use Sphinx to create a blog that had the early 00’s code documentation vibe of my new idol, Simon Willison’s blog! 🎉  
This was literally the reasoning that went through my head about shutting down my Posthaven blog and starting a new one with Sphinx.  
I started researching how to use Sphinx for blogging and quickly found the `ablog <https://ablog.readthedocs.io/en/latest/>`_ extension for Sphinx that could be hosted for free on GitHub Pages.

It turned out to be quite tedious to set up. And to be honest, I'm not sure that ablog is the best option at all, but now I'm too deep into it to turn back 😂  
To help my fellow bloggers out there who wants a blog that reminds people of a code documentation site (must be a massive audicence), I decided to write this guide to help others who want to create a blog with Sphinx and ablog.

Step 1: Create a GitHub Repository for Your Blog
-------------------------------------------------

Create a new repository on GitHub named `<username>.github.io`. This will be the repository where your blog will be hosted.

Once you have created the repository, clone it to your local machine:

.. code-block:: bash
    
   git clone git@github.com:<username>/<username>.github.io.git

For this guide to work, you’ll also need to open your repository’s Settings on GitHub, navigate to Pages, and under **Build and deployment > Branch**, change the build folder from `/` (root) to `/docs`.

Step 2: Set Up a Python Environment with uv
--------------------------------------------

Next, create a Python environment for your blog.

We will use **uv** to manage the environment because it is nice <3.

Change directory (yes, that is why the command is called "cd") to the repository you just cloned in the previous step and run:

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

Now a virtual environment has been created in the `.venv` directory and ablog has been installed in it.

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

We won't need `hello.py`, so let's remove it:

.. code-block:: bash
    
   rm hello.py

Step 3: Set Up ablog
--------------------

Now that we have a Python environment with ablog installed, we can set up ablog.

Run the following command to set up ablog:

.. code-block:: bash
    
   uv run ablog start

You are going to be prompted with a few questions. Here are the questions and the answers I used:

.. code-block:: console

    > Root path for your project (path has to exist) [.]:

    > Project name: Kasper Junge
    
    > Author name(s): Kasper Junge

    > Base URL for your project: 

Note that I left the base URL for the project blank.

Now we have some new files and directories in the project:

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

The `.rst` files are reStructuredText files, which is the markup language used by ablog, and you will quickly get used to it.

Here's a quick overview of the files:

- **index.rst**: The index page for your blog, similar to index.html on websites, I guess.
- **about.rst**: An example about page.
- **first-post.rst**: An example blog post, which you can edit to become your first blog post 🎉.
- **conf.py**: The configuration file for Sphinx and ablog.
- **_static/** and **_templates/**: Directories for static files and templates that Sphinx/ablog uses.

Your first auto-generated example blog post is going to look something like this:

.. code-block:: rst
    
   .. Kasper Junge post example, created by `ablog start` on Feb 14, 2025.

   .. post:: Feb 14, 2025
      :tags: atag
      :author: Kasper Junge

   First Post
   ==========

   World, hello again! This very first paragraph of the post will be used
   as an excerpt in archives and feeds. Find out how to control how much is shown
   in `Post Excerpts and Images
   <https://ablog.readthedocs.io/manual/post-excerpts-and-images/>`__. Remember
   that you can refer to posts by file name, e.g. ``:ref:`first-post``` results
   in :ref:`first-post`. Find out more at `Cross-Referencing Blog Pages
   <https://ablog.readthedocs.io/manual/cross-referencing-blog-pages/>`__.

As far as I understand, ablog will automatically pick up any `.rst` files with the post directive (the ".. post::" thing) and add them to the blog.  
Thus, it should not matter too much where the blog posts are kept, but to keep things organized, I like to move the `first-post.rst` file to a `posts` directory and create a `2025` directory in it:

.. code-block:: bash
    
   mkdir posts
   mkdir posts/2025
   mv first-post.rst posts/2025

Now we're almost ready to deploy our blog to GitHub Pages, but before we do that, we need one last thing.

Since we have our `.venv/` directory in the project, we need to add some files to the `exclude_patterns` in the `conf.py` file to avoid Sphinx interpreting the files in the `.venv/` directory as blog post material.

.. code-block:: python
   
   exclude_patterns = [
      '**/site-packages/**',
      '**/*.dist-info/**',
   ]

Step 4: Deploy Your Blog
------------------------

To deploy your blog to GitHub Pages, you need to build the blog and push the build files to the repository.

I've created a short Python script that does all of this for you:

.. code-block:: python
    
   import subprocess
   from pathlib import Path

   def deploy():
      
      # 1. Get the path to the build directory
      build_path = str((Path(__file__).parent / "docs").resolve())

      # 2. Build the blog
      subprocess.run("uv run ablog build -w docs", shell=True)

      # 3. Commit the blog updates
      subprocess.run("git add .", shell=True)
      subprocess.run('git commit -m "update blog"', shell=True)

      # 4. Deploy the blog to GitHub pages
      subprocess.run(
         f"uv run ablog deploy --github-branch main -w {build_path} -g kasperjunge -p {build_path}",
         shell=True
      )

      # 5. Push the updates to the repository
      subprocess.run("git push", shell=True)

   if __name__ == "__main__":
      deploy()


Here's what the script does:

1. Gets the path to the build directory.
2. Runs ablog's CLI command `ablog build` to build the blog. The `-w docs` flag tells ablog to build the blog in a directory named `docs/`.
3. Commits the repository changes to Git.
4. Runs ablog's CLI command `ablog deploy` to deploy the blog to GitHub Pages. The `--github-branch main` flag tells ablog to deploy to the `main` branch. If not specified, it will try to use `master`. The `-g kasperjunge` flag tells ablog to deploy to the repository `kasperjunge/kasperjunge.github.io`. The `-p docs` flag tells ablog to deploy the `docs/` directory.
5. Pushes the updates to the repository. (Actually, this step should be carried out by the `ablog deploy` command, but it doesn’t always work for me, so I added this step.)

Now you can go to your repository and see that a set of GitHub Actions has been invoked to deploy your blog to GitHub Pages.  
When they're done, you should be able to see your blog at `https://<username>.github.io`.

And that's it!

I plan to adjust the theme and design of the blog and also set up Google Analytics to track analytics on the blog in the future.  
When I do that, I will update this post to explain how I did it. For now, I will end it here.  
I hope you got it to work! If not, feel free to reach out to me.