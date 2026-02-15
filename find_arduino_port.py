"""
Simple utility to find Arduino COM ports
Run this before setting up the main controller to identify your Arduino's port
"""

import serial.tools.list_ports
import sys

def list_available_ports():
    """List all available COM ports with descriptions"""
    ports = serial.tools.list_ports.comports()
    
    if not ports:
        print("No COM ports found!")
        print("Please check:")
        print("  1. Arduino is plugged in via USB")
        print("  2. Arduino drivers are installed")
        print("  3. USB cable is working properly")
        return
    
    print("=" * 70)
    print("AVAILABLE COM PORTS")
    print("=" * 70)
    print()
    
    for i, port in enumerate(ports, 1):
        print(f"{i}. {port.device:6} - {port.description}")
        if port.manufacturer:
            print(f"   Manufacturer: {port.manufacturer}")
        print()
    
    print("=" * 70)
    print("NEXT STEPS:")
    print("  1. Find your Arduino in the list above")
    print("  2. Note the COM port number (e.g., COM3)")
    print("  3. Update SERIAL_PORT in railroader_controller.py")
    print()
    print("     SERIAL_PORT = \"COM3\"  # Change COM3 to your port")
    print()
    print("=" * 70)


def test_connection(port, baud=9600):
    """Test if a serial connection works"""
    try:
        ser = serial.Serial(port, baud, timeout=2)
        print(f"\n✓ Successfully connected to {port}")
        
        # Try to read some data
        print(f"Waiting for data from {port}...")
        for i in range(5):
            if ser.in_waiting:
                data = ser.readline().decode('utf-8', errors='ignore').strip()
                print(f"Received: {data}")
            else:
                print(f"  [{i+1}/5] Waiting...", end='\r')
                import time
                time.sleep(1)
        
        ser.close()
        print("\n✓ Connection test complete")
        
    except Exception as e:
        print(f"\n✗ Failed to connect to {port}: {e}")
        print("  Try a different port or check your Arduino connection")


if __name__ == "__main__":
    print()
    list_available_ports()
    
    # Offer to test a connection
    response = input("\nTest a connection to a specific port? (y/n): ").strip().lower()
    if response == 'y':
        port = input("Enter port name (e.g., COM3): ").strip().upper()
        if not port.startswith('COM'):
            port = f"COM{port}"
        test_connection(port)
