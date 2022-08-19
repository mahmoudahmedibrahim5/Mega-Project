//Motors pin
#define M1_1 PB5
#define M1_2 PB4
#define M2_1 PC4
#define M2_2 PC3
#define M1EN PB2
#define M2EN PB1
int spd = 0;

#define VSensor PC0
#define CSensor PC1
float volt,current;

#define Red PD5
#define Blue PD6
#define Green PD7

#define I/O1 PB0
#define I/O2 PC5
#define I/O3 PC2
#define ESC PB3

char command;

void setup()
{
  Serial.begin(9600);  //Set the baud rate to your Bluetooth module.
  for(int i=5;i<14;i++)
  {pinMode(i,OUTPUT);}
  
  pinMode(PC2,OUTPUT);
  pinMode(PC3,OUTPUT);
  pinMode(PC4,OUTPUT);
  pinMode(PC5,OUTPUT);
  
  pinMode(VSensor,INPUT);
  pinMode(CSensor,INPUT);
  
}

void loop() {
  volt = (analogRead(VSensor)/1023.)*5;
  current = (analogRead(CSensor)/1023.)*5;

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
      case 'S':
        if (Serial.available() > 0) {
          setspeed(Serial.read());
        }
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
  command = '0';
}

void back()
{
  digitalWrite(M1_1,LOW);
  digitalWrite(M1_2,HIGH);
  digitalWrite(M2_1,LOW);
  digitalWrite(M2_2,HIGH);
  delay(1000);
  command = '0';
}

void left()
{
  digitalWrite(M1_1,HIGH);
  digitalWrite(M1_2,LOW);
  digitalWrite(M2_1,LOW);
  digitalWrite(M2_2,HIGH);
  delay(1000);
  command = '0';
}

void right()
{
  digitalWrite(M1_1,LOW);
  digitalWrite(M1_2,HIGH);
  digitalWrite(M2_1,HIGH);
  digitalWrite(M2_2,LOW);
  delay(1000);
  command = '0';
}

void Stop()
{
  digitalWrite(M1_1,LOW);
  digitalWrite(M1_2,LOW);
  digitalWrite(M2_1,LOW);
  digitalWrite(M2_2,LOW);
  delay(1000);
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
