export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface EnvironmentalSensors {
  temperature: number;
  co2: number;
  humidity: number;
}

export interface OccupancySensors {
  sensitivity: number;
  online: boolean;
  occupied: boolean;
}

export interface RoomData {
  id: string;
  environmental: EnvironmentalSensors;
  occupancy: OccupancySensors;
  last_updated: string;
}

export interface EnergyData {
  value: number;
  unit: string;
  timestamp: Date;
}