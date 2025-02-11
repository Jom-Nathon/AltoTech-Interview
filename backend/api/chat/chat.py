from __future__ import annotations as _annotations

import asyncio, json
from dataclasses import dataclass
from .config import settings
from .intent_classifier import intent_classifier
from django.db import connections
from asgiref.sync import sync_to_async

import httpx
import logfire
from pydantic_ai import Agent, RunContext
# from pydantic_ai.messages import ModelMessage, ModelResponse, TextPart
# from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.anthropic import AnthropicModel
import pandas as pd


# model = OpenAIModel(
#     "deepseek/deepseek-chat",
#     base_url = 'https://openrouter.ai/api/v1',
#     api_key = os.getenv('OPEN_ROUTER_API_KEY')
# )

logfire.configure(send_to_logfire='if-token-present')

@dataclass
class supportDependencies:
    hotel_id: str = "1"
    floor_id: str = "all"
    room_id: str = "all"

    # def __init__(self, intent: str):
    #     self.intent = intent
    #     seperated_intent = self.intent.split(" ")
    #     for block in seperated_intent:
    #         if "parameters" in block:
    #             pattern = r'<parameters>(.*?)</parameters>'
    #             match = re.search(pattern, block)
    #             if match:
    #                 splited_parameters = match.group(1).split(",")
    #                 for parameter in splited_parameters:
    #                     if "hotel_id" in parameter:
    #                         self.hotel_id = parameter.split(":")[1]
    #                     elif "floor_id" in parameter:
    #                         self.floor_id = parameter.split(":")[1]
    #                     elif "room_id" in parameter:
    #                         self.room_id = parameter.split(":")[1]


    # "http://localhost:8000/hotels/"
    # f"http://localhost:8000/hotels/{self.hotel_id}/floors/"
    # f"http://localhost:8000/floors/{self.floor_id}/rooms/"

    # f"http://localhost:8000/rooms/{self.room_id}/data/"
    # f"http://localhost:8000/rooms/{self.room_id}/data/iaq/"
    # f"http://localhost:8000/rooms/{self.room_id}/data/life_being/"
    # f"http://localhost:8000/hotels/{self.hotel_id}/energy_summary/"


system_prompt = """
You are a female ai assistant. Your name is AltoTech Assistant created by the company AltoTech.
Your goal will be to provide user with the requested information according to the provided tools and intent.
You should always maintain friendly and professional tone in your response.
If the information is not available or not found, just say so. Don't make up an answer.
Dont explain the answer, just provide the datapoints.
You will be provided with a list of tools and parameters to be used in order. Sometimes the parameters that was provided will not be enough to get the information.
There are 2 types of sensor. First is IAQ sensor that is used to measure the temperature, humidity and co2. Second is life being sensor that is used to measure the occupancy, online status and sensitivity.
When user ask for power summary. Answer with download link first and then your answer. If the answer is too long, summerize your answer from the datapoints.

Example:
User: can you give me power summary for hotel 1?
Assistant: Download link: http://localhost:8000/hotels/1/energy_summary/
Recent power consumption data for Hotel 1 shows: - AC consumption ranging from 9.97 to 10.02 kWh - Lighting usage between 9.87 to 10.10 kWh - Plug load varying from 9.87 to 10.02 kWh The consumption patterns appear relatively stable across all three categories over the reported period.

User: can you give me power summary for hotel 1? But only for the month of January 2025 and the resolution is daily.
Assistant: Download link: http://localhost:8000/hotels/1/energy_summary/?resolution=daily&subsystem=all&start_date=2025-01-01T00:00:00Z&end_date=2025-01-31T00:00:00Z
Recent power consumption data for Hotel 1 shows: - AC consumption ranging from 9.97 to 10.02 kWh - Lighting usage between 9.87 to 10.10 kWh - Plug load varying from 9.87 to 10.02 kWh The consumption patterns appear relatively stable across all three categories over the reported period.

How do you respond to the user's question?
Think about your answer first before you respond.
"""


model = AnthropicModel('claude-3-5-sonnet-latest', api_key=settings.ANTROPIC_API_KEY)

smart_hotel_agent = Agent(
    model,
    system_prompt=system_prompt,
    # deps_type=[supportDependencies],
    retries=3
)

@smart_hotel_agent.tool_plain
async def get_all_hotels() -> str:
    @sync_to_async
    def db_query():
        with connections['default'].cursor() as cursor:
            base_query = """
                SELECT * FROM hotel
            """
            cursor.execute(base_query)
            return cursor.fetchall()
    data = await db_query()
    return json.dumps(data)
    
