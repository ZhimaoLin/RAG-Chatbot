# RAG-Chatbot

An AI chatbot that searches PDF files from the [Pinecone](https://www.pinecone.io/) vector store using [Retrieval-Augmented Generation (RAG)](https://ai.meta.com/blog/retrieval-augmented-generation-streamlining-the-creation-of-intelligent-natural-language-processing-models/) system.

## Quick Demo

### Ask a Question

```
You: How to diagnose Resistant Hypertension?
==============================
          Answer
==============================
The steps to diagnose Resistant Hypertension include the following:

1. Proper office and out-of-office blood pressure measurement.
2. Optimization of pharmacotherapy, taking into consideration clinical inertia.
3. Assessment of adherence to medication regimen.
4. Evaluation of other factors, as described in Table 2 and Figure 1 of the guidelines.

It is important to note that these steps should be performed in conjunction with a healthcare professional.
==============================

============================================================
Source [1]       File: [data/paper3.pdf]         Page: [4]
============================================================
Conﬁrm diagnosis of true resistant hypertension
Figure 1. Diagnostic algorithm for a patient with suspected resistant hypertension. ABPM, ambulatory blood pressure monitoring; BP, blood
pressure; HT, hypertension. *Three or more drugs, at optimally tolerated dosages, and preferably including a diuretic.yHome BP monitoring can be
performed if ABPM is not accessible.628 Canadian Journal of Cardiology
Volume 36 2020
============================================================

============================================================
Source [2]       File: [data/paper3.pdf]         Page: [3]
============================================================
 for uncontrolled vs controlled RHT.20
Diagnosis of Resistant Hypertension
The diagnosis of RHT should take into account proper
ofﬁce and out-of-of ﬁce BP measurement, optimization of
pharmacotherapy taking into consideration clinical inertia,
and an assessment of adherence, in addition to other factors as
described in Table 2 andFigure 1 .
BP measurement
Cohort studies that have evaluated prognosis as well as
some
============================================================
```

### Ask a Follow-up Question

```
You: How to treat it?
==============================
          Answer
==============================
The recommended treatment for Resistant Hypertension includes several steps:

1. Rule out white coat effect by preferably using ambulatory blood pressure monitoring (ABPM).
2. Assess for nonadherence to medication.
3. Optimize drug therapy, considering factors such as drug dose, duration, and diuretic choice.
4. Consider additional treatments, such as directly observed therapy or adding fourth-line antihypertensive agents.

It is important to note that specific treatment recommendations may vary for each individual, and it is best to consult with a healthcare professional for personalized treatment plans.
==============================

============================================================
Source [1]       File: [data/paper3.pdf]         Page: [1]
============================================================
============ Omit the content for demo purpose =============
============================================================

============================================================
Source [2]       File: [data/paper3.pdf]         Page: [4]
============================================================
============ Omit the content for demo purpose =============
============================================================
```

### Clear the Chat History

```
You: clear
You: How to treat it?
==============================
          Answer
==============================
The treatment for "it" is not clear from the provided context. Please provide more specific information or clarify what condition or disease you are referring to.
==============================
```


## How to run the code

Both Jupyter Notebook and Python scripts are provided. If you prefer step-by-step explanations, you can refer to the Jupyter Notebooks. 

- Jupyter Notebooks
  - [load_papers.ipynb](./load_papers.ipynb)
  - [chatbot.ipynb](./chatbot.ipynb)
- Python scripts
  - [load_papers.py](./load_papers.py)
  - [chatbot.py](./chatbot.py)

### Configuration

First of all, please add API keys and vector store information to the `config.py`. 

- `OPENAI_API_KEY`
- `PINECONE_API_KEY`
- `PINECONE_ENVIRONMENT`
- `PINECONE_INDEX_NAME`

### Dependencies

In order to install all the dependencies, you can run the `pip` command at the top of the notebook 

or

`pip install -r requirements.txt`

If you are using MacOS, please use `pip3` instead.

### Run

Please put all the PDFs that you want upload into the `/data` folder. You need to load your PDFs to the Pinecone vector storage and then run the chatbot. The `chatbot.py` offers an interaction with the chatbot through the terminal. However, `chatbot.ipynb` only runs a few test cases. 

#### Load PDFs

Please insert all the relative path to your papers into `PAPER_LIST` global variable, such as `PAPER_LIST = ["data/paper1.pdf", "data/paper2.pdf", "data/paper3.pdf"]`

Then, run 

`python ./load_papers.py`

or

`load_papers.ipynb`

This will embed all your PDF files into vectors stored in the Pinecone vector storage.

#### Run the chatbot

Then, run 

`python ./chatbot.py`

or

`chatbot.ipynb`

##### User Interaction

`chatbot.py` offers a user-interaction with the chatbot. Here are a few commands for the chatbot:

- `clear`: Clear the chat history and start a new session
- `quit`: Quit the chatbot

