//Motors pin
#define M1_1 13
#define M1_2 12
#define M2_1 A4
#define M2_2 A3
#define M1EN 10
#define M2EN 9
int spd = 255;

#define VSensor A0
#define CSensor A1
float volt,current;

#define Red 5
#define Blue 6
#define Green 7

#define I/O1 8
#define I/O2 A5
#define I/O3 A2
#define ESC 11

char command;

void setup()
{
  Serial.begin(9600);  //Set the baud rate to your Bluetooth module.
  for(int i=5;i<14;i++)
  {pinMode(i,OUTPUT);}
  
  pinMode(A2,OUTPUT);
  pinMode(A3,OUTPUT);
  pinMode(A4,OUTPUT);
  pinMode(A5,OUTPUT);
  
  pinMode(VSensor,INPUT);
  pinMode(CSensor,INPUT);
  
}

void loop() {
  volt = (analogRead(VSensor)/1023.)*12;
  current = (analogRead(CSensor)/1023.)*5;
  //Serial.println("");
  
  if (Serial.available() > 0) {
    command = Serial.read();
    switch (command) {
      case 'F':
        forward();
        break;
      case 'B':
        back();
        break;
      case 'L':
        left();
        break;
      case 'R':
        right();
        break;
      case 'D':
        setspeed('L');
        break;
      case 'M':
        setspeed('M');
        break;
      case 'H':
        setspeed('H');
        break;
      default:
        Stop();
        break;
    }
  }
  
  //RGB LED
  if (spd <= 85)
  {
    digitalWrite(Green,HIGH);
    digitalWrite(Blue,LOW);
    digitalWrite(Red,LOW);
  }
  else if(spd <= 170)
  {
    digitalWrite(Green,LOW);
    digitalWrite(Blue,HIGH);
    digitalWrite(Red,LOW);
  }
  else if(spd <= 255)
  {
    digitalWrite(Green,LOW);
    digitalWrite(Blue,LOW);
    digitalWrite(Red,HIGH);
  }
}


////////////////////////////////////////////////////////////////////////////////////////// Movements Functions //////////////////////////////////////////////////////////////////////////////////////////
void forward()
{
  digitalWrite(M1_1,HIGH);
  digitalWrite(M1_2,LOW);
  digitalWrite(M2_1,HIGH);
  digitalWrite(M2_2,LOW);
  delay(1000);
}

void back()
{
  digitalWrite(M1_1,LOW);
  digitalWrite(M1_2,HIGH);
  digitalWrite(M2_1,LOW);
  digitalWrite(M2_2,HIGH);
}

void left()
{
  digitalWrite(M1_1,HIGH);
  digitalWrite(M1_2,LOW);
  digitalWrite(M2_1,LOW);
  digitalWrite(M2_2,HIGH);
}

void right()
{
  digitalWrite(M1_1,LOW);
  digitalWrite(M1_2,HIGH);
  digitalWrite(M2_1,HIGH);
  digitalWrite(M2_2,LOW);
}

void Stop()
{
  digitalWrite(M1_1,LOW);
  digitalWrite(M1_2,LOW);
  digitalWrite(M2_1,LOW);
  digitalWrite(M2_2,LOW);
}

void setspeed(char s)
{
  switch(s){
    case 'L':
      spd = 85;
      break;
    case 'M':
      spd = 170;
      break;
    case 'H':
      spd = 255;
      break;
  }
  analogWrite(M1EN,spd);
  analogWrite(M2EN,spd);
}
