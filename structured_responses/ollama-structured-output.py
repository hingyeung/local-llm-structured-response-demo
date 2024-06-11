from langchain_community.llms import Ollama
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import (
    PydanticOutputParser,
    RetryOutputParser,
    OutputFixingParser,
)
from langchain_core.runnables import RunnableParallel, RunnableLambda

from structured_responses.config import Config


config = Config()
model_name = config.model_name
user_question = config.user_question
context = config.context

# output model
class Person(BaseModel):
    name: str = Field(description="Name of the person")
    age: int = Field(description="Age of the person")


plain_text_template = """You are an assistant IA and is very good at extracting deep meaning in provided context. Answer user question based on the context provided.
Context: {context}
{format_instructions}
Question: {query}
Response:"""

# <|eot_id|> is supposed to be at the end of the text. The response was very wrong when I put the <|eot_id|> on the next line.
# Not sure why.
template_with_system_prompt_and_llama3_token = """
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are an assistant IA and is very good at extracting deep meaning in provided context. Answer user question based on the context provided.<|eot_id|><|start_header_id|>user<|end_header_id|>
Context: {context}
{format_instructions}
Question: {query}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
Response:<|eot_id|>
"""

for template in [plain_text_template, template_with_system_prompt_and_llama3_token]:
    llm = Ollama(temperature=0, model="llama3")

    person_pydantic_parser = PydanticOutputParser(pydantic_object=Person)
    fix_parser = OutputFixingParser.from_llm(parser=person_pydantic_parser, llm=llm)
    retry_parser = RetryOutputParser.from_llm(parser=fix_parser, llm=llm)

    prompt = PromptTemplate(
        template=template,
        partial_variables={
            "format_instructions": person_pydantic_parser.get_format_instructions(),
            "context": context,
        },
        input_variables=["query"],
    )
    print(f"\n\nPrompt >>>  {prompt.invoke({"query": user_question})}")

    # use retry_parser to get acceptable answer before giving it to
    # pydantic parser to get the final Person object
    chain = prompt | llm
    main_chain = RunnableParallel(completion=chain, prompt_value=prompt) | RunnableLambda(
        lambda x: retry_parser.parse_with_prompt(**x)
    )

    print(f"Plain text response >>>  {chain.invoke({"query": user_question})}")
    print(f"Structured response >>>  {main_chain.invoke({"query": user_question})}")
