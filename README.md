# AltoTech Fullstack Software Developer Test

![image14](https://github.com/user-attachments/assets/61065858-d641-4d94-b83f-1debdd7cc4b8)



![messageImage_1739252572076](https://github.com/user-attachments/assets/f3a19a54-d991-4b24-ae57-000e103bede4)


This repo is made for AltoTech interview test project.
A comprehensive IoT-based hotel management system that provides real-time monitoring of room conditions, energy consumption tracking, and an AI-powered chat interface for guest interactions.

## Features

- **Real-time Room Monitoring**
  - Temperature, humidity, and CO2 levels (IAQ Sensor)
  - Room occupancy detection (Life Being Sensor)
  - Energy consumption tracking

- **Data Management**
  - Time-series data storage with TimescaleDB
  - Message queuing with RabbitMQ
  - RESTful API endpoints

- **AI Chat Interface**
  - Natural language interaction using Claude Sonnet 3.5
  - Real-time sensor data queries
  - Energy consumption reports
  - Guest assistance

## Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Anthropic API key for Claude AI

## Quick Start

1. Clone the repository
```bash
git clone https://github.com/Jom-Nathon/AltoTech-Interview
```

2. Set up environment variables

Create a python env file in the root directory:
```
python -m venv env
pip install requirements.txt
```

3. Set up Anthropic API key and config.py file
Sign up for Anthropic account at
`https://console.anthropic.com/`
and then generate keys at
`https://console.anthropic.com/settings/keys`

4. Create Anthropic key file inside backend/api/config.py file, example below

```
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    ANTROPIC_API_KEY: str = 'your-anthropic-api-key'

    class Config:
        case_sensitive = True

settings = Settings() 

```

5. Start the services
```bash
docker compose up --build
```

6. Access the services
- Chat Interface: `http://localhost:5173/`
- Backend API: `http://localhost:8000/`
- RabbitMQ Management: `http://localhost:15672` (guest/guest)
- PGAdmin `http://localhost:8080/`
- PGAdmin username and password can be change inside docker compose file. Example: 
  
```
  postgres:
    image: postgres:17.1
    hostname: postgres
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: "change this to your prefer username"
      POSTGRES_PASSWORD: "change this to your prefer password"
```


## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/hotels/` | GET | List all hotels |
| `/api/hotels/<hotel_id>/floors/` | GET | Get all floors from specific hotel |
| `/api/floors/<floor_id>/rooms/` | GET | Get all rooms from specific floor |
| `/api/rooms/<room_id>/data/` | GET | Get room sensor data |
| `/api/rooms/<room_id>/data/life_being` | GET | Get room life being sensor data |
| `/api/rooms/<room_id>/data/iaq` | GET | Get room iaq sensor data |
| `/api/hotels/<hotel_id>/energy_summary/` | GET | Get csv energy consumption reports |
| `/chat/` | POST | Post reponse from chat bot api |

## System Architecture

The project uses Docker Compose for development. Each component runs in its own container:

| Service | Description |
|---------|-------------|
| `pgadmin` | Django REST API |
| `postgres` | Django REST API |
| `rabbitmq` | Message queue |
| `timescaledb` | Time-series database |
| `supabase` | realtime database |
| `datalogger_supabase` | Data collection service for supabase |
| `datalogger_timescale` | Data collection service for timescale |
| `initpostgres` | Simple python script for initilizing postgres relational table |
| `frontend` | Data collection service for timescale |
| `backend` | Django REST API |
| `powermeter_agent` | Data collection service for supabase |
| `lifebeing_agent` | Lifebeing sensor simulation |
| `iaq_agent` | IAQ sensor simulation |

## Directory Structure

```
smart_hotel/
├── backend/            # Django REST API
    ├── api/            # Backend endpoint and configs
        ├── chat/              # Anthropic chat bot agent
├── frontend/           # React Frontend chat ui
├── iot/                # Simulated iot sensor data with rabbitmq broker
└── docker-compose.yml  # Docker configuration
```

