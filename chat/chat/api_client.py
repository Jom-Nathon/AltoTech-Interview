import requests
from datetime import datetime, timedelta
import os

class SmartHotelAPI:
    def __init__(self):
        self.base_url = os.getenv('BACKEND_URL', 'http://backend:8000/api')

    def get_room_data(self, room_id):
        """Get latest sensor data for a room"""
        response = requests.get(f"{self.base_url}/rooms/{room_id}/data/")
        response.raise_for_status()
        return response.json()

    def get_room_iaq_data(self, room_id):
        """Get latest IAQ sensor data for a room"""
        response = requests.get(f"{self.base_url}/rooms/{room_id}/iaq/")
        response.raise_for_status()
        return response.json()

    def get_room_life_being_data(self, room_id):
        """Get latest Life Being sensor data for a room"""
        response = requests.get(f"{self.base_url}/rooms/{room_id}/life_being/")
        response.raise_for_status()
        return response.json()

    def get_energy_summary(self, hotel_id, resolution='1hour', subsystem=None, 
                         start_time=None, end_time=None):
        """Get energy consumption summary for a hotel"""
        params = {'resolution': resolution}
        if subsystem:
            params['subsystem'] = subsystem
        if start_time:
            params['start_time'] = start_time
        if end_time:
            params['end_time'] = end_time

        response = requests.get(
            f"{self.base_url}/hotels/{hotel_id}/energy_summary/",
            params=params
        )
        response.raise_for_status()
        return response.content  # Returns CSV content 