
.. post:: Aug 17, 2023
   :tags: 
   :author: Kasper Junge

**A Process for Building LLM Classifiers**
==========================================

Large language models (LLMs) can be prompt-engineered to solve a wide variety of tasks. While many consider chat as the primary use case, LLMs can also be used to build traditional classifiers. 

Before the rise of advanced generative text-to-text models, crafting a custom text classifier was a time-consuming process that required extensive data collection and annotation.

Nowadays, you can get your hands dirty with LLMs without worrying about annotating data. This is great as it saves you a lot of time. However, it also becomes tempting to bypass best practices for building robust machine learning applications. 

When there's no need to create a training dataset, the temptation of simply hand-tuning a prompt based on a few examples becomes strong. You might convince yourself that it will generalize to any data that might be presented to it.The challenge is, without annotations to measure accuracy or a method to assess your prompt, you can't determine its robustness once deployed.

In my recent work with LLMs, I have thought a lot about this and have developed a process that, in my experience, enables the construction of robust LLM classifiers. This method is not only more efficient but also more enjoyable to fine-tune compared to the old school way of doing it.

The following process will help you craft more robust and reliable LLM modules.

**Step 1: Collect Dataset**
---------------------------

Collect a raw, unannotated dataset representative of the data on which your classifier will be used in real-world scenarios. The dataset's size should provide the desired significance level when assessing the classifier, while remaining realistic for you to annotate and not exhausting your API call budget with OpenAI. Divide the dataset into validation and test subsets.

Step 2: Create Initial Prompt
Construct an initial prompt you believe will be effective. It should yield two outputs. The first output should articulate the model's thoughts when determining which class to assign to the input text. 

This will be useful for iterative improvements to the prompt, ensuring it aligns with the task. In accordance with the chain-of-thought method, this should improve its performance and enhance explainability. The second output should specify the class you want the LLM to categorize.

The output format should look something like this:

.. code-block:: bash

    {
        "thoughts": <rationale behind classification here>, 
        "class": <the class the model has classified the example as here>
    }

Test the prompt on a few dataset samples to get a feeling og the model's comprehension of the task. Dedicate some time to refining it for optimal results. You should be confident that the LLM's has a reasonable understanding of the task.

**Step 3: Run, Inspect and Annotate**
--------------------------------------

Now run the hand-tuned prompt on the entire validation dataset.  For reproducibility, set the temperature to 0. Review all classified samples. If the LLM's categorization is inaccurate, correct it and document areas of misunderstanding. Use the thoughts output to understand its decision-making process. 

During annotation, you'll almost certainly discover complexities and nuances in the problem you're trying solve that didn't initially think of. Also you will likely discover ambiguities in the instruction you asked the LLM to follow, where you will have to be more clear in what you want it to do. In some cases the LLM's limits of understanding will also reveal themselves. Document these findings in an "annotation protocol", which outlines rules for managing edge cases.

**Step 4: Measure Performance of Prompt**
-----------------------------------------

Upon completing step 3, you'll have an annotated validation dataset. This allows for the evaluation of the prompt's predictive performance. Measure the performance to gain insight into the prompt's predictive capabilities.

**Step 5: Adjust Prompt**
-------------------------

Post step 5, you'll have written notes detailing cases where the LLM misclassified data. From this, formulate a hypothesis on potential prompt modifications to enhance its accuracy. Adjust the prompt in a which you think will mitigate the errors.

**Step 6: Iterate**
-------------------

After step 6, run the adjusted prompt on the validation dataset and measure its performance. Ideally, results should improve post-adjustment. Analyze incorrect classifications and take notes to understand the model's behavior. Repeat this process until you are satisfied with the prompt's performance or you believe that you have reached maximum performance.

**Step 7: Measure Performance on Test Dataset**
-----------------------------------------------

Now is the time. It's time to follow best practices, like the diligent and competent ML engineer you are. Now, you need to run the tuned prompt on a test set. However, your test set isn't annotated yet, presenting a significant temptation to skip this step. But you know you have to do it! If you do this, you will likely find that performance on the test dataset is a little worse. This is expected and is because you have probably overfitted your prompt to the validation dataset.

**Conclusion**
--------------

Congratulations, you now have an LLM classifier to solve a problem for you! For now, this is the best process I have. If you know of a better approach, I would love to hear from you. Additionally, at SEO.ai, where I work as an ML Engineer, we are constantly striving to crystallize our learnings into code. Specifically, we are developing a Python package called prompt-functions, which, in our experience, makes this process much smoother. We would love to continue the conversation on how to manage LLM applications, so please feel free to open an issue, send us a pull request or simply just reach out to me 🤗




