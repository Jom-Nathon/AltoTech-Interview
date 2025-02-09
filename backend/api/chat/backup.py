from __future__ import annotations as _annotations

import os
from dataclasses import dataclass
from .config import settings

import httpx
import logfire
from pydantic_ai import Agent, ModelRetry, RunContext
# from pydantic_ai.messages import ModelMessage, ModelResponse, TextPart
# from pydantic_ai.models.openai import OpenAIModel
# from devtools import debug
from pydantic_ai.models.anthropic import AnthropicModel
import pandas as pd


# model = OpenAIModel(
#     "deepseek/deepseek-chat",
#     base_url = 'https://openrouter.ai/api/v1',
#     api_key = os.getenv('OPEN_ROUTER_API_KEY')
# )


logfire.configure(send_to_logfire='if-token-present')

@dataclass
class AllHotel:
    endpoint: str = "http://localhost:8000/hotels/"

@dataclass
class FloorList:
    hotel_id: str
    endpoint: str = None
    def __post_init__(self):
        if self.endpoint is None:
            self.endpoint = f"http://localhost:8000/hotels/{self.hotel_id}/floors/"
@dataclass
class RoomList:
    floor_id: str
    endpoint: str = None
    def __post_init__(self):
        if self.endpoint is None:
            self.endpoint = f"http://localhost:8000/floors/{self.floor_id}/rooms/"
@dataclass
class RoomData:
    room_id: str
    endpoint: str = None

    def __post_init__(self):
        if self.endpoint is None:
            self.endpoint = f"http://localhost:8000/rooms/{self.room_id}/data/"
@dataclass
class RoomDataIAQ:
    room_id: str
    endpoint: str = None
    def __post_init__(self):
        if self.endpoint is None:
            self.endpoint = f"http://localhost:8000/rooms/{self.room_id}/data/iaq/"
@dataclass
class RoomDataLifeBeing:
    room_id: str
    endpoint: str = None
    def __post_init__(self):
        if self.endpoint is None:
            self.endpoint = f"http://localhost:8000/rooms/{self.room_id}/data/life_being/"
@dataclass
class PowerMeterData:
    hotel_id: str
    meter_type: str
    endpoint: str = None
    
    def __post_init__(self):
        if self.endpoint is None:
            self.endpoint = f"http://localhost:8000/hotels/{self.hotel_id}/energy_summary/"

system_prompt = """
You are a virtual assistance with access to smart hotel api to help inform the user about the hotel information that have installed AltoTech smart hotel system. This may include the hotel information about the hotel, room information, life sensor data, iaq sensor data and the power usage data.

AltoTech smart hotel system is a system with sensors installed in the hotel to collect data and send to the cloud. Each hotel has multiple floors and rooms. In every room, there are 2 sensors installed to collect data, one for life sensor and one for iaq sensor. Lastly, each hotel has a power meter installed inside a special room called power room.

The power meter data is seperated by meter type, which is either AC, lighting, plug load or total. Only provide the data that the user asked for.

Your only job is to assist with this and you don't answer other questions besides describing what you are able to do.

Don't ask the user before taking an action, just do it. Always make sure you look at the database or api with the provided tools before answering the user's question unless you have already.

When answering a question about the sensor data or room information, always start your answer with the provided sensor data or room information first and then give your answer on a newline. Like:

[Sensor data/Room information]

Your answer here...

When answering a question about the power usage, always start your answer with the URL link to download CSV. Then type out the csv file in easy to read format on a new line. Lastly give your answer on a last line. Like:

[Link to download power meter data]

[CSV file typed out in easy to read format]

Your answer here...

Also, when user didn't ask for a specific meter type, always provide the total meter data by combining all the meter type energy usage and call the new row total. The energy usage is in kW/h.

When user specify the resolution, only provide the data that match the resolution.

Lastly, when user specify that they need end time and start time for the power meter data, always provide the data in the same format as timestamp. That data should be in new row and remove timestamp.

Start time is always timestamp-resolution. End time is always timestamp.
"""

model = AnthropicModel('claude-3-5-sonnet-latest', api_key=settings.ANTROPIC_API_KEY)

async def get_hotels(ctx: RunContext[AllHotel]) -> str:

    async with httpx.AsyncClient() as client:
        response = await client.get(ctx.deps.endpoint)
        return response.json()
    
async def get_floor_list(ctx: RunContext[FloorList]) -> str:

    async with httpx.AsyncClient() as client:
        response = await client.get(ctx.deps.endpoint)
        return response.json()

async def get_room_list(ctx: RunContext[RoomList]) -> str:

    async with httpx.AsyncClient() as client:
        response = await client.get(ctx.deps.endpoint)
        return response.json()

async def get_room_data(ctx: RunContext[RoomData]) -> str:

    async with httpx.AsyncClient() as client:
        response = await client.get(ctx.deps.endpoint)
        return response.json()

async def get_room_iaq(ctx: RunContext[RoomDataIAQ]) -> str:

    async with httpx.AsyncClient() as client:
        response = await client.get(ctx.deps.endpoint)
        return response.json()

async def get_room_life_being(ctx: RunContext[RoomDataLifeBeing]) -> str:

    async with httpx.AsyncClient() as client:
        response = await client.get(ctx.deps.endpoint)
        return response.json()

async def get_power_meter_data(ctx: RunContext[PowerMeterData]):

    response = pd.read_csv(ctx.deps.endpoint)
    link = str(ctx.deps.endpoint)
    return f"{link}\n{response.to_string()}"

smart_hotel_agent = Agent(
    model,
    system_prompt=system_prompt,
    deps_type=[AllHotel, FloorList, RoomList, RoomData, RoomDataIAQ, RoomDataLifeBeing, PowerMeterData],
    tools=[
        get_hotels,
        get_floor_list,
        get_room_list,
        get_room_data,
        get_room_iaq,
        get_room_life_being,
        get_power_meter_data
    ],
    retries=2
)

class Chat:

    def get_deps_for_query(self, query: str):
        """Determine which dependency to use based on the query"""
        query = query.lower()
        words = query.split()
        
            # Look for specific identifiers
        room_id = next((
            words[i+1] for i, word in enumerate(words) 
            if word == "room" and i+1 < len(words) and words[i+1].isdigit()
        ), "101")
        
        floor_id = next((
            words[i+1] for i, word in enumerate(words) 
            if word == "floor" and i+1 < len(words) and words[i+1].isdigit()
        ), "1")
        
        hotel_id = next((
            words[i+1] for i, word in enumerate(words) 
            if word == "hotel" and i+1 < len(words) and words[i+1].isdigit()
        ), "1")

        if 'iaq' in query or 'air quality' in query:
            return RoomDataIAQ(room_id=room_id)
        
        if 'life' in query or 'occupancy' in query:
            return RoomDataLifeBeing(room_id=room_id)
            
        if 'room data' in query or 'room information' in query:
            return RoomData(room_id=room_id)
        
        if 'room list' in query or 'room number' in query or 'room information' in query:
            return RoomList(floor_id=floor_id)
            
        if 'floor' in query:
            return FloorList(hotel_id=hotel_id)
            
        if 'power' in query or 'energy' in query:
            return PowerMeterData(hotel_id=hotel_id, meter_type="total")
            
        # Default to AllHotel for general queries
        return AllHotel()

    # async def process_message(self, message:str):
    #     deps = self.get_deps_for_query(message)
    #     result = await smart_hotel_agent.run(
    #                     message,
    #                     deps=deps
    #         )
    #     return result.data
                
    #             if user_input.lower() in ['exit', 'quit', 'q']:
    #                 print("\nGoodbye!")
    #                 break

    #             if not user_input:
    #                 print("Please type something!")
    #                 continue

    #             deps = self.get_deps_for_query(user_input)
    #             print("\nThinking...")
                
    #             

    #             print("\nAssistant:", result.data)

    #         except Exception as e:
    #             print(f"\nError: {str(e)}")
    #             print("Please try again or type 'exit' to quit.")

# async def main():
#     chat = Chat()
#     await chat.chat()

# if __name__ == '__main__':
#     asyncio.run(main())
