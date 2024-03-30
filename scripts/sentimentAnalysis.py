'''
In the context of dental procedures, traditional sentiments (positive, negative, neutral) may be less relevant.
Instead, it's more beneficial to focus on the intents and emotions related to pain, urgency and concern, breaking it down into the following categories:
1. Urgency : Indicating immediate attention is needed
2. Anxiety/concern: Expressing worry about a dental issue or treatment options
3. Inquiry: Seeking information about symptoms, procedures, or costs
4. Satisfaction/Dissatisfaction: Expressing contentment or disappointment with a dental visit
'''

from llama_index_client import EvalDataset
import nest_asyncio

nest_asyncio.apply()

from pathlib import Path
from llama_index.readers.file import PyMuPDFReader
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import IndexNode
from dotenv import load_dotenv
from llama_index.core.evaluation import QueryResponseDataset
import os
#setup vector index over this data
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.core.evaluation import QueryResponseDataset
from llama_index.core.evaluation.eval_utils import get_responses
from llama_index.core.evaluation import CorrectnessEvaluator, BatchEvalRunner
import numpy as np
from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


# load specific files within the data directory
reader = SimpleDirectoryReader(input_dir="../data/")
docs = reader.load_data()
print(f"loaded {len(docs)} documents")   # output: loaded 174 documents

# only load pdf files
required_ext = [".pdf"]
pdf_reader = SimpleDirectoryReader(
    input_dir="../data",
    required_exts=required_ext,
    recursive=True,
)

docs_pdf = pdf_reader.load_data()
print(f"loaded {len(docs_pdf)} pdf documents")  # output: loaded 173 pdf documents, which means it's correctly ignoring the txt file

load_dotenv()

# Retrieve the API key from the environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")


'''
Perform some embedding with the data
- Purpose of embeddings: are used in llamaindex to represent your documents using a sophisiticated numerical representation. Embedding models take text as input, and return a long list of numbers used to capture the semantics of the text.
'''

#Settings.embed_model = OpenAIEmbedding()

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

embed_model1 = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5", 
    embed_batch_size=42
)

embed_model2 = OpenAIEmbedding()   # use this if hugging face doesn't perform well

#per-index
index=VectorStoreIndex.from_documents(docs, embed_model=embed_model1)   # we are embedding the docs data which we imported using simpleDirectoryReader

query_engine = index.as_query_engine()
response = query_engine.query("what information relevant to the dental procedures were you able to extract from the pdfs?")
print(response)   # output: model embedding works as intended





# load all the pdf that contains information on the procedures
docs0_crossbite = PyMuPDFReader().load(file_path=Path("../data/crossbite.pdf"))
docs1_emax = PyMuPDFReader().load(file_path=Path("../data/emax-veneer.pdf"))
docs2_emax2 = PyMuPDFReader().load(file_path=Path("../data/emax-veneer2.pdf"))
docs3_gap = PyMuPDFReader().load(file_path=Path("../data/gap.pdf"))
#docs4_makeover = PyMuPDFReader().load(file_path=Path("../data/makeover.txt"))  --> TODO: need to find data in pdf format for makeover

docs4_openbite = PyMuPDFReader().load(file_path=Path("../data/openbite.pdf"))
docs5_overbite = PyMuPDFReader().load(file_path=Path("../data/overbite.pdf"))
docs6_overjet = PyMuPDFReader().load(file_path=Path("../data/overjet.pdf"))
docs7_underbite = PyMuPDFReader().load(file_path=Path("../data/underbite.pdf"))
docs8_zirconium = PyMuPDFReader().load(file_path=Path("../data/zirconium-veneer.pdf"))

#print(docs0_crossbite)
#print(docs0_crossbite.load_page(1))

doc0_text = "\n\n".join([d.get_content() for d in docs0_crossbite])
docs = [Document(text=doc0_text)]
node_parser = SentenceSplitter(chunk_size=1024)
print(node_parser.json)
base_nodes = node_parser.get_nodes_from_documents(docs)  # didn't get to figure this part out earlier



Settings.llm = OpenAI(model="gpt-4", api_key=api_key)  #ensure that emded_model="local" isn't specified
index = VectorStoreIndex(base_nodes)
query_engine = index.as_query_engine(similarity_top=0.5)


eval_dataset = QueryResponseDataset.from_json(
    "./llama2_eval_qr_dataset.json"
)



evaluator_c = CorrectnessEvaluator()
evaluator_dict = {"correctness": evaluator_c}
batch_runner = BatchEvalRunner(evaluator_dict, workers=2, show_progress=True)

#define correctness eval patterns
async def get_correctness(query_engine, eval_qa_pairs, batch_runner):
    # then evaluate
    # TODO: Evaluate a sample of genereated results
    eval_qs = [q for q, _ in eval_qa_pairs]
    eval_answers = [a for _, a in eval_qa_pairs]
    pred_responses = get_responses(eval_qs, query_engine, show_progress=True)

    eval_results = await batch_runner.aevaluate_responses(
        eval_qs, responses=pred_responses, reference=eval_answers
    )
    avg_correctness = np.array(
        [r.score for r in eval_results["correctness"]]
    ).mean()
    return avg_correctness



emotion_stimuli_dict = {
    "ep01": "Write your answer and give me a confidence score between 0-1 for your answer. ",
    "ep02": "This is very important to my career. ",
    "ep03": "You'd better be sure.",
    # add more from the paper here!!
}

# NOTE: ep06 is the combination of ep01, ep02, ep03
emotion_stimuli_dict["ep06"] = (
    emotion_stimuli_dict["ep01"]
    + emotion_stimuli_dict["ep02"]
    + emotion_stimuli_dict["ep03"]
)

QA_PROMPT_KEY = "response_synthesizer:text_qa_template"

from llama_index.core import PromptTemplate

qa_tmpl_str = """\
Context information is below. 
---------------------
{context_str}
---------------------
Given the context information and not prior knowledge, \
answer the query.
{emotion_str}
Query: {query_str}
Answer: \
"""
qa_tmpl = PromptTemplate(qa_tmpl_str)

# This should be defined as async because it calls another async function
async def run_and_evaluate(
    query_engine, eval_qa_pairs, batch_runner, emotion_stimuli_str, qa_tmpl
):
    """Run and evaluate."""
    new_qa_tmpl = qa_tmpl.partial_format(emotion_str=emotion_stimuli_str)

    old_qa_tmpl = query_engine.get_prompts()[QA_PROMPT_KEY]
    query_engine.update_prompts({QA_PROMPT_KEY: new_qa_tmpl})

    # Correctly await the async get_correctness function
    avg_correctness = await get_correctness(
        query_engine, eval_qa_pairs, batch_runner
    )

    query_engine.update_prompts({QA_PROMPT_KEY: old_qa_tmpl})
    return avg_correctness

# Usage (make sure this is inside an async context or an event loop)
# correctness_ep01 = await run_and_evaluate(...)



# try out ep01
import asyncio

# Assuming run_and_evaluate is ready to be called
async def main():
    # Setup and preparations...
    correctness_ep01 = await run_and_evaluate(
        query_engine,
        eval_dataset.qr_pairs,
        batch_runner,
        emotion_stimuli_dict["ep01"],
        qa_tmpl,
    )
    print(correctness_ep01)

if __name__ == "__main__":
    asyncio.run(main())