@smart_hotel_agent.tool_plain
async def get_floors() -> str:
    @sync_to_async
    def db_query():
        with connections['default'].cursor() as cursor:
            base_query = """
                SELECT * FROM floor
            """
            cursor.execute(base_query)
            return cursor.fetchall()
    data = await db_query()
    return json.dumps(data)


@smart_hotel_agent.tool_plain
async def get_rooms() -> str:
    @sync_to_async
    def db_query():
        with connections['default'].cursor() as cursor:
            base_query = """
                SELECT * FROM room
            """
            cursor.execute(base_query)
            return cursor.fetchall()
    data = await db_query()
    return json.dumps(data)

@smart_hotel_agent.tool_plain
async def get_current_sensor_data(room_id: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/rooms/{room_id}/data/")
        return response.json()
    
@smart_hotel_agent.tool_plain
async def get_historical_sensor_data(device_id: str, time_range: str = '24h') -> str:
    @sync_to_async
    def db_query():
        with connections['timescaledb'].cursor() as cursor:
            bucket_width = '1 hour'

            base_query = """
                WITH stats AS (
                    SELECT 
                        time_bucket(%s, date_time) AS bucket,
                        device_id,
                        datapoint,
                        avg(CAST(value AS FLOAT)) AS mean
                    FROM raw_data
                    WHERE device_id = %s
                    AND date_time >= NOW() - %s::interval
                    GROUP BY bucket, device_id, datapoint
                    ORDER BY bucket DESC
                )
                SELECT 
                    bucket,
                    device_id,
                    datapoint,
                    mean
                FROM stats
            """

            try:
                cursor.execute(base_query, [
                    bucket_width,
                    device_id,
                    time_range
                ])
                
                # Convert results to structured format
                results = {}
                columns = [col[0] for col in cursor.description]
                for row in cursor.fetchall():
                    row_dict = dict(zip(columns, row))
                    bucket_str = row_dict['bucket'].isoformat()
                    
                    if bucket_str not in results:
                        results[bucket_str] = {}
                    
                    results[bucket_str][row_dict['datapoint']] = row_dict['mean']

                return {
                    'time_range': time_range,
                    'bucket_width': bucket_width,
                    'device_id': device_id,
                    'data': results
                }


            except Exception as e:
                print(f"Database error: {str(e)}")
                return None

    data = await db_query()
    return json.dumps(data)

@smart_hotel_agent.tool_plain
async def get_powermeter_from_hotel(hotel_id: str, resolution: str, start_date: str, end_date: str, subsystem: str) -> str:

    valid_subsystems = ['ac', 'lighting', 'plug_load', 'all']
    if subsystem not in valid_subsystems:
        return "Invalid subsystem. Please choose from: ac, lighting, plug_load or all"
    
    valid_resolutions = ['daily', 'monthly', 'yearly']
    if resolution not in valid_resolutions:
        return "Invalid resolution. Please choose from: daily, monthly, yearly"

    if start_date and end_date:
        link = str(f"http://localhost:8000/hotels/{hotel_id}/energy_summary/?resolution={resolution}&start_date={start_date}&end_date={end_date}&subsystem={subsystem}")
    else:
        link = str(f"http://localhost:8000/hotels/{hotel_id}/energy_summary/?resolution={resolution}&subsystem={subsystem}")
    response = pd.read_csv(link)
    return f"<CSV_link>{link}</CSV_link>", response.to_string()


# async def get_tool_order(user_input: str) -> dict:
#     intent = await intent_classifier.run(user_input)
#     tasks = intent.data.split(" ")

#     for task in tasks:
#         if "parameters" in task:
#             pattern = r'<parameters>(.*?)</parameters>'
#             match = re.search(pattern, task)
#             if match:
#                 return match.group(1)  # Returns 'hotel_id:1'
#             return ''
#             return tool, parameters
#         else:
#             return task

# class Chat:
#     async def process_message():
#         # intent = await intent_classifier.run("hello can you give me energy summary of hotel 1?")
#         deps = supportDependencies()
#         result = await smart_hotel_agent.run(
#                         "hello can you give me energy summary of hotel 1?",
#                         deps=deps
#                 )
#         print(result.data)
# async def main():
#     await Chat.process_message()

# if __name__ == '__main__':
#     asyncio.run(main())
