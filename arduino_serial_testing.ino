
#include <Arduino.h>

#define encoderCLK 2  // CLK pin of the rotary encoder
#define encoderDT 4   // DT pin of the rotary encoder
#define encoderSW 3   // SW pin of the rotary encoder

int encoderPos = 0;
int lastEncoderPos = 0;
boolean rotating = false;

void setup() {

  pinMode(encoderCLK, INPUT);
  pinMode(encoderDT, INPUT);
  pinMode(encoderSW, INPUT_PULLUP);


  Serial.begin(9600);
  
}

void loop() {
  
  int CLKstate = digitalRead(encoderCLK);
  if (CLKstate != lastEncoderPos) {
    if (digitalRead(encoderDT) != CLKstate) {
      encoderPos++;
      Serial.println("VolumeUp");

    } else {
      encoderPos--;
      Serial.println("VolumeDown");
    }
    
    Serial.println(encoderPos);
  }
  lastEncoderPos = CLKstate;

  if (digitalRead(encoderSW) == LOW) {
    if (!rotating) {
      Serial.println("PlayPause");
      rotating = true;
    }
  } else {
    rotating = false;
  }
}
