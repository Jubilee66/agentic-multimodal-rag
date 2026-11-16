from langchain_groq import ChatGroq


def create_plan(query, api_key):

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        api_key=api_key,
        temperature=0
    )

    prompt = f"""
You are a planner agent.

Available tools:

1. TEXT_SEARCH
- Use when document content is needed.

2. IMAGE_SEARCH
- Use when diagrams, charts, figures,
  architecture images, maps or visual
  content are needed.

Question:
{query}

Rules:

- Facts, summaries, reports, definitions
  → TEXT_SEARCH

- Diagrams, charts, maps, figures,
  visuals, images
  → IMAGE_SEARCH

- Explanation + image
  → BOTH

Return ONLY one of:

TEXT_SEARCH

IMAGE_SEARCH

TEXT_SEARCH, IMAGE_SEARCH
"""

    plan_text = (
        llm.invoke(prompt)
        .content
        .strip()
        .upper()
    )

    return {
        "text_search":
            "TEXT_SEARCH" in plan_text,

        "image_search":
            "IMAGE_SEARCH" in plan_text,

        "text_query":
            query,

        "image_query":
            query,

        "raw_plan":
            plan_text
    }

# from langchain_groq import ChatGroq
# def create_plan(query, api_key):

#     llm = ChatGroq(
#         model="openai/gpt-oss-120b",
#         api_key=api_key,
#         temperature=0
#     )

#     prompt = f"""
#         You are a planner agent.

#         Available tools:

#         1. TEXT_SEARCH
#         Use when the answer requires document content.

#         2. IMAGE_SEARCH
#         Use when the answer requires diagrams, charts, figures or images.

#         Question:
#         {query}

#         Return ONLY one of these:

#         TEXT_SEARCH

#         IMAGE_SEARCH

#         TEXT_SEARCH, IMAGE_SEARCH
#         """

#     response = llm.invoke(prompt)
#     return f"""
#         QUESTION:
#         {query}

#         PLAN:
#         {plan}

#         REFLECTION:
#         {reflection}

#         ANSWER:
#         {result.content}
#         """

#     # return response.content.strip()