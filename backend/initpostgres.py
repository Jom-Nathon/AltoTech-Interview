from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session

# Database URL
DATABASE_URL = "postgresql://postgres:jommy348@postgres:5432/postgres"

# Models
class Hotel(SQLModel, table=True):
    __tablename__ = "hotel"
    hotel_id: str = Field(primary_key=True)
    hotel_name: str

class Room(SQLModel, table=True):
    __tablename__ = "room"

    room_id: str = Field(primary_key=True)
    floor_id: str = Field(index=True)
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
        # Add a hotel
        hotel = Hotel(hotel_id="1", hotel_name="Grand AltoTech Hotel")
        session.add(hotel)
        
        # Add some rooms
        room1 = Room(room_id="101", floor_id="1", hotel_id="1")
        room2 = Room(room_id="102", floor_id="1", hotel_id="1")
        room3 = Room(room_id="201", floor_id="2", hotel_id="1")
        room4 = Room(room_id="202", floor_id="2", hotel_id="1")
        room5 = Room(room_id="301", floor_id="3", hotel_id="1")
        room6 = Room(room_id="302", floor_id="3", hotel_id="1")
        room7 = Room(room_id="401", floor_id="4", hotel_id="1")
        room8 = Room(room_id="402", floor_id="4", hotel_id="1")
        room9 = Room(room_id="501", floor_id="5", hotel_id="1")
        room10 = Room(room_id="502", floor_id="5", hotel_id="1")
        room11 = Room(room_id="601", floor_id="6", hotel_id="1")
        room12 = Room(room_id="602", floor_id="6", hotel_id="1")
        room13 = Room(room_id="701", floor_id="7", hotel_id="1")
        room14 = Room(room_id="702", floor_id="7", hotel_id="1")
        room15 = Room(room_id="801", floor_id="8", hotel_id="1")
        room16 = Room(room_id="802", floor_id="8", hotel_id="1")
        room17 = Room(room_id="901", floor_id="9", hotel_id="1")
        room18 = Room(room_id="902", floor_id="9", hotel_id="1")
        room19 = Room(room_id="1001", floor_id="10", hotel_id="1")
        room20 = Room(room_id="1002", floor_id="10", hotel_id="1")
        room21 = Room(room_id="power_room", floor_id="5", hotel_id="1")

        session.add(room1)  
        session.add(room2)
        session.add(room3)
        session.add(room4)
        session.add(room5)
        session.add(room6)
        session.add(room7)
        session.add(room8)
        session.add(room9)
        session.add(room10)
        session.add(room11)
        session.add(room12)
        session.add(room13)
        session.add(room14)
        session.add(room15)
        session.add(room16)
        session.add(room17)
        session.add(room18)
        session.add(room19)
        session.add(room20)
        session.add(room21)

        # Add some sensors
        sensor1 = Sensor(device_id="1", room_id="101", device_type="iaq_sensor")
        sensor2 = Sensor(device_id="2", room_id="102", device_type="iaq_sensor")
        sensor3 = Sensor(device_id="3", room_id="201", device_type="iaq_sensor")
        sensor4 = Sensor(device_id="4", room_id="202", device_type="iaq_sensor")
        sensor5 = Sensor(device_id="5", room_id="301", device_type="iaq_sensor")
        sensor6 = Sensor(device_id="6", room_id="302", device_type="iaq_sensor")
        sensor7 = Sensor(device_id="7", room_id="401", device_type="iaq_sensor")
        sensor8 = Sensor(device_id="8", room_id="402", device_type="iaq_sensor")
        sensor9 = Sensor(device_id="9", room_id="501", device_type="iaq_sensor")
        sensor10 = Sensor(device_id="10", room_id="502", device_type="iaq_sensor")
        sensor11 = Sensor(device_id="11", room_id="601", device_type="iaq_sensor")
        sensor12 = Sensor(device_id="12", room_id="602", device_type="iaq_sensor")
        sensor13 = Sensor(device_id="13", room_id="701", device_type="iaq_sensor")
        sensor14 = Sensor(device_id="14", room_id="702", device_type="iaq_sensor")
        sensor15 = Sensor(device_id="15", room_id="801", device_type="iaq_sensor")
        sensor16 = Sensor(device_id="16", room_id="802", device_type="iaq_sensor")
        sensor17 = Sensor(device_id="17", room_id="901", device_type="iaq_sensor")
        sensor18 = Sensor(device_id="18", room_id="902", device_type="iaq_sensor")
        sensor19 = Sensor(device_id="19", room_id="1001", device_type="iaq_sensor")
        sensor20 = Sensor(device_id="20", room_id="1002", device_type="iaq_sensor")
        sensor21 = Sensor(device_id="21", room_id="101", device_type="lifebeing_sensor")
        sensor22 = Sensor(device_id="22", room_id="102", device_type="lifebeing_sensor")
        sensor23 = Sensor(device_id="23", room_id="201", device_type="lifebeing_sensor")
        sensor24 = Sensor(device_id="24", room_id="202", device_type="lifebeing_sensor")
        sensor25 = Sensor(device_id="25", room_id="301", device_type="lifebeing_sensor")
        sensor26 = Sensor(device_id="26", room_id="302", device_type="lifebeing_sensor")
        sensor27 = Sensor(device_id="27", room_id="401", device_type="lifebeing_sensor")
        sensor28 = Sensor(device_id="28", room_id="402", device_type="lifebeing_sensor")
        sensor29 = Sensor(device_id="29", room_id="501", device_type="lifebeing_sensor")
        sensor30 = Sensor(device_id="30", room_id="502", device_type="lifebeing_sensor")
        sensor31 = Sensor(device_id="31", room_id="601", device_type="lifebeing_sensor")
        sensor32 = Sensor(device_id="32", room_id="602", device_type="lifebeing_sensor")
        sensor33 = Sensor(device_id="33", room_id="701", device_type="lifebeing_sensor")
        sensor34 = Sensor(device_id="34", room_id="702", device_type="lifebeing_sensor")
        sensor35 = Sensor(device_id="35", room_id="801", device_type="lifebeing_sensor")
        sensor36 = Sensor(device_id="36", room_id="802", device_type="lifebeing_sensor")
        sensor37 = Sensor(device_id="37", room_id="901", device_type="lifebeing_sensor")
        sensor38 = Sensor(device_id="38", room_id="902", device_type="lifebeing_sensor")
        sensor39 = Sensor(device_id="39", room_id="1001", device_type="lifebeing_sensor")
        sensor40 = Sensor(device_id="40", room_id="1002", device_type="lifebeing_sensor")
        sensor41 = Sensor(device_id="power_kw_power_meter_1", room_id="power_room", device_type="power_meter")
        sensor42 = Sensor(device_id="power_kw_power_meter_2", room_id="power_room", device_type="power_meter")
        sensor43 = Sensor(device_id="power_kw_power_meter_3", room_id="power_room", device_type="power_meter")
        sensor44 = Sensor(device_id="power_kw_power_meter_4", room_id="power_room", device_type="power_meter")
        sensor45 = Sensor(device_id="power_kw_power_meter_5", room_id="power_room", device_type="power_meter")
        sensor46 = Sensor(device_id="power_kw_power_meter_6", room_id="power_room", device_type="power_meter")

        session.add(sensor1)
        session.add(sensor2)
        session.add(sensor3)
        session.add(sensor4)
        session.add(sensor5)
        session.add(sensor6)
        session.add(sensor7)
        session.add(sensor8)
        session.add(sensor9)
        session.add(sensor10)
        session.add(sensor11)
        session.add(sensor12)
        session.add(sensor13)
        session.add(sensor14)
        session.add(sensor15)
        session.add(sensor16)
        session.add(sensor17)
        session.add(sensor18)
        session.add(sensor19)
        session.add(sensor20)
        session.add(sensor21)
        session.add(sensor22)
        session.add(sensor23)
        session.add(sensor24)
        session.add(sensor25)
        session.add(sensor26)
        session.add(sensor27)
        session.add(sensor28)
        session.add(sensor29)
        session.add(sensor30)
        session.add(sensor31)
        session.add(sensor32)
        session.add(sensor33)
        session.add(sensor34)
        session.add(sensor35)
        session.add(sensor36)
        session.add(sensor37)
        session.add(sensor38)
        session.add(sensor39)
        session.add(sensor40)
        session.add(sensor41)
        session.add(sensor42)
        session.add(sensor43)
        session.add(sensor44)
        session.add(sensor45)
        session.add(sensor46)
        session.commit()

if __name__ == "__main__":
    create_db_and_tables()
    add_initial_data()