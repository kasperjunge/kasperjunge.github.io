.. post:: 
   :tags: 
   :author: Kasper Junge

**How I code with AI**
======================

Since the launch of ChatGPT, I've been using LLMs for coding a lot.

I've developed a workflow and some fundamental principles I use to get good results from AI chatbots and ideally to make AI do as much of the coding for me as possible.

What I've experienced talking to others who are coding with AI, is that almost no one has the same workflow.

Since I always enjoy hearing about others' workflows, I thought I would share mine.

When it comes to getting good results from AI chatbots, in my mental model there's 3 components that can impact the result an LLM generates.

Model capability
Instruction
Context
The above I use as core components to think about how to get the best possible output from LLMs from first principles.

I will refer back to them in the blog post.

In this blog post I will tell about my AI coding workflow and how I got there.

First of all – I mainly use vanilla ChatGPT for coding. I use a little GitHub copilot for autocomplete stuff, but no Cursor, lovable.dev, bito.new, devbin, etc.

This might seem a little old-school and handheld, and I am always open for new ways of using AI for coding, but for now vanilla ChatGPT and a small tool I've developed works great for me.

When I initiate my AI coding sessions, it is usually a situation where there's some existing code that I want to add a feature to or modify in some way.

Here we can bring in the fundamental components I mentioned earlier.

Context: The existing code I want to modify.
Instruction: The thing I want to do with the code.
Usually, I have the instruction in my head, so I start out gathering the context that the LLM needs to fully understand my project.

Back in the days, I did a lot of copy-pasting of file content into ChatGPT, which was pretty time-consuming, but worked well.

Pretty quickly I also discovered that a common source of context-related failure was that the LLM did not know where the files were located relative to each other and in general had poor understanding of my project structure.

That led to me using the "tree" command a lot and copy-pasting the output of it into ChatGPT (tree prints a file tree of a dir's files and subdirs). This turned out to be valuable information for the LLM that helped it do a better job fulfilling my instructions.

However, I quickly became tired of all that manual copy-pasting work, so I decided to invest some time into automating it.

That led to me developing the tool "copcon" (for "copy context").

It basically works by typing:
copcon /path/to/code/project

in the terminal, and it copies the file tree and the content of all files directly onto the clipboard, so that context about the entire project is easily available on ctrl + v to copy-paste into ChatGPT.

This really supercharged my workflow and improved the results I got from ChatGPT a lot. However, as the reader might predict, I quickly ran into another problem.

As many may know, LLMs have limited context windows, meaning that there's a finite amount of tokens they can process at a time.

One thing I quickly discovered with copcon is that if the file tree is big, a lot of tokens is copied and it quickly bleats the context window of ChatGPT which simply makes it refuse my query.

Also, even if the content fits in the context window, ChatGPT can become "confused" about the information overload which leads to degraded performance.

So as a rule of thumb, I think it is always the best idea to keep the context as tight as possible.

One thing I didn't mention is that copcon is open source and can be found on GitHub and it’s on PyPi, so it can be installed using pip.

The reason I mentioned this is because the solution to this problem came from a contributor.