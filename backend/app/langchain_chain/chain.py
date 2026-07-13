
# #  working




# """
# Product-matching RAG pipeline: embeds the Galaxy Plastics product catalog
# into a Chroma vector store. Retrieves relevant products and lets the LLM
# select the best match with structured JSON output.
# """

# import json
# from pathlib import Path
# from typing import Optional, TypedDict

# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain_community.vectorstores import Chroma
# from langchain_core.documents import Document
# from langchain.prompts import PromptTemplate
# from langchain.schema.output_parser import StrOutputParser
# from langchain.schema.runnable import RunnableLambda


# PRODUCTS_PATH = Path(__file__).parent.parent / "data" / "products.json"

# PROMPT = PromptTemplate.from_template(
#     """
# You are a product-matching assistant for Galaxy Plastics, a PVC fittings
# and waterworks manufacturer.

# A customer will describe what they need. Your job is to find the best
# matching product from the provided context.

# IMPORTANT RULES:

# - Use ONLY the product context provided.
# - Return ONLY valid JSON. No markdown or explanations.
# - Never invent products or URLs.
# - Always copy the Product URL exactly from the context.
# - If a matching product exists, product_url MUST not be empty.
# - If the customer request is vague, unclear, or missing important details,
#   do NOT guess a product. Return null values and ask for more information.
# - If multiple products could match and you cannot confidently choose one,
#   return null values and explain what information is needed.

# Examples of vague requests:
# "I need a product"
# "I need help"
# "I need something for pipes"
# "Show me your products"

# For vague requests, respond:

# {{
# "product_name": null,
# "product_url": null,
# "category": null,
# "reason": "Please provide more details about your application, such as drainage, sewer, municipal water, irrigation, plumbing, or industrial use."
# }}


# If a product is found, return exactly:

# {{
# "product_name": "...",
# "product_url": "...",
# "category": "...",
# "reason": "one sentence explaining why this product fits"
# }}


# If no reasonable match exists, return:

# {{
# "product_name": null,
# "product_url": null,
# "category": null,
# "reason": "Explain what information is missing and suggest contacting a sales representative."
# }}


# PRODUCT CONTEXT:
# {context}


# CUSTOMER REQUEST:
# {question}


# JSON RESPONSE:
# """
# )

# CATEGORY_KEYWORDS = {
#     "Municipal": [
#         "sewer",
#         "backflow",
#         "municipal",
#         "water main",
#         "c900",
#         "backwater"
#     ],

#     "Drainage": [
#         "drain",
#         "stormwater",
#         "pooling",
#         "runoff",
#         "basin"
#     ],

#     "Corrosion Control": [
#         "corrosion",
#         "rust",
#         "anode",
#         "buried metal"
#     ],

#     "Irrigation & Agriculture": [
#         "irrigation",
#         "agriculture",
#         "field",
#         "crop"
#     ],

#     "Plumbing & Industrial": [
#         "plumbing",
#         "dwv",
#         "industrial",
#         "solvent weld"
#     ],
# }


# def is_vague_query(question: str) -> bool:
#     vague_words = [
#         "product",
#         "something",
#         "anything",
#         "help",
#         "need help",
#         "looking for",
#         "what do you sell",
#         "recommend something"
#     ]

#     q = question.lower().strip()

#     return (
#         len(q.split()) <= 3
#         or any(word in q for word in vague_words)
#     )

# def guess_category(question: str) -> Optional[str]:
#     q = question.lower()

#     for category, keywords in CATEGORY_KEYWORDS.items():
#         if any(keyword in q for keyword in keywords):
#             return category

#     return None



# class BotMatch(TypedDict):
#     product_name: Optional[str]
#     product_url: Optional[str]
#     category: Optional[str]
#     reason: str



# _vectorstore = None



# def _load_products() -> list[dict]:
#     with open(PRODUCTS_PATH, encoding="utf-8") as f:
#         return json.load(f)



# def _get_vectorstore():

#     global _vectorstore

#     if _vectorstore is None:

#         products = _load_products()

#         docs = [
#             Document(

#                 page_content=(
#                     f"Product Name: {p['name']}\n"
#                     f"Category: {p['category']}\n"
#                     f"Product URL: {p['url']}\n"
#                     f"Description: {p['description']}"
#                 ),

#                 metadata={
#                     "id": p["id"],
#                     "name": p["name"],
#                     "url": p["url"],
#                     "category": p["category"],
#                 }
#             )

#             for p in products
#         ]


#         _vectorstore = Chroma.from_documents(
#             docs,
#             OpenAIEmbeddings()
#         )


#     return _vectorstore




# def _retrieve(question: str, k: int = 5):

#     vectorstore = _get_vectorstore()

#     category = guess_category(question)


#     if category:

#         return vectorstore.similarity_search(
#             question,
#             k=k,
#             filter={
#                 "category": category
#             }
#         )


#     return vectorstore.similarity_search(
#         question,
#         k=k
#     )




# def _build_chain():

#     llm = ChatOpenAI(
#         model="gpt-4o-mini",
#         temperature=0
#     )


#     def retrieve_and_format(inputs: dict):

#         docs = _retrieve(
#             inputs["question"]
#         )


#         context = "\n\n".join(

#             f"""
# Product Name:
# {doc.metadata.get("name")}

# Category:
# {doc.metadata.get("category")}

# Product URL:
# {doc.metadata.get("url")}

# Description:
# {doc.page_content}
# """

#             for doc in docs

#         )


#         return {
#             "context": context,
#             "question": inputs["question"]
#         }



#     return (
#         RunnableLambda(retrieve_and_format)
#         | PROMPT
#         | llm
#         | StrOutputParser()
#     )




# def parse_bot_output(raw: str) -> BotMatch:

#     try:

#         parsed = json.loads(raw)


#     except json.JSONDecodeError:

#         return {

#             "product_name": None,
#             "product_url": None,
#             "category": None,
#             "reason":
#                 "Sorry, I couldn't parse a match. Please contact a sales representative."
#         }



#     return {

#         "product_name": parsed.get("product_name"),

#         "product_url": parsed.get("product_url"),

#         "category": parsed.get("category"),

#         "reason": parsed.get("reason", "")
#     }




# async def ask_bot(question: str) -> BotMatch:

#     chain = _build_chain()

#     raw = await chain.ainvoke(
#         {
#             "question": question
#         }
#     )


#     return parse_bot_output(raw)









#  working




"""
Product-matching RAG pipeline: embeds the Galaxy Plastics product catalog
into a Chroma vector store. Retrieves relevant products and lets the LLM
select the best match with structured JSON output.
"""

import json
from pathlib import Path
from typing import Optional, TypedDict

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda


PRODUCTS_PATH = Path(__file__).parent.parent / "data" / "products.json"

PROMPT = PromptTemplate.from_template(
    """
You are a product-matching assistant for Galaxy Plastics, a PVC fittings
and waterworks manufacturer.

A customer will describe what they need. Your job is to find the best
matching product from the provided context.

IMPORTANT RULES:

- Use ONLY the product context provided.
- Return ONLY valid JSON. No markdown or explanations.
- Never invent products or URLs.
- Always copy the Product URL exactly from the context.
- If a matching product exists, product_url MUST not be empty.
- If the customer request is vague, unclear, or missing important details,
  do NOT guess a product. Return null values and ask for more information.
- If multiple products could match and you cannot confidently choose one,
  return null values and explain what information is needed.

Examples of vague requests:
"I need a product"
"I need help"
"I need something for pipes"
"Show me your products"

For vague requests, respond:

{{
"product_name": null,
"product_url": null,
"category": null,
"reason": "Please provide more details about your application, such as drainage, sewer, municipal water, irrigation, plumbing, or industrial use."
}}


If a product is found, return exactly:

{{
"product_name": "...",
"product_url": "...",
"category": "...",
"reason": "one sentence explaining why this product fits"
}}


If no reasonable match exists, return:

{{
"product_name": null,
"product_url": null,
"category": null,
"reason": "Explain what information is missing and suggest contacting a sales representative."
}}


PRODUCT CONTEXT:
{context}


CUSTOMER REQUEST:
{question}


JSON RESPONSE:
"""
)

CATEGORY_KEYWORDS = {
    "Municipal": [
        "sewer",
        "backflow",
        "municipal",
        "water main",
        "c900",
        "backwater"
    ],

    "Drainage": [
        "drain",
        "stormwater",
        "pooling",
        "runoff",
        "basin"
    ],

    "Corrosion Control": [
        "corrosion",
        "rust",
        "anode",
        "buried metal"
    ],

    "Irrigation & Agriculture": [
        "irrigation",
        "agriculture",
        "field",
        "crop"
    ],

    "Plumbing & Industrial": [
        "plumbing",
        "dwv",
        "industrial",
        "solvent weld"
    ],
}


