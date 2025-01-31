from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Hotel, Room, Sensor, NewestData, RawData
from .serializers import HotelSerializer, RoomSerializer, SensorSerializer, NewestDataSerializer, RawDataSerializer
from django.db import connection, connections
from django.conf import settings
import psycopg2, csv
from datetime import datetime, timedelta
from django.http import HttpResponse

@api_view(['GET'])
def get_all_hotels(request):
    hotels = Hotel.objects.all()
    serializer = HotelSerializer(hotels, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_floors_from_hotel(request, hotel_id):
    """Get all floors from a specific hotel"""
    try:
        floors = Room.objects.filter(hotel=hotel_id).values('floor_id').distinct()
        return Response(floors, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_rooms_from_floor(request, floor_id):
    """Get all rooms from a specific floor"""
    try:
        rooms = Room.objects.filter(floor_id=floor_id)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_room_data(request, room_id):
    """Get all sensor data for a specific room"""
    try:
        sensors = Sensor.objects.filter(room=room_id)
        device_ids = sensors.values_list('device_id', flat=True)
        all_sensor_data = []
        for device_id in device_ids:
            sensor_data = NewestData.objects.filter(device_id=device_id)
            all_sensor_data.extend(sensor_data)
        
        serializer = NewestDataSerializer(all_sensor_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_life_being(request, room_id):
    """Get life being sensor data for a specific room"""
    try:
        sensors = Sensor.objects.filter(room=room_id).filter(device_type='lifebeing_sensor')
        device_ids = sensors.values_list('device_id', flat=True)
        all_sensor_data = []
        for device_id in device_ids:
            sensor_data = NewestData.objects.filter(device_id=device_id)
            all_sensor_data.extend(sensor_data)
        
        serializer = NewestDataSerializer(all_sensor_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_iaq(request, room_id):
    """Get IAQ sensor data for a specific room"""
    try:
        sensors = Sensor.objects.filter(room=room_id).filter(device_type='iaq_sensor')
        device_ids = sensors.values_list('device_id', flat=True)
        all_sensor_data = []
        for device_id in device_ids:
            sensor_data = NewestData.objects.filter(device_id=device_id)
            all_sensor_data.extend(sensor_data)
        
        serializer = NewestDataSerializer(all_sensor_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
SUBSYSTEM_METERS = {
    'ac': ['power_meter_1', 'power_meter_2', 'power_meter_3'],
    'lighting': ['power_meter_4', 'power_meter_5'],
    'plug_load': ['power_meter_6']
}

VALID_RESOLUTIONS = {
    'hourly': '1 hour',
    'daily': '1 day',
    'monthly': '1 month'
}

@api_view(['GET'])
def get_energy_summary(request, hotel_id):
    try:
        end_time = datetime.now()
        start_time = end_time - timedelta(days=30)

        query = """
            WITH bucketed_data AS (
                SELECT 
                    %s as resolution,
                    time_bucket(%s, date_time) AS timestamp,
                    CASE 
                        WHEN device_id IN ('power_meter_1', 'power_meter_2', 'power_meter_3') THEN 'ac'
                        WHEN device_id IN ('power_meter_4', 'power_meter_5') THEN 'lighting'
                        WHEN device_id = 'power_meter_6' THEN 'plug_load'
                    END as subsystem,
                    SUM(CAST(value AS FLOAT)) as total_kw,
                    COUNT(*) as reading_count
                FROM raw_data
                WHERE date_time BETWEEN %s AND %s
                    AND device_id IN (
                        'power_meter_1', 'power_meter_2', 'power_meter_3',
                        'power_meter_4', 'power_meter_5', 'power_meter_6'
                    )
                GROUP BY timestamp, subsystem
            )
            SELECT 
                resolution,
                timestamp,
                MAX(CASE WHEN subsystem = 'ac' THEN total_kw END) as ac_kwh,
                MAX(CASE WHEN subsystem = 'lighting' THEN total_kw END) as lighting_kwh,
                MAX(CASE WHEN subsystem = 'plug_load' THEN total_kw END) as plug_load_kwh
            FROM bucketed_data
            GROUP BY resolution, timestamp
            ORDER BY resolution, timestamp;
        """

        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        filename = f"energy_consumption_{hotel_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        writer = csv.writer(response)
        writer.writerow(['Resolution', 'Timestamp', 'AC (kWh)', 'Lighting (kWh)', 'Plug Load (kWh)'])

        # Execute query for each resolution
        with connection.cursor() as cursor:
            for resolution_name, resolution_value in VALID_RESOLUTIONS.items():
                cursor.execute(
                    query, 
                    [
                        resolution_name,
                        resolution_value,
                        start_time,
                        end_time
                    ]
                )
                
                for row in cursor.fetchall():
                    # Convert kW to kWh based on resolution
                    hours = 1
                    if resolution_name == 'daily':
                        hours = 24
                    elif resolution_name == 'monthly':
                        hours = 720  # 30 days * 24 hours
                    
                    # Calculate kWh for each subsystem
                    ac_kwh = row[2] * hours if row[2] else 0
                    lighting_kwh = row[3] * hours if row[3] else 0
                    plug_load_kwh = row[4] * hours if row[4] else 0
                    
                    writer.writerow([
                        row[0],  # Resolution
                        row[1],  # Timestamp
                        round(ac_kwh, 2),
                        round(lighting_kwh, 2),
                        round(plug_load_kwh, 2)
                    ])

        return response

    except Exception as e:
        return Response(
            {
                "error": str(e),
                "detail": "Error generating energy consumption report"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_energy_consumption(request, hotel_id):
    """Simple test to verify TimescaleDB connection and list tables"""
    try:
        # Use the timescaledb connection
        with connections['timescaledb'].cursor() as cursor:
            queryAC = """
                SELECT time_bucket(%s, date_time) AS bucket,
                    avg(CAST(value AS FLOAT)) AS avg_value
                FROM raw_data
                WHERE device_id IN ('power_kw_power_meter_1', 'power_kw_power_meter_2', 'power_kw_power_meter_3')
                GROUP BY bucket
                ORDER BY bucket ASC;
            """
            queryLighting = """
                SELECT time_bucket(%s, date_time) AS bucket,
                    avg(CAST(value AS FLOAT)) AS avg_value
                FROM raw_data
                WHERE device_id IN ('power_kw_power_meter_4', 'power_kw_power_meter_5')
                GROUP BY bucket
                ORDER BY bucket ASC;
            """
            queryPlugLoad = """
                SELECT time_bucket(%s, date_time) AS bucket,
                    avg(CAST(value AS FLOAT)) AS avg_value
                FROM raw_data
                WHERE device_id = 'power_kw_power_meter_6'
                GROUP BY bucket
                ORDER BY bucket ASC;
            """

            resolutions = ['1 hour', '1 day', '1 month']
            response = HttpResponse(content_type='text/csv')

            for resolution in resolutions:
                filename = f"energy_consumption_{hotel_id}.csv"
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                cursor.execute(queryAC,[resolution])
                ACdata = cursor.fetchall()
                cursor.execute(queryLighting,[resolution])
                Lightingdata = cursor.fetchall()
                cursor.execute(queryPlugLoad,[resolution])
                PlugLoaddata = cursor.fetchall()

                writer = csv.writer(response)
                writer.writerow(['resolution', 'timestamp', 'ac', 'lighting', 'plug_load'])

                for i in range(len(ACdata)):
                    writer.writerows([[resolution, ACdata[i][0], ACdata[i][1], Lightingdata[i][1], PlugLoaddata[i][1]]])
                
            return response


    except Exception as e:
        return Response({
            "error": str(e),
            "detail": "Error connecting to TimescaleDB",
            "type": type(e).__name__
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)