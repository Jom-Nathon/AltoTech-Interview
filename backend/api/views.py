from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Hotel, Room, Sensor, NewestData
from .serializers import HotelSerializer, RoomSerializer, NewestDataSerializer
from django.db import connections
import json, csv
from datetime import datetime
from django.http import HttpResponse
from .chat.chat import smart_hotel_agent, supportDependencies
from .chat.intent_classifier import intent_classifier
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


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
        resolution = request.GET.get('resolution')
        start_time = request.GET.get('start_time', '2024-01-01T00:00:00Z')
        end_time = request.GET.get('end_time', datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'))
        subsystem = request.GET.get('subsystem', 'all')

        VALID_RESOLUTIONS = [
            'hourly',
            'daily',
            'monthly'
        ]

        if resolution not in VALID_RESOLUTIONS:
            return Response(
                {"error": f"Invalid resolution. Must be one of: {', '.join(VALID_RESOLUTIONS)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if resolution == 'hourly':
            resolution = '1 hour'
        elif resolution == 'daily':
            resolution = '1 day'
        elif resolution == 'monthly':
            resolution = '1 month'

        # Validate subsystem
        VALID_SUBSYSTEMS = ['ac', 'lighting', 'plug_load', 'all']
        if subsystem not in VALID_SUBSYSTEMS:
            return Response(
                {"error": f"Invalid subsystem. Must be one of: {', '.join(VALID_SUBSYSTEMS)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Use the timescaledb connection
        with connections['timescaledb'].cursor() as cursor:
            base_query = """
                SELECT 
                    time_bucket(%s, date_time) AS bucket,
                    avg(CAST(value AS FLOAT)) AS avg_value
                FROM raw_data
                WHERE date_time BETWEEN %s AND %s
            """

            # Add subsystem filter
            ac_query = base_query + " AND device_id IN ('power_kw_power_meter_1', 'power_kw_power_meter_2', 'power_kw_power_meter_3')"
            lightning_query = base_query + " AND device_id IN ('power_kw_power_meter_4', 'power_kw_power_meter_5')"
            plug_load_query = base_query + " AND device_id = 'power_kw_power_meter_6'"

            # Add grouping and ordering
            if resolution != 'all':
                ac_query += " GROUP BY bucket ORDER BY bucket ASC"
                lightning_query += " GROUP BY bucket ORDER BY bucket ASC"
                plug_load_query += " GROUP BY bucket ORDER BY bucket ASC"
            else:
                ac_query += " ORDER BY bucket ASC"
                lightning_query += " ORDER BY bucket ASC"
                plug_load_query += " ORDER BY bucket ASC"


            response = HttpResponse(content_type='text/csv')

            filename = f"energy_consumption_{hotel_id}.csv"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

            if subsystem == 'ac':
                cursor.execute(ac_query,[resolution, start_time, end_time])
                ACdata = cursor.fetchall()
                writer = csv.writer(response)
                writer.writerow(['timestamp', 'ac'])

                for i in range(len(ACdata)):
                    writer.writerows([[ACdata[i][0], ACdata[i][1]]])

            elif subsystem == 'lighting':
                cursor.execute(lightning_query,[resolution, start_time, end_time])
                Lightingdata = cursor.fetchall()
                writer = csv.writer(response)
                writer.writerow(['timestamp', 'lighting'])

                for i in range(len(Lightingdata)):
                    writer.writerows([[Lightingdata[i][0], Lightingdata[i][1]]])

            elif subsystem == 'plug_load':
                cursor.execute(plug_load_query,[resolution, start_time, end_time])
                PlugLoaddata = cursor.fetchall()
                writer = csv.writer(response)
                writer.writerow(['timestamp', 'plug_load'])

                for i in range(len(PlugLoaddata)):
                    writer.writerows([[PlugLoaddata[i][0], PlugLoaddata[i][1]]])

            else:
                cursor.execute(ac_query,[resolution, start_time, end_time])
                ACdata = cursor.fetchall()
                cursor.execute(lightning_query,[resolution, start_time, end_time])
                Lightingdata = cursor.fetchall()
                cursor.execute(plug_load_query,[resolution, start_time, end_time])
                PlugLoaddata = cursor.fetchall()
                writer = csv.writer(response)

                writer.writerow(['timestamp', 'ac', 'lighting', 'plug_load'])

                for i in range(len(ACdata)):
                    writer.writerows([[ACdata[i][0], ACdata[i][1], Lightingdata[i][1], PlugLoaddata[i][1]]])

            return response

    except Exception as e:
        return Response({
            "error": str(e),
            "detail": "Error connecting to TimescaleDB",
            "type": type(e).__name__
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@csrf_exempt
@require_http_methods(["POST"])
async def chat_endpoint(request):
    # try:
        data = json.loads(request.body)
        message = data.get('message')
        result = await smart_hotel_agent.run(message)

        return JsonResponse({
            "data": result.data,
            "status": "success"
        })
    # except Exception as e:
    #     return JsonResponse({
    #         "error": str(e),
    #         "status": "error"
    #     }, status=500)