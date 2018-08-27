#include <SPI.h>
#include <Servo.h>


char buf[100];
volatile byte idx;
volatile boolean process;

#define L293N_ENA 3

const int SERVO=6;
int angle=0;
Servo myservo;
int speed;
int curve;
void setup(void)
{
  Serial.begin(9600);
   pinMode(A1, OUTPUT);
  pinMode(A2, OUTPUT);
  pinMode(L293N_ENA, OUTPUT); 
  pinMode(MISO, OUTPUT);
  
  SPCR |= _BV(SPE);
  
  idx = 0;
  process = false;
  /* sensor */
  myservo.attach(SERVO);        

  // 임시적으로 GO
  speed = 200;
  SPI.attachInterrupt();
}

ISR(SPI_STC_vect)
{
  byte c = SPDR;
  
  if(idx < sizeof buf)
  {
    buf[idx++] = c;
    
    if(c == '\0')
      process = true;
      
  }
  
}
void car_start(){
 // Serial.println("GO");
  digitalWrite(A1, LOW);         
  digitalWrite(A2, HIGH); 
  analogWrite(L293N_ENA, speed);
}

void loop(void)
{
  if(process)
  {
 //   buf[idx] = 0;
    process = false;
    Serial.println(buf);
    idx = 0;
    car_start();
    curve = atoi(buf);
    Serial.print("curve  ");
    Serial.println(curve);
    myservo.write(curve);
  }
}
