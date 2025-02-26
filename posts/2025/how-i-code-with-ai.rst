.. post:: Feb 30, 2025
   :tags: 
   :author: Kasper Junge

How I Code With AI
==================
Since the release of ChatGPT, I've been coding *a lot* wiht AI.

I'v been through a lot of trial and error, and have landend on a process that works well for me. 

When I talk to other developers that uses AI for coding about their workflow and what tools they use, I seem to get as many answers as people I ask.

So I thought I would share my process with you.

The Tools I use
-----------------

First I want to quickly go through the tools that I use. I keep it pretty simple and handheld, so the two tools that i mainly use is:

1. `ChatGPT <https://chatgpt.com/>`_ 
2. `Copcon <https://github.com/kasperjunge/copcon>`_

ChatGPT is obviously an LLM-based chatbot.

Copcon is a tool I've developed to efficiently copy context from my code project to ChatGPT (more on `Copcon <https://github.com/kasperjunge/copcon>`_ later).

When I tell other devs about my stack, a common reaction is that it is kind of handheld and thinks that I could benefit from tools that automates the copy conext part.

I'm not at all sure that my ways is the best (it is probably not i guess) and I am curious if I am making it harder for myself using this quite handheld stack, so I have it on my todo to try some of the other tools and I will probably write a blog post on the pros and cons by the method i describe now vs other soliutions like Cursor, GitHub Copilot Chat etc.

The 3 Components
----------------

When I think about what it takes to increase the quality of the code that AI writes for me, I think about it in the following three components: 

1. Context
2. Instruction
3. Model capability

In the following I will go through each of the components and how I optimize for each of them.

1. Load context into the LLM
2. Write my instruction
3. Clarify my instruction with the LLM
4. Put the LLM to work



Context
~~~~~~~

When you use LLMs you have to work with the fact that even though they on a super human level know a lot about many concepts in the world, they know nothing about you, your situation, what you want to accomplish and how you want to accomplish it. 

And the solution is actually simple. You have to provide all the nessesary context about all information that is relevant to solve you problem, in the prompt.

The catch is that this this is actually hard work to provid context. It involves a lot of copy pasting and thinking about what information is relevant and what is not.

In fact, this can be so time consuming that many developers conclude that it is simply 

My first step when begging an AI coding session is to boot the context into the LLM.

Instruction
~~~~~~~~~~~



