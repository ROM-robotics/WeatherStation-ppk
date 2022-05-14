
// These constants won't change. They're used to give names to the pins used:
const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to


int sensorValue = 0;        // value read from the pot
float constant = 0.0;

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  pinMode(analogInPin,INPUT);
  //analogReadResolution(12);
  constant = (5.0 /1023.0);
}

void loop() {
  // read the analog in value:
  sensorValue = analogRead(analogInPin);
  float volt = sensorValue * constant;
//  float voltage = sensorValue / 1023.0 * 5.0;
//  float wind_speed = volt/2.5 * 45.0;
  //float wind_speed = 
  
  // map it to the range of the analog out:
  //float wind_speed = map(voltage, 0.0, 5.0, 0.0, 32.0);
  //float ws = map(volt, 0, 5, 0, 32);

  //Serial.print("sensor = ");
  //Serial.print(volt)Serial.print(" == ");
  Serial.println(volt);
  //Serial.println(ws);
  //Serial.print("\t output = ");
  //Serial.print(voltage); Serial.print(" == ");
  //Serial.println(volt);

  // wait 2 milliseconds before the next loop for the analog-to-digital
  // converter to settle after the last reading:
  delay(500);
}
