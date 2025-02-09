import React, { useEffect, useState } from 'react';
import { 
  Thermometer,
  Droplets,
  Wind,
  Wifi,
  Activity,
  Users,
  Gauge
} from 'lucide-react';
import { subscribeToRoomData } from '../lib/supabase';
import type { RoomData } from '../types';

// Mock data for preview
const mockRoomData: RoomData = {
  id: '1',
  environmental: {
    temperature: 22.5,
    co2: 800,
    humidity: 45
  },
  occupancy: {
    sensitivity: 75,
    online: true,
    occupied: true
  },
  last_updated: new Date().toISOString()
};

export function RoomVisualization() {
  const [roomData, setRoomData] = useState<RoomData>(mockRoomData);

  // Keep Supabase subscription logic for later use
  useEffect(() => {
    // Simulate data updates for preview
    const interval = setInterval(() => {
      setRoomData(prev => ({
        ...prev,
        environmental: {
          temperature: Math.round((prev.environmental.temperature + (Math.random() * 0.4 - 0.2)) * 10) / 10,
          co2: Math.round(prev.environmental.co2 + (Math.random() * 20 - 10)),
          humidity: Math.round(prev.environmental.humidity + (Math.random() * 2 - 1))
        },
        occupancy: {
          ...prev.occupancy,
          occupied: Math.random() > 0.8 ? !prev.occupancy.occupied : prev.occupancy.occupied
        },
        last_updated: new Date().toISOString()
      }));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-4 max-w-md mx-auto">
      <div className="bg-gray-800 rounded-lg overflow-hidden border border-gray-700">
        {/* Room Image */}
        <img
          src="https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?auto=format&fit=crop&w=1200&q=80"
          alt="Modern hotel room"
          className="w-full h-32 object-cover"
        />
        
        <div className="p-3">
          <h3 className="text-gray-100 font-semibold mb-3 text-lg">Room 101</h3>
          
          <div className="space-y-4">
            {/* Environmental Sensors */}
            <div className="space-y-2">
              <h4 className="text-sm font-medium text-gray-400">Environmental Sensors</h4>
              <div className="space-y-2 text-sm bg-gray-900 rounded-lg p-2">
                <div className="flex items-center justify-between text-gray-300">
                  <div className="flex items-center gap-1.5">
                    <Thermometer size={16} className="text-blue-400" />
                    <span>Temperature</span>
                  </div>
                  <span>{roomData.environmental.temperature}°C</span>
                </div>
                
                <div className="flex items-center justify-between text-gray-300">
                  <div className="flex items-center gap-1.5">
                    <Wind size={16} className="text-blue-400" />
                    <span>CO2</span>
                  </div>
                  <span>{roomData.environmental.co2} ppm</span>
                </div>
                
                <div className="flex items-center justify-between text-gray-300">
                  <div className="flex items-center gap-1.5">
                    <Droplets size={16} className="text-blue-400" />
                    <span>Humidity</span>
                  </div>
                  <span>{roomData.environmental.humidity}%</span>
                </div>
              </div>
            </div>

            {/* Occupancy Sensors */}
            <div className="space-y-2">
              <h4 className="text-sm font-medium text-gray-400">Occupancy Sensors</h4>
              <div className="space-y-2 text-sm bg-gray-900 rounded-lg p-2">
                <div className="flex items-center justify-between text-gray-300">
                  <div className="flex items-center gap-1.5">
                    <Gauge size={16} className="text-purple-400" />
                    <span>Sensitivity</span>
                  </div>
                  <span>{roomData.occupancy.sensitivity}%</span>
                </div>
                
                <div className="flex items-center justify-between text-gray-300">
                  <div className="flex items-center gap-1.5">
                    <Wifi size={16} className="text-purple-400" />
                    <span>Status</span>
                  </div>
                  <span className={roomData.occupancy.online ? 'text-green-400' : 'text-red-400'}>
                    {roomData.occupancy.online ? 'Online' : 'Offline'}
                  </span>
                </div>
                
                <div className="flex items-center justify-between text-gray-300">
                  <div className="flex items-center gap-1.5">
                    <Users size={16} className="text-purple-400" />
                    <span>Occupancy</span>
                  </div>
                  <span className={roomData.occupancy.occupied ? 'text-green-400' : 'text-gray-400'}>
                    {roomData.occupancy.occupied ? 'Occupied' : 'Vacant'}
                  </span>
                </div>
              </div>
            </div>

            <div className="text-xs text-gray-500 mt-2 pt-2 border-t border-gray-700">
              Last updated: {new Date(roomData.last_updated).toLocaleTimeString()}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}