from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic import Field
from dataclasses import dataclass
# from .config import settings
import asyncio
import logfire

logfire.configure(send_to_logfire='if-token-present')

model = AnthropicModel('claude-3-5-sonnet-latest', api_key='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')


Intent_classifier_prompt =("""
                            You are an assistant agent that will be given a question and you need to classify the intent of the question.
                            The intent should be one or more of the following options:
                            options: <get_all_hotels>, <get_floors_from_hotel>, <get_rooms_from_floor>, <get_sensor_from_room>, <get_iaq_from_room>, <get_lifebeing_from_room>, <get_powermeter_from_hotel>
                            Don't explain how you got the answer, just provide the answer.
                            You need to think logically how to get to the answer from the question.                          
                            If the question is not related to the options. Answer with <no_tool>
                            You will also have to collect the parameters for the tool if needed.
                            For example:
                                <example>
                                    Question: "Hello can i get list of all rooms in floor 2 of hotel 1?"
                                    Answer:<get_all_hotels> <get_floors_from_hotel> <parameters>hotel_id:1,floor_id:2</parameters>
                                </example>
                                <example>
                                    Question: "Provide me list of all rooms in hotel 1?"
                                    Answer:<get_all_hotels> <get_floors_from_hotel> <get_rooms_from_floor> <parameters>hotel_id:1</parameters>
                                </example>
                                In this example user did not provide floor id so we need to get all floors from hotel 1 first and then get all rooms from all floors.
                                <example>
                                    Question: "Hello can i get latest data of all rooms in floor 2?"
                                    Answer:<get_rooms_from_floor> <get_sensor_from_room> <parameters>floor_id:2</parameters>
                                </example>
                                <example>
                                    Question: "give me the detailed energy summary of hotel 1"
                                    Answer:<get_powermeter_from_hotel> <parameters>hotel_id:1</parameters>
                                </example>
                            Again, you need to think logically since each tool has its own parameters and to get the answer you might need to use multiple tools in the correct order.

""")

intent_classifier = Agent(
    model,
    system_prompt=Intent_classifier_prompt,
    result_tool_name='user_intent',
    result_tool_description="Log the user's intent action and whether it is valid",
    retries=3
)

# @intent_classifier.result_validator
# def validate_intent(ctx: RunContext[None], result: Intent) -> Intent:
#     if result.tool not in ['get_all_hotels', 'get_floors_from_hotel', 'get_rooms_from_floor', 'get_sensor_from_room', 'get_iaq_from_room', 'get_lifebeing_from_room', 'get_powermeter_from_hotel', 'no_tool']:
#         raise ModelRetry("Invalid intent, please choose from `get_all_hotels`, `get_floors_from_hotel`, `get_rooms_from_floor`, `get_sensor_from_room`, `get_iaq_from_room`, `get_lifebeing_from_room`, `get_powermeter_from_hotel`, `no_tool`")
#     return result


# class Chat:
#     async def process_message():
#         result = await intent_classifier.run(
#                         "ขอดูข้อมูลห้องในชั้น 2",
#                 )
#         print(result.data)
     

# async def main():
#     await Chat.process_message()

# if __name__ == '__main__':
#     asyncio.run(main())
