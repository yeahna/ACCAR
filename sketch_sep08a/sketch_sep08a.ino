#include <SPI.h>  
#include <Servo.h>

char buf [100];  
volatile byte pos = 0;  
volatile boolean printIt = false;  
#define   spi_enable()   (SPCR |= _BV(SPE))  
  
#define L293N_ENA 3

const int SERVO=6;
Servo myservo;
int speed;
int curve=90;

void setup (void)  
{  
  //시리얼 통신 초기화  
  Serial.begin (9600);  
   
  //Master Input Slave Output 12번핀을 출력으로 설정  
  pinMode(MISO, OUTPUT);  
  pinMode(A1, OUTPUT);
  pinMode(A2, OUTPUT);
  pinMode(L293N_ENA, OUTPUT);
  
  //slave 모드로 SPI 시작   
  spi_enable();  
   
  //인터럽트 시작  
  SPI.setClockDivider(SPI_CLOCK_DIV64); //250kHz   
  SPI.setDataMode(SPI_MODE0);  
  SPI.attachInterrupt();  
  
   speed = 130;
   myservo.attach(SERVO);   
}   
   
   
// SPI 인터럽트 루틴  
ISR (SPI_STC_vect)  
{  
  // SPI 데이터 레지스터로부터 한바이트 가져옴  
  byte c = SPDR;    
    
  //버퍼에 자리가 있다면...  
  if (pos < sizeof buf)  
  {  
    buf[pos++] = c;  
      
    // 출력을 진행한다.   
     if (c == '\0')  
      printIt = true;        
   }   
}    
   
  
void loop (void)  
{  
  digitalWrite(A1, LOW);         
  digitalWrite(A2, HIGH); 
  analogWrite(L293N_ENA, 160);
  
  /*
  if (printIt)  
    {  
        buf[pos] = 0;    
        //Serial.println (buf);  
        if(strcmp(buf, "a") == 0){
          curve = 90;
          myservo.write(curve);
          analogWrite(3, speed);      
        }
        else if(strcmp(buf, "b") == 0){
          if(curve > 80 && curve < 100){
            curve -= 2;
            myservo.write(curve);
            analogWrite(L293N_ENA, speed+50);
          }
        }
        else if(strcmp(buf, "c") == 0){
          if(curve > 80 && curve < 100){
            curve += 2;
            myservo.write(curve);
            analogWrite(L293N_ENA, speed+50);
          }
        }
        Serial.println(curve);
        pos = 0;  
        printIt = false;  
    }    
      */
}  

