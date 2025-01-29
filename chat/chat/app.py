import gradio as gr
import anthropic
import json
import os
from datetime import datetime, timedelta
from api_client import SmartHotelAPI

class SmartHotelChat:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.api = SmartHotelAPI()
        
        # Define the available tools
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_room_data",
                    "description": "Get the latest sensor data for a hotel room",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "room_id": {
                                "type": "integer",
                                "description": "The ID of the room"
                            }
                        },
                        "required": ["room_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_energy_summary",
                    "description": "Get energy consumption summary for a hotel",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "hotel_id": {
                                "type": "integer",
                                "description": "The ID of the hotel"
                            },
                            "resolution": {
                                "type": "string",
                                "enum": ["1hour", "1day", "1month"],
                                "description": "Time resolution for the data"
                            },
                            "subsystem": {
                                "type": "string",
                                "enum": ["ac", "lighting", "plug_load"],
                                "description": "Filter by specific subsystem"
                            }
                        },
                        "required": ["hotel_id"]
                    }
                }
            }
        ]

    def handle_function_call(self, function_call):
        function_name = function_call['name']
        arguments = json.loads(function_call['arguments'])
        
        if function_name == "get_room_data":
            return self.api.get_room_data(arguments['room_id'])
        elif function_name == "get_energy_summary":
            return self.api.get_energy_summary(
                hotel_id=arguments['hotel_id'],
                resolution=arguments.get('resolution', '1hour'),
                subsystem=arguments.get('subsystem')
            )
        
        raise ValueError(f"Unknown function: {function_name}")

    def chat(self, message, history):
        messages = []
        
        # Convert history to Anthropic format
        for human, assistant in history:
            messages.append({"role": "user", "content": human})
            messages.append({"role": "assistant", "content": assistant})
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        # Get response from Claude
        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            messages=messages,
            tools=self.tools,
            max_tokens=1024,
            temperature=0
        )
        
        # Handle any function calls
        message = response.content[0].text
        if response.content[0].tool_calls:
            for tool_call in response.content[0].tool_calls:
                result = self.handle_function_call(tool_call.function)
                
                # Add function result to conversation
                messages.append({
                    "role": "assistant",
                    "content": message
                })
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": json.dumps(result)
                })
                
                # Get final response
                final_response = self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    messages=messages,
                    max_tokens=1024,
                    temperature=0
                )
                message = final_response.content[0].text
        
        return message

    def create_interface(self):
        return gr.ChatInterface(
            self.chat,
            chatbot=gr.Chatbot(height=600),
            textbox=gr.Textbox(placeholder="Ask about room conditions or energy usage...", container=False),
            title="Smart Hotel Assistant",
            description="I can help you check room conditions and energy usage data.",
            theme="soft"
        )

if __name__ == "__main__":
    chat = SmartHotelChat()
    demo = chat.create_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860) 