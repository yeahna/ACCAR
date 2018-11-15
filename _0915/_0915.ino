#include <SPI.h> // SPI

#include <Servo.h> // 서보모터

#include <NewPing.h> //초음파 센서

 

 

//FOR SPI

char buf[100];

volatile byte pos = 0;

volatile boolean printIt = false;

#define spi_enable() (SPCR |= _BV(SPE))

 

//FOR DC MOTOR

// #define L293N_ENA 6

#define L293N_ENA 3

// int IN1Pin = 7;         // 헤드라이트

// int IN2Pin = 8;         // 정체불명

 

int IN1Pin = 15;

int IN2Pin = 16;

 

int speed;

 

//FOR SERVO MOTOR

// const int SERVO=3;

const int SERVO=6;

Servo myservo;

int curve,center;

 

//초음파 센서

/* trigger and echo pins for each sensor*/

#define SONAR1        2

#define SONAR2        4

#define SONAR3        5

#define MAX_DISTANCE  1000  // maximum distance for sensors

#define NUM_SONAR     3     // number of sonar sensors

 

// array of sonar sensor objects

NewPing sonar[NUM_SONAR] = { 

  NewPing(SONAR1, SONAR1, MAX_DISTANCE),

  NewPing(SONAR2, SONAR2, MAX_DISTANCE),

  NewPing(SONAR3, SONAR3, MAX_DISTANCE)

 

};

 

// array stores distances for each(cm)

int distance[NUM_SONAR]; 

int dir;

 

void setup(void)

{

  //시리얼 통신 초기화

  Serial.begin(9600);

  //Master Input Slave Output 12번핀을 출력으로 설정

  pinMode(MISO, OUTPUT);

 

  //slave 모드로 SPI 시작

  spi_enable();

 

  //인터럽트 시작

  SPI.setClockDivider(SPI_CLOCK_DIV64); //250kHz   

  SPI.setDataMode(SPI_MODE0);  

  SPI.attachInterrupt();  

  

  // DC MOTOR SETTING

  pinMode(IN1Pin, OUTPUT);

  pinMode(IN2Pin, OUTPUT);

  pinMode(L293N_ENA, OUTPUT);

  speed = 55;

  

  // SERVO MOTOR SETTING

  myservo.attach(SERVO);   

  curve = 77;   

  center = 77;  

  myservo.write(curve); // 서보모터 각도 90도 SETTING

}

 

//초음파센서 값 얻어오는 함수

void updateSonar() {

 

  for (int i = 0; i < NUM_SONAR; i++) {

 

    // update distance

    distance[i] = sonar[i].ping_cm(); 

    

    Serial.println(sonar[i].ping_cm());

 

  }

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

    //printIt = true;

    // 출력을 진행한다.   

    if (c == '\0')  

      printIt = true;     

         

   }  

 

   //Serial.println(buf);

   

   

}    

 

void car_start(){

 // Serial.println("GO");

  digitalWrite(IN1Pin, LOW);         

  digitalWrite(IN2Pin, HIGH); 

  analogWrite(L293N_ENA, speed);

}

 

void car_stop(){

  //Serial.println("STOP");

  digitalWrite(IN1Pin, LOW);         

  digitalWrite(IN2Pin, LOW);

}

 

void loop(void)

{

 

  // 테스트 코드

  //updateSonar();

  //초음파 센서 하나만 임시 테스트(거리가 가까워졌을 때 주행 멈춤)

  //if(distance[0] < 10)

  //  car_stop();

   

  //SPI 통신으로 문자열 수신

  

  if (printIt)  

   {

   

     // if(distance[0] < 10)

     //   car_stop();

        //else

       //   car_start();  

        buf[pos] = 0;    

        Serial.println (buf);  

        pos = 0;  

        printIt = false;  

        //car_start();

 

        //SPI통신으로 젯슨에게 a,b,c 문자열 수신하여 방향 파악 가능

        if(strcmp(buf, "straight") == 0){ // Straight

          car_start();

          curve=77;

          myservo.write(curve);

          analogWrite(L293N_ENA, speed);

        }

        else if(strcmp(buf, "left") == 0){ // LEFT

          car_start();

          if(curve <= 106 && curve >= 44){ //각도제한은 트랙에 따라 수정

            //if(curve < 108 && curve > 44){

              //curve-=1; 

              if(curve > center)

                curve = center;

 

              curve -= 1;

            //}

            myservo.write(curve);

            //analogWrite(L293N_ENA, 220); // 회전 주행 시 pwm 출력이 더 필요하여 +50

          }

        }

        else if(strcmp(buf, "right") == 0){ // RIGHT

          car_start();

          if(curve <= 106 && curve >= 44){

            if(curve == 106){

              curve=105;

            }

 

            

            if(curve < center)

              curve=center;

            curve +=1;

            myservo.write(curve);

            //analogWrite(L293N_ENA, 220);

          }

        }

        else if(!(strcmp(buf, "car") && strcmp(buf, "person") && strcmp(buf, "stop_sign") && strcmp(buf, "traffic_light"))){

          car_stop();

        }

        

        //Serial.println(curve);

        

    }

   

    

   

}
