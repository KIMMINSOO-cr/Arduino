#define TRIG 13
#define ECHO 12

void setup()
{
  Serial.begin(9600);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
}

void loop()
{
  long duration,distance;
  
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2); //delay(2)
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10); 
  digitalWrite(TRIG, LOW);
  
  duration = pulseIn(ECHO, HIGH);
  distance = duration/58.2;
  
  Serial.println(duration);
  Serial.print("\nDIstance : ");
  Serial.print(distance);
  Serial.println(" Cm");
  
  if (distance >=100){
    digitalWrite(7, HIGH);
    digitalWrite(8, LOW);
  }else {
    digitalWrite(7, LOW);
    digitalWrite(8, HIGH);
  }
  
  
  delay(1000);
  
}