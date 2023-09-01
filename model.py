import json

import aiohttp
from motor.motor_asyncio import AsyncIOMotorClient

from utils import Conversation

class Model:
    def __init__(self, mongo_db_url, mongo_db_name, model_server_url):
        self.model_server_url = model_server_url
        self.db_collection = AsyncIOMotorClient(mongo_db_url)[mongo_db_name]
        self.db_collection.messages.create_index([("user_id", 1)])
        self.db_collection.messages.create_index([("mes_is", 1)])
        self.db_collection.reports.create_index([("user_id", 1)])
        self.db_collection.reports.create_index([("mes_is", 1)])

    async def clear_context(self, user_id, mes_is):
        await self.db_collection.messages.insert_one({
            "user_id": user_id,
            "mes_is": mes_is,
            "role": "clear",
            "content": "",
        })

    async def ask(self, user_id, mes_is, question):
        await self.db_collection.messages.insert_one({
            "user_id": user_id,
            "mes_is": mes_is,
            "role": "user",
            "content": question,
        })

        mes = self.db_collection.messages.find(
            { "user_id": user_id, "mes_is": mes_is }).to_list(None)
        prompt = Conversation(mes).get_prompt()

        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url=self.model_server_url + "complete/",
                json=json.dumps(prompt)
            )
            answer = (await response.json(encoding='UTF-8'))["text"]
    
        await self.db_collection.messages.insert_one({
            "user_id": user_id,
            "mes_is": mes_is,
            "role": "bot",
            "content": answer,
        })
        return answer
    
    async def report(self, user_id, mes_is, is_like=True, is_harmful=False,
               is_lie=False, is_useless=False, comment=""):
        await self.db_collection.reports.insert_one({
            "user_id": user_id,
            "mes_is": mes_is,
            "is_like": is_like,
            "is_harmful": is_harmful,
            "is_lie": is_lie,
            "is_useless": is_useless,
            "comment": comment
        })

    async def get_metrics(self):
        metrics = {
            "Share of positive reviews": 0,
            "Share of negative reviews": 0,
            "Number of messages from users": 0,
        }

        messages = await self.db_collection.messages.find().to_list(None)
        reports = await self.db_collection.reports.find().to_list(None)

        metrics["Number of messages from users"] = len(
            [1 for mes in messages if mes["type"] == "user"])
        
        reports = { f"{rep['user_id']}/{rep['mes_is']}": rep['is_like']
                   for rep in reports } # Учтем послений отзыв пользователя

        metrics["Share of positive reviews"] = len(
            [1 for rep in reports.values() if rep]) / len(reports)

        metrics["Share of negative reviews"] = len(
            [1 for rep in reports.values() if not rep]) / len(reports)

        return metrics