def is_vague_query(question: str) -> bool:
    vague_words = [
        "product",
        "something",
        "anything",
        "help",
        "need help",
        "looking for",
        "what do you sell",
        "recommend something"
    ]

    q = question.lower().strip()

    return (
        len(q.split()) <= 3
        or any(word in q for word in vague_words)
    )

def guess_category(question: str) -> Optional[str]:
    q = question.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in q for keyword in keywords):
            return category

    return None



class BotMatch(TypedDict):
    product_name: Optional[str]
    product_url: Optional[str]
    category: Optional[str]
    reason: str



_vectorstore = None



def _load_products() -> list[dict]:
    with open(PRODUCTS_PATH, encoding="utf-8") as f:
        return json.load(f)



def _get_vectorstore():

    global _vectorstore

    if _vectorstore is None:

        products = _load_products()

        docs = [
            Document(

                page_content=(
                    f"Product Name: {p['name']}\n"
                    f"Category: {p['category']}\n"
                    f"Product URL: {p['url']}\n"
                    f"Description: {p['description']}"
                ),

                metadata={
                    "id": p["id"],
                    "name": p["name"],
                    "url": p["url"],
                    "category": p["category"],
                }
            )

            for p in products
        ]


        _vectorstore = Chroma.from_documents(
            docs,
            OpenAIEmbeddings()
        )


    return _vectorstore




def _retrieve(question: str, k: int = 5):

    vectorstore = _get_vectorstore()

    category = guess_category(question)


    if category:

        return vectorstore.similarity_search(
            question,
            k=k,
            filter={
                "category": category
            }
        )


    return vectorstore.similarity_search(
        question,
        k=k
    )




def _build_chain():

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )


    def retrieve_and_format(inputs: dict):

        docs = _retrieve(
            inputs["question"]
        )


        context = "\n\n".join(

            f"""
Product Name:
{doc.metadata.get("name")}

Category:
{doc.metadata.get("category")}

Product URL:
{doc.metadata.get("url")}

Description:
{doc.page_content}
"""

            for doc in docs

        )


        return {
            "context": context,
            "question": inputs["question"]
        }



    return (
        RunnableLambda(retrieve_and_format)
        | PROMPT
        | llm
        | StrOutputParser()
    )




def parse_bot_output(raw: str) -> BotMatch:

    try:

        parsed = json.loads(raw)


    except json.JSONDecodeError:

        return {

            "product_name": None,
            "product_url": None,
            "category": None,
            "reason":
                "Sorry, I couldn't parse a match. Please contact a sales representative."
        }



    return {

        "product_name": parsed.get("product_name"),

        "product_url": parsed.get("product_url"),

        "category": parsed.get("category"),

        "reason": parsed.get("reason", "")
    }

def is_vague_query(question: str) -> bool:
    vague_words = [
        "product",
        "something",
        "anything",
        "help",
        "need something",
        "what do you sell",
        "show me products"
    ]

    q = question.lower().strip()

    if len(q.split()) <= 2:
        return True

    return any(word in q for word in vague_words)

async def ask_bot(question: str) -> BotMatch:

    # Handle vague questions first
    if is_vague_query(question):
        return {
            "product_name": None,
            "product_url": None,
            "category": None,
            "reason": (
                "Could you provide more details about what you need? "
                "For example, are you looking for drainage, sewer, "
                "municipal, plumbing, irrigation, or corrosion control products?"
            )
        }

    # Retrieve matching products
    docs = _retrieve(question)

    # Run LLM chain
    chain = _build_chain()

    raw = await chain.ainvoke(
        {
            "question": question
        }
    )

    result = parse_bot_output(raw)


    # Guarantee URL from retrieved metadata
    if result["product_name"] and not result["product_url"]:

        for doc in docs:
            if (
                doc.metadata.get("name","").lower()
                == result["product_name"].lower()
            ):
                result["product_url"] = doc.metadata.get("url")
                break


    # Extra fallback if name matching fails
    if result["product_name"] and not result["product_url"]:

        if docs:
            result["product_url"] = docs[0].metadata.get("url")


    return result

async def ask_bot(question: str) -> BotMatch:
    docs = _retrieve(question)

    print("\n--- RETRIEVED DOCS ---")
    for d in docs:
        print(d.metadata)
        print(d.page_content[:300])
        print("----------------")

    chain = _build_chain()
    raw = await chain.ainvoke({"question": question})
    return parse_bot_output(raw)















