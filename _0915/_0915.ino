#include <SPI.h> // SPI

#include <Servo.h> 

//#include <NewPing.h>



//FOR SPI

char buf[100];

volatile byte pos = 0;

volatile boolean printIt = false;

#define spi_enable() (SPCR |= _BV(SPE))



//FOR DC MOTOR

// #define L293N_ENA 6

#define L293N_ENA 3

// int IN1Pin = 7;        

// int IN2Pin = 8;        



int IN1Pin = 15;

int IN2Pin = 16;



int speed;



//FOR SERVO MOTOR

// const int SERVO=3;

const int SERVO=6;

Servo myservo;

int curve;




/* trigger and echo pins for each sensor*/

#define SONAR1        2

#define SONAR2        4

#define SONAR3        5

#define MAX_DISTANCE  1000  // maximum distance for sensors

#define NUM_SONAR     3     // number of sonar sensors



// array of sonar sensor objects

/*NewPing sonar[NUM_SONAR] = { 

  NewPing(SONAR1, SONAR1, MAX_DISTANCE),

  NewPing(SONAR2, SONAR2, MAX_DISTANCE),

  NewPing(SONAR3, SONAR3, MAX_DISTANCE)



};*/



// array stores distances for each(cm)

int distance[NUM_SONAR]; 

int dir;



void setup(void)

{


  Serial.begin(9600);

  //Master Input Slave Output 12

  pinMode(MISO, OUTPUT);




  spi_enable();




  SPI.setClockDivider(SPI_CLOCK_DIV64); //250kHz   

  SPI.setDataMode(SPI_MODE0);  

  SPI.attachInterrupt();  

  

  // DC MOTOR SETTING

  pinMode(IN1Pin, OUTPUT);

  pinMode(IN2Pin, OUTPUT);

  pinMode(L293N_ENA, OUTPUT);

  speed = 200;

  

  // SERVO MOTOR SETTING

  myservo.attach(SERVO);   

  curve = 90;     

  myservo.write(curve); // Œ­ºžžðÅÍ °¢µµ 90µµ SETTING

}




/*void updateSonar() {



  for (int i = 0; i < NUM_SONAR; i++) {



    // update distance

    distance[i] = sonar[i].ping_cm(); 

    

  //  Serial.println(sonar[i].ping_cm());



  }

}*/




ISR (SPI_STC_vect)  

{  


  byte c = SPDR;    

    
 

  if (pos < sizeof buf)  

  {  

    buf[pos++] = c;  

      


     if (c == '\0')  

      printIt = true;        

   }   

}    



void car_start(){

 // Serial.println("GO");

  digitalWrite(IN1Pin, LOW);         

  digitalWrite(IN2Pin, HIGH); 

  analogWrite(L293N_ENA, speed);

}



void car_stop(){

  Serial.println("STOP");

  digitalWrite(IN1Pin, LOW);         

  digitalWrite(IN2Pin, LOW);

}

unsigned char a=1;

void loop(void)

{


  //if(distance[0] < 10)

    //car_stop();

    

  if (printIt)  

    {  

        buf[pos] = 0;    

        Serial.println (buf);  

        pos = 0;  

        printIt = false;  

        if(a)
        {
          car_start();
        }
        else
        {
          car_stop();
        }
        a^=1;



        if(strcmp(buf, "a") == 0){ // Straight

          curve=90;

          myservo.write(curve);

        }

        else if(strcmp(buf, "b") == 0){ // LEFT

          if(curve < 110 && curve > 70){ //°¢µµÁŠÇÑÀº Æ®·¢¿¡ µû¶ó ŒöÁ€

            curve-=2;

            myservo.write(curve);

            analogWrite(L293N_ENA, speed); 
          }

        }

        else if(strcmp(buf, "c") == 0){ // RIGHT

          if(curve < 110 && curve > 70){

            curve+=2;

            myservo.write(curve);

            analogWrite(L293N_ENA, speed);

          }

        }

    }    

}
