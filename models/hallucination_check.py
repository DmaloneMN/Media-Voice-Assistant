from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

judge_prompt = PromptTemplate.from_template(
    "Does this recommendation: '{response}' match the context: '{context}'? Output 'Yes' or 'No'."
)
judge_chain = LLMChain(llm=llm, prompt=judge_prompt)

def check_hallucination(response, context):
    return judge_chain.run(response=response, context=context).strip() == "Yes"

# Integrate with agent
result = RetrievalQA.from_chain_type(llm, retriever=kb_map["movie"]).run(query)
context = "\n".join([d.page_content for d in result["source_documents"]])
if not check_hallucination(result["result"], context):
    result["result"] += " (Verify with official sources—may be inaccurate.)"
