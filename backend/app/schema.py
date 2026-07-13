import json
from pathlib import Path
from typing import Optional

import strawberry

from app.langchain_chain.chain import ask_bot as run_bot_chain


FAQ_PATH = Path(__file__).parent / "data" / "faqs.json"


def _load_faqs() -> list[dict]:
    with open(FAQ_PATH, encoding="utf-8") as f:
        return json.load(f)


@strawberry.type
class FAQ:
    id: strawberry.ID
    product: str
    question: str
    answer: str


@strawberry.type
class BotResponse:
    product_name: Optional[str]
    product_url: Optional[str]
    category: Optional[str]
    reason: str


@strawberry.type
class Query:

    @strawberry.field
    def faqs(self, product: Optional[str] = None) -> list[FAQ]:
        data = _load_faqs()

        if product:
            data = [
                faq for faq in data
                if faq["product"].lower() == product.lower()
            ]

        return [
            FAQ(
                id=faq["id"],
                product=faq["product"],
                question=faq["question"],
                answer=faq["answer"],
            )
            for faq in data
        ]


    @strawberry.field
    def faq(self, id: strawberry.ID) -> Optional[FAQ]:
        data = _load_faqs()

        match = next(
            (faq for faq in data if faq["id"] == str(id)),
            None
        )

        if not match:
            return None

        return FAQ(
            id=match["id"],
            product=match["product"],
            question=match["question"],
            answer=match["answer"],
        )


    @strawberry.field
    async def ask_bot(self, question: str) -> BotResponse:

        result = await run_bot_chain(question)

        return BotResponse(
            product_name=result.get("product_name"),
            product_url=result.get("product_url"),
            category=result.get("category"),
            reason=result.get("reason", ""),
        )


schema = strawberry.Schema(query=Query)