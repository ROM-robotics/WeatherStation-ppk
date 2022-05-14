

volatile unsigned long Rotations=0; //Cup rotation counter used in interrupt routine

float WindSpeed; //Speed meter per second

unsigned long gulStart_Read_Timer = 0;

void setup(){
  Serial.begin(9600);
  pinMode(2,INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(2),isr_rotation, RISING); //Set up the interrupt

  Serial.println("Rotations\tm/s");
  sei(); //Enables interrupts
  
}

void loop()
{
    Serial.println(Rotations);
    delay(100);
}

// This is the function that the interrupt calls to increment the rotation count
void isr_rotation()
{
    Rotations++;
}
