/***
 * Arduino Sketch Example for Railroader Train Control Panel
 * 
 * This sketch reads analog and digital inputs and sends formatted data
 * to the Python controller via serial communication.
 * 
 * Hardware connections:
 * - Analog inputs: A0-A6 for potentiometers (WHISTLE, HEADLIGHT, REVERSER, THROTTLE, BRAKE, IND_BRAKE, etc.)
 * - Digital inputs: D2-D4 for buttons/switches (BELL, CYLINDER)
 * 
 * Serial format sent to Python:
 * WHISTLE:512;BELL:1;HEADLIGHT:300;CYLINDER:0;REVERSER:800;THROTTLE:200;TRAINBRAKE:100;INDBRAKE:50
 */

// Pin definitions
const int WHISTLE_PIN = A0;
const int HEADLIGHT_PIN = A1;
const int REVERSER_PIN = A2;
const int THROTTLE_PIN = A3;
const int TRAINBRAKE_PIN = A4;
const int INDBRAKE_PIN = A5;
const int CYLINDER_PIN = 2;  // Digital input for toggle switch
const int BELL_PIN = 3;      // Digital input for button

// Serial communication
const int BAUD_RATE = 9600;
const int UPDATE_INTERVAL = 50;  // milliseconds

void setup() {
  // Initialize serial communication
  Serial.begin(BAUD_RATE);
  
  // Set pin modes
  pinMode(CYLINDER_PIN, INPUT);
  pinMode(BELL_PIN, INPUT);
  
  // Wait for serial monitor to open (optional)
  delay(1000);
  Serial.println("Railroader Controller Ready");
}

void loop() {
  // Read all analog inputs (0-1023)
  int whistle = analogRead(WHISTLE_PIN);
  int headlight = analogRead(HEADLIGHT_PIN);
  int reverser = analogRead(REVERSER_PIN);
  int throttle = analogRead(THROTTLE_PIN);
  int trainBrake = analogRead(TRAINBRAKE_PIN);
  int indBrake = analogRead(INDBRAKE_PIN);
  
  // Read digital inputs (0 or 1)
  int cylinder = digitalRead(CYLINDER_PIN);
  int bell = digitalRead(BELL_PIN);
  
  // Build and send formatted string
  Serial.print("WHISTLE:");
  Serial.print(whistle);
  Serial.print(";BELL:");
  Serial.print(bell);
  Serial.print(";HEADLIGHT:");
  Serial.print(headlight);
  Serial.print(";CYLINDER:");
  Serial.print(cylinder);
  Serial.print(";REVERSER:");
  Serial.print(reverser);
  Serial.print(";THROTTLE:");
  Serial.print(throttle);
  Serial.print(";TRAINBRAKE:");
  Serial.print(trainBrake);
  Serial.print(";INDBRAKE:");
  Serial.println(indBrake);
  
  // Wait before next transmission
  delay(UPDATE_INTERVAL);
}
