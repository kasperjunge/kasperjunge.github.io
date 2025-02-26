
.. post:: Feb 26, 2025
   :tags: 
   :author: Kasper Junge

Investigating the DeepSeek DeepGEMM Release
===========================================

DeepSeek just released `DeepGEMM <https://github.com/deepseek-ai/DeepGEMM>`_, as the third release in their `Open-Sourcing 5 AI Repos in 5 Days <https://github.com/deepseek-ai/open-infra-index>`_ series.

I'm no LLM infra engineer, so I am probably not the primary audience for this release.

Also, I can't claim that I would fully understand what was going on under the hood in DeepGEMM if I read the code. At the very least, it would take me quite some time.

But I'm curious. So I thought I would write a short blog post where I share my understanding of what DeepGEMM is and what it can be used for.

In this blog post, I will go through the repo, read the comments on the `Hacker News post of the release <https://news.ycombinator.com/item?id=43179478>`_, and write about what I learn.

Programming Languages Used
--------------------------

By looking at the DeepGEMM repository on GitHub, the first thing I notice is that the code is written in 58.9% CUDA and 41.1% Python.

This tells me that the content of this code likely consists of CUDA kernels that optimize some of the calculations executed when running LLM training and inference. (It's fine, just call me a genius.)

The fact that almost half of the code is Python could indicate that the optimized CUDA kernels are made available as Python bindings through a deep learning framework like PyTorch.

The README
----------

Surprisingly, the README file contains a lot of information about the project.

It states that DeepGEMM is:

   *a library designed for clean and efficient FP8 General Matrix Multiplications (GEMMs) with fine-grained scaling, as proposed in DeepSeek-V3.*

FP8 is an 8-bit floating point format, which I suppose is used to represent model weights in order to reduce the memory footprint of the model and thus speed up training and inference.

General Matrix Multiplications (GEMMs) is a term I've never heard before. However, after some research, I quickly learned that this is basically just the operation of multiplying two matrices to produce a third matrix—an operation heavily used when training and running deep learning models.

Then, it is mentioned that the library provides *fine-grained scaling*.  
After some research, it seems that this has to do with managing numerical underflow/overflow when working with such low precision.  
The reason it is called fine-grained is that it does not use a single global scaling factor for the entire matrix but instead applies different scaling factors to different sections of the matrix to ensure numerical stability.  
So one of the big problems it solves is keeping matrix multiplications numerically stable with a precision as low as FP8.

One thing I'm curious about now is whether this is a new concept or if it has been around for a while.

Terms That I Don't Know and/or Understand
-----------------------------------------

In the README, there were many terms I either didn't know or didn't fully understand.

The first was `CUTLASS <https://github.com/nvidia/cutlass>`_, which appears to be an abbreviation for *CUDA Templates for Linear Algebra Subroutines and Solvers*.  
It is a library developed by NVIDIA that provides high-performance matrix-multiplication code optimized for NVIDIA GPUs.  
DeepGEMM takes inspiration from CUTLASS but is simpler. DeepGEMM seems to differentiate from CUTLASS by providing support for FP8 precision.

The second term I didn't know was `CuTe <https://github.com/NVIDIA/cutlass/tree/main/include/cute>`_, which, like CUTLASS, is a library that provides CUDA templates. (I'm not entirely sure what is meant by templates in a CUDA context.)  

The DeepSeek engineers give credit to both the CUTLASS and the CuTe library in the README and mention that DeepGEMM took inspiration from it.

Hacker News Comments
--------------------

To be honest, the comments on the Hacker News post of the release was way above my knowledge of GPU programming.
However, I summarized the top 20 points from the comments with ChatGPT and to me it was super interesting to read.
So here at the end, I will be super lazy and just paste the key points from the comments:

1. DeepGEMM claims 2x–2.5x speedup over its own CUTLASS-based baseline.
2. Uncertainty remains on performance vs. cuBLAS, which is the gold standard for NVIDIA GEMMs.
3. FFMA SASS interleaving optimization improves FP8 GEMM performance by 10%+.
4. Yield-bit manipulation allows warp-level parallelism, reducing stalls and improving register reuse.
5. Similar techniques were used in NVIDIA Maxwell (2015) but hadn’t been applied to FP8 GEMMs.
6. Reverse engineering NVIDIA’s SASS assembly has been a key part of these optimizations.
7. Some corporations and hedge funds have implemented similar optimizations privately.
8. Google and other AI firms have also explored undocumented NVIDIA optimizations.
9. DeepSeek's open-source MIT license approach is appreciated but benefits big AI companies more than individual developers.
10. FP8 precision may not be sustainable long-term, as it relies on the assumption that models are inherently sparse.
11. Native microscaling support (MXFP) in Blackwell GPUs may replace DeepGEMM’s scaling tricks.
12. NVIDIA’s CUDA advantage ("moat") may weaken if more AI accelerators integrate similar optimizations in hardware.
13. DeepGEMM only runs on Hopper GPUs (H100, H800) due to Tensor Core dependencies.
14. Attempts to run it on consumer GPUs (RTX 5080) failed due to shared memory limitations.
15. Lowering memory settings in gemm.py may allow it to work on lower-end GPUs.
16. GPU compiler technology still lags behind—manual optimizations like this show how much performance is left on the table.
17. Future GPUs may reduce the need for low-level software optimizations as hardware catches up.
18. NVIDIA keeps some GPU features undocumented, leading to reverse engineering by researchers and companies.
19. AI engineers interested in GPU programming should learn CUDA, SIMT, warp scheduling, and memory hierarchies.
20. Books recommended for learning GPU programming: Programming Massively Parallel Processors (Wen-Mei Hwu) and Advanced GPU Assembly Programming (Gareth Thomas).

Conclusion
----------

All in all, DeepGEMM seems to be a library that provides CUDA kernels that can be accessed via PyTorch and enables numerically stable FP8 precision to speed up training and inference of Large Language Models.

If you want to check out the two previous DeepSeek infra releases, visit the `FlashMLA <https://github.com/deepseek-ai/FlashMLA>`_ and `DeepEP <https://github.com/deepseek-ai/DeepEP>`_ repos. 👍
