from langchain_groq import ChatGroq


def reflect(
    query,
    text_context,
    image_context,
    api_key
):

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        api_key=api_key,
        temperature=0
    )

    prompt = f"""
Question:

{query}

TEXT CONTEXT:

{text_context}

IMAGE CONTEXT:

{image_context}

Do we have enough information
to answer the question accurately?

Reply ONLY:

YES

or

NO
"""

    result = llm.invoke(prompt)

    return result.content.strip().upper()