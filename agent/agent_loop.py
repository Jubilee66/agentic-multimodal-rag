from langchain_groq import ChatGroq

from agent.planner_agent import create_plan
from agent.reflection_agent import reflect

from tools.vector_search_tool import (
    search_documents
)

from tools.image_search_tool import (
    search_images
)


def run_agent(
    query,
    api_key
):

    plan = create_plan(
        query=query,
        api_key=api_key
    )

    text_results = []

    image_results = []

    if plan["text_search"]:
        text_results = search_documents(
            query
        )

    if plan["image_search"]:
        image_results = search_images(
            query
        )

    reflection = reflect(
        query=query,
        text_context=str(text_results),
        image_context=str(image_results),
        api_key=api_key
    )

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        api_key=api_key,
        temperature=0
    )

    prompt = f"""
You are an Agentic Multimodal RAG Assistant.

QUESTION:
{query}

TEXT RESULTS:
{text_results}

IMAGE RESULTS:
{image_results}

RULES:

- Use retrieved evidence only.
- Do not hallucinate.
- Ignore irrelevant images.
- Mention image findings if useful.
- If evidence is insufficient,
  clearly say so.
"""

    answer = llm.invoke(
        prompt
    ).content

    return {
        "question": query,
        "plan": plan,
        "reflection": reflection,
        "answer": answer,
        "images": image_results
    }
# from langchain_groq import ChatGroq

# from agent.planner_agent import (
#     create_plan
# )

# from agent.reflection_agent import (
#     reflect
# )

# from tools.vector_search_tool import (
#     search_documents
# )

# from tools.image_search_tool import (
#     search_images
# )


# def run_agent(
#     query,
#     api_key
# ):

#     plan = create_plan(
#         query=query,
#         api_key=api_key
#     )

#     text_results = []

#     image_results = []

#     if plan.get(
#         "text_search",
#         True
#     ):
#         text_results = search_documents(
#             query
#         )

#     if plan.get(
#         "image_search",
#         False
#     ):
#         image_results = search_images(
#             query
#         )

#     reflection = reflect(
#         query=query,
#         text_context=str(
#             text_results
#         ),
#         image_context=str(
#             image_results
#         ),
#         api_key=api_key
#     )

#     best_text = min(
#         [
#             r["distance"]
#             for r in text_results
#         ],
#         default=999
#     )

#     best_image = min(
#         [
#             r["distance"]
#             for r in image_results
#         ],
#         default=999
#     )

#     if (
#         best_text > 0.75
#         and
#         best_image > 0.65
#     ):
#         return {
#             "question": query,
#             "plan": plan,
#             "reflection": reflection,
#             "text_results": text_results,
#             "images": image_results,
#             "answer":
#                 "I am unable to answer "
#                 "from the indexed "
#                 "knowledge base."
#         }

#     llm = ChatGroq(
#         model="openai/gpt-oss-120b",
#         api_key=api_key,
#         temperature=0
#     )

#     prompt = f"""
# You are an Agentic Multimodal RAG Assistant.

# QUESTION:
# {query}

# TEXT RESULTS:
# {text_results}

# IMAGE RESULTS:
# {image_results}

# Rules:

# 1. Use retrieved evidence only.
# 2. Never use external knowledge.
# 3. Never hallucinate.
# 4. Cite source files if available.
# 5. If evidence is weak, state so.
# 6. Use image captions and page text when relevant.
# """

#     answer = llm.invoke(
#         prompt
#     ).content

#     return {
#         "question": query,
#         "plan": plan,
#         "reflection": reflection,
#         "text_results": text_results,
#         "images": image_results,
#         "answer": answer
#     }


# if __name__ == "__main__":

#     import os

#     result = run_agent(
#         "What is AI according to NVIDIA?",
#         os.getenv(
#             "GROQ_API_KEY"
#         )
#     )

#     print(result)


##------------------------------------------------------------------------------------------------------

# from langchain_groq import ChatGroq

# from agent.planner_agent import create_plan
# from agent.reflection_agent import reflect

# from tools.vector_search_tool import search_documents
# from tools.image_search_tool import search_images


# def run_agent(
#     query,
#     api_key
# ):

#     llm = ChatGroq(
#         model="openai/gpt-oss-120b",
#         api_key=api_key,
#         temperature=0
#     )

#     text_context = ""
#     image_context = ""

#     final_plan = ""
#     final_reflection = ""

#     MAX_STEPS = 3

#     for step in range(MAX_STEPS):

#         final_plan = create_plan(
#             query=query,
#             api_key=api_key
#         )

#         print("\n" + "=" * 60)
#         print("PLAN")
#         print("=" * 60)
#         print(final_plan)

#         # ===============================
#         # TEXT SEARCH
#         # ===============================

#         if (
#             "TEXT_SEARCH" in final_plan
#             and not text_context
#         ):

#             print("\nRunning TEXT_SEARCH")

#             text_context = search_documents(
#                 query=query
#             )

#         # ===============================
#         # IMAGE SEARCH
#         # ===============================

#         if (
#             "IMAGE_SEARCH" in final_plan
#             and not image_context
#         ):

#             print("\nRunning IMAGE_SEARCH")

#             image_context = search_images(
#                 query=query
#             )

#         # ===============================
#         # REFLECTION
#         # ===============================

#         final_reflection = reflect(
#             query=query,
#             text_context=text_context,
#             image_context=image_context,
#             api_key=api_key
#         )

#         print("\n" + "=" * 60)
#         print("REFLECTION")
#         print("=" * 60)
#         print(final_reflection)

#         if final_reflection == "YES":

#             print(
#                 "\nEnough information gathered."
#             )

#             break

#         print(
#             "\nReflection says NO."
#         )

#         print(
#             "Attempting additional retrieval..."
#         )

#         # Fallback Retrieval

#         if not text_context:

#             text_context = search_documents(
#                 query=query
#             )

#         if not image_context:

#             image_context = search_images(
#                 query=query
#             )

#     # ==================================
#     # FINAL ANSWER
#     # ==================================

#     prompt = f"""
# You are an Agentic Multimodal RAG Assistant.

# QUESTION

# {query}

# TEXT CONTEXT

# {text_context}

# IMAGE CONTEXT

# {image_context}

# Rules:

# 1. Use retrieved information only.

# 2. Mention image findings if relevant.

# 3. Ignore irrelevant image results.

# 4. Do not hallucinate.

# 5. Mention sources when possible.
# """

#     result = llm.invoke(prompt)

#     return {
#     "question": query,
#     "plan": final_plan,
#     "reflection": final_reflection,
#     "answer": result.content,
#     "images": image_context if isinstance(image_context, list) else []
# }



# if __name__ == "__main__":

#     import os

#     print(
#         run_agent(
#             "What is AI according to NVIDIA?",
#             os.getenv("GROQ_API_KEY")
#         )
#     )

#---------TO RUN-----------------
# python -m agent.agent_loop

#---------------------------------

# from langchain_groq import ChatGroq

# from tools.vector_search_tool import (
#     search_documents
# )

# from tools.image_search_tool import (
#     search_images
# )


# def run_agent(query, api_key):

#     llm = ChatGroq(
#         model="openai/gpt-oss-120b",
#         api_key=api_key,
#         temperature=0
#     )

#     # TEXT RETRIEVAL

#     text_context = search_documents(
#         query
#     )

#     # IMAGE RETRIEVAL

#     image_context = search_images(
#         query
#     )

#     prompt = f"""
# You are a multimodal RAG assistant.

# TEXT CONTEXT

# {text_context}

# IMAGE CONTEXT

# {image_context}

# QUESTION

# {query}

# Answer using both text and image context.

# If image context is relevant,
# mention it.

# Do not hallucinate.
# Use only retrieved information.
# """

#     result = llm.invoke(
#         prompt
#     )

#     return result.content