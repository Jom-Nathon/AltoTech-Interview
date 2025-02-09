from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session

# Database URL
DATABASE_URL = "postgresql://postgres:jommy348@postgres:5432/postgres"

# Models
class Hotel(SQLModel, table=True):
    __tablename__ = "hotel"
    hotel_id: str = Field(primary_key=True)
    hotel_name: str

class Floor(SQLModel, table=True):
    __tablename__ = "floor"
    floor_id: str = Field(primary_key=True)
    hotel_id: str = Field(default=None, foreign_key="hotel.hotel_id")

class Room(SQLModel, table=True):
    __tablename__ = "room"

    room_id: str = Field(primary_key=True)
    floor_id: str = Field(default=None, foreign_key="floor.floor_id")
    hotel_id: Optional[str] = Field(default=None, foreign_key="hotel.hotel_id")

class Sensor(SQLModel, table=True):
    __tablename__ = "sensor"
    
    device_id: str = Field(primary_key=True)
    room_id: Optional[str] = Field(default=None, foreign_key="room.room_id")
    device_type: str

# Create tables
def create_db_and_tables():
    engine = create_engine(DATABASE_URL, echo=True)
    SQLModel.metadata.create_all(engine)

# Optional: Add some initial data
def add_initial_data():
    engine = create_engine(DATABASE_URL, echo=True)
    
    with Session(engine) as session:
        try:
            # First, add the hotel and commit immediately
            hotel = Hotel(hotel_id="1", hotel_name="Grand AltoTech Hotel")
            session.add(hotel)
            session.commit()  # Commit hotel first

            # Then add floors
            floors = [
                Floor(floor_id=str(i), hotel_id="1") 
                for i in range(1, 11)
            ]
            session.add_all(floors)
            session.commit()  # Commit floors

            # Then add rooms
            rooms = [
                Room(room_id="101", floor_id="1", hotel_id="1"),
                Room(room_id="102", floor_id="1", hotel_id="1"),
                Room(room_id="201", floor_id="2", hotel_id="1"),
                Room(room_id="202", floor_id="2", hotel_id="1"),
                Room(room_id="301", floor_id="3", hotel_id="1"),
                Room(room_id="302", floor_id="3", hotel_id="1"),
                Room(room_id="401", floor_id="4", hotel_id="1"),
                Room(room_id="402", floor_id="4", hotel_id="1"),
                Room(room_id="501", floor_id="5", hotel_id="1"),
                Room(room_id="502", floor_id="5", hotel_id="1"),
                Room(room_id="601", floor_id="6", hotel_id="1"),
                Room(room_id="602", floor_id="6", hotel_id="1"),
                Room(room_id="701", floor_id="7", hotel_id="1"),
                Room(room_id="702", floor_id="7", hotel_id="1"),
                Room(room_id="801", floor_id="8", hotel_id="1"),
                Room(room_id="802", floor_id="8", hotel_id="1"),
                Room(room_id="901", floor_id="9", hotel_id="1"),
                Room(room_id="902", floor_id="9", hotel_id="1"),
                Room(room_id="1001", floor_id="10", hotel_id="1"),
                Room(room_id="1002", floor_id="10", hotel_id="1"),
                Room(room_id="power_room", floor_id="5", hotel_id="1")
            ]
            session.add_all(rooms)
            session.commit()  # Commit rooms

            # Finally add sensors
            sensors = [
                Sensor(device_id="1", room_id="101", device_type="iaq_sensor"),
                Sensor(device_id="2", room_id="102", device_type="iaq_sensor"),
                Sensor(device_id="3", room_id="201", device_type="iaq_sensor"),
                Sensor(device_id="4", room_id="202", device_type="iaq_sensor"),
                Sensor(device_id="5", room_id="301", device_type="iaq_sensor"),
                Sensor(device_id="6", room_id="302", device_type="iaq_sensor"),
                Sensor(device_id="7", room_id="401", device_type="iaq_sensor"),
                Sensor(device_id="8", room_id="402", device_type="iaq_sensor"),
                Sensor(device_id="9", room_id="501", device_type="iaq_sensor"),
                Sensor(device_id="10", room_id="502", device_type="iaq_sensor"),
                Sensor(device_id="11", room_id="601", device_type="iaq_sensor"),
                Sensor(device_id="12", room_id="602", device_type="iaq_sensor"),
                Sensor(device_id="13", room_id="701", device_type="iaq_sensor"),
                Sensor(device_id="14", room_id="702", device_type="iaq_sensor"),
                Sensor(device_id="15", room_id="801", device_type="iaq_sensor"),
                Sensor(device_id="16", room_id="802", device_type="iaq_sensor"),
                Sensor(device_id="17", room_id="901", device_type="iaq_sensor"),
                Sensor(device_id="18", room_id="902", device_type="iaq_sensor"),
                Sensor(device_id="19", room_id="1001", device_type="iaq_sensor"),
                Sensor(device_id="20", room_id="1002", device_type="iaq_sensor"),
                Sensor(device_id="21", room_id="101", device_type="lifebeing_sensor"),
                Sensor(device_id="22", room_id="102", device_type="lifebeing_sensor"),
                Sensor(device_id="23", room_id="201", device_type="lifebeing_sensor"),
                Sensor(device_id="24", room_id="202", device_type="lifebeing_sensor"),
                Sensor(device_id="25", room_id="301", device_type="lifebeing_sensor"),
                Sensor(device_id="26", room_id="302", device_type="lifebeing_sensor"),
                Sensor(device_id="27", room_id="401", device_type="lifebeing_sensor"),
                Sensor(device_id="28", room_id="402", device_type="lifebeing_sensor"),
                Sensor(device_id="29", room_id="501", device_type="lifebeing_sensor"),
                Sensor(device_id="30", room_id="502", device_type="lifebeing_sensor"),
                Sensor(device_id="31", room_id="601", device_type="lifebeing_sensor"),
                Sensor(device_id="32", room_id="602", device_type="lifebeing_sensor"),
                Sensor(device_id="33", room_id="701", device_type="lifebeing_sensor"),
                Sensor(device_id="34", room_id="702", device_type="lifebeing_sensor"),
                Sensor(device_id="35", room_id="801", device_type="lifebeing_sensor"),
                Sensor(device_id="36", room_id="802", device_type="lifebeing_sensor"),
                Sensor(device_id="37", room_id="901", device_type="lifebeing_sensor"),
                Sensor(device_id="38", room_id="902", device_type="lifebeing_sensor"),
                Sensor(device_id="39", room_id="1001", device_type="lifebeing_sensor"),
                Sensor(device_id="40", room_id="1002", device_type="lifebeing_sensor"),
                Sensor(device_id="power_kw_power_meter_1", room_id="power_room", device_type="power_meter"),
                Sensor(device_id="power_kw_power_meter_2", room_id="power_room", device_type="power_meter"),
                Sensor(device_id="power_kw_power_meter_3", room_id="power_room", device_type="power_meter"),
                Sensor(device_id="power_kw_power_meter_4", room_id="power_room", device_type="power_meter"),
                Sensor(device_id="power_kw_power_meter_5", room_id="power_room", device_type="power_meter"),
                Sensor(device_id="power_kw_power_meter_6", room_id="power_room", device_type="power_meter")
            ]
            session.add_all(sensors)
            session.commit()  # Commit sensors

        except Exception as e:
            print(f"Error adding initial data: {e}")
            session.rollback()
            raise

if __name__ == "__main__":
    create_db_and_tables()
    add_initial_data()