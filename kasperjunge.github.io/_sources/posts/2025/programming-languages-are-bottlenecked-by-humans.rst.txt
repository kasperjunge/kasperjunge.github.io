
.. Kasper Junge post example, created by `ablog start` on Feb 13, 2025.

.. post:: Feb 13, 2025
   :tags:
   :author: Kasper Junge

Programming Languages are Bottlenecked by Humans
================================================================

I recently heard an interview with `Bret Taylor <https://backchannel.org/>`_ in the `Latent Space Podcast <https://youtu.be/0G1vd3Trj2U?si=lSWMWfw7TlSjxwk0>`_.

He shared an intersting observation about programming languages that got me thinking.

I went something along the lines of like this:

Programming languages like Rust is optimized for being fast at runtime, while Python is being optimized for being fast at authorshiptime.

So the advantage you get by choosing Python is that you humans can write code faster.

That is nice because then it is cheaper to ship software and you can iterate faster because developers do not have to spend as much time coding as they maybe would have in Rust.

And for many applications the crazy fast runtime speed of Rust enables is just super overkill and do not make sense.

So we optimize for authorshiptime because of humans.

But as AI begins to code more and more of the code the runs in software, coudl we then imagine that the human bottleneck will be removed?

Because if humans was not a factor, there would be no reason to optimize for authorshiptime, and thus no reason to choose Python over Rust.

Bret then shared that he was curious about what programming languages would look like if they were only optimized for AI authorship.
