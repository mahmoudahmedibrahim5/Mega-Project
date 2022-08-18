//Motors pin
int M1_1 = 10;  //PB2
int M1_2 = 11;  //PB3
int M2_1 = 12;  //PB4
int M2_2 = 13;  //PB5

char command;

void setup()
{
  Serial.begin(9600);  //Set the baud rate to your Bluetooth module.
  for(int i=10;i<14;i++)
  {pinMode(i,OUTPUT);}
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.read();

    //Stop(); //initialize with motors stoped
    
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
      default:
        Stop();
        break;
    }
  }
}

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
