from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv('query_key'),
    model_name="llama-3.1-8b-instant"
)

def query_processing_agent(query):
    prompt = f"""
Your task is to extract only the proper noun or central entity mentioned in the user's input prompt.

- The output must be exactly the main person, place, animal, or concept mentioned in the user's input.
- Do NOT hallucinate, guess, or add anything.
- If multiple entities are present, extract only the most relevant one (usually the proper noun).
- If no clear entity is present, return "UNKNOWN".

Examples:
Input: "Give me the life story of Nikola Tesla" → Output: Nikola Tesla  
Input: "Tell me about the habitat of Bengal tigers" → Output: Bengal tiger  
Input: "What is the significance of the Great Wall of China?" → Output: Great Wall of China  
Input: "How does photosynthesis work?" → Output: Photosynthesis  
Input: "What is quantum physics?" → Output: Quantum physics  

Now process only this input and output the correct entity, nothing else.

User Input:
"{query}"

Output:
"""

    pt = PromptTemplate(
        input_variables=["user_input"],
        template=prompt
    )

    chain = pt | llm

    response = chain.invoke({"user_input": query})

    return response.content.strip()
