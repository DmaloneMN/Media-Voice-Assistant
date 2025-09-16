judge_prompt = PromptTemplate.from_template(
    "Does this rec: '{response}' match the media context: '{context}'? Yes/No."
)
judge_chain = LLMChain(llm=llm, prompt=judge_prompt)

def check_media_hallucination(response, context):
    return judge_chain.run(response=response, context=context).strip() == "Yes"

# In agent
result = RetrievalQA(...).run(query)
if not check_media_hallucination(result["result"], "\n".join([d.page_content for d in result["source_documents"]])):
    result["result"] += " (Verify with official sources—may be inaccurate.)"
