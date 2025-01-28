# Smart Hotel System

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
  - Natural language interaction using Claude AI
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
cd smart-hotel
```

2. Set up environment variables

Create a `.env` file in the root directory:
```ini
ANTHROPIC_API_KEY=your_api_key_here
```

3. Start the services
```bash
docker-compose up --build
```

4. Access the services
- Chat Interface: `http://localhost:7860`
- Backend API: `http://localhost:8000/api`
- RabbitMQ Management: `http://localhost:15672` (guest/guest)

## System Architecture

### IoT Agents (`agents/`)
- **IAQ Sensor**: Environmental monitoring
- **Life Being Sensor**: Occupancy detection
- **Datalogger**: Data collection and storage

### Backend (`backend/`)
- Django REST API
- Room management
- Energy consumption tracking
- Sensor data endpoints

### Chat Interface (`chat/`)
- Gradio web interface
- Claude AI integration
- Natural language processing

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/hotels/` | GET | List all hotels |
| `/api/rooms/<room_id>/data/` | GET | Get room sensor data |
| `/api/hotels/<hotel_id>/energy_summary/` | GET | Get energy consumption reports |

## Development

The project uses Docker Compose for development. Each component runs in its own container:

| Service | Description |
|---------|-------------|
| `backend` | Django REST API |
| `timescaledb` | Time-series database |
| `rabbitmq` | Message queue |
| `chat` | AI chat interface |
| `iaq_sensor` | IAQ sensor simulation |
| `life_being_sensor` | Occupancy sensor simulation |
| `datalogger` | Data collection service |

## Directory Structure

```
smart_hotel/
├── agents/              # IoT sensor simulation agents
├── backend/             # Django REST API
├── chat/               # AI chat interface
├── docs/               # Documentation
└── docker-compose.yml  # Docker configuration
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
