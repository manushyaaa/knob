#include <Arduino.h>

#define encoderCLK 11  // CLK pin of the rotary encoder
#define encoderDT 9   // DT pin of the rotary encoder
#define encoderSW 8   // SW pin of the rotary encoder

const int buttonPin = 5;  // The digital pin where the button is connected
const int redPin = 9;     // Use a different PWM pin
const int greenPin = 6;   // Use a different PWM pin
const int bluePin = 5;    // Use a different PWM pin

int buttonState = HIGH;      // The initial state of the button (assume not pressed)
int lastButtonState = HIGH;  // The previous state of the button
int counter = 0;             // Counter to keep track of the value

int CLKstate = 0;
int encoderPos = 0;
int lastEncoderPos = 0;
boolean rotating = false;



void setup() {
  Serial.begin(9600);

  pinMode(buttonPin, INPUT_PULLUP);  // Enable internal pull-up resistor

  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);

  pinMode(encoderCLK, INPUT);
  pinMode(encoderDT, INPUT);
  pinMode(encoderSW, INPUT_PULLUP);
}

void primaryColors(int redValue, int greenValue, int blueValue) {
  digitalWrite(redPin, redValue);
  digitalWrite(greenPin, greenValue);
  digitalWrite(bluePin, blueValue);
}

void loop() {

  CLKstate = digitalRead(encoderCLK);
  buttonState = digitalRead(buttonPin);
  if (CLKstate != lastEncoderPos) {
    if (digitalRead(encoderDT) != CLKstate) {
      encoderPos++;
      switch (counter) {
        case 1:
          Serial.println("VolumeUp");
          break;
        case 2:
          Serial.println("BrightnessUp");
          break;
        case 3:
          Serial.println("SEEKUp");
          break;
        default:
          // Handle other cases here
          break;
      }


    } else {
      encoderPos--;
      switch (counter) {
        case 1:
          Serial.println("VolumeDown");
          break;
        case 2:
          Serial.println("BrightnessDown");
          break;
        case 3:
          Serial.println("SEEKDown");
          break;
        default:
          // Handle other cases here
          break;
      }
    }
  }
  lastEncoderPos = CLKstate;

  if (digitalRead(encoderSW) == LOW) {
    if (!rotating) {
      switch (counter) {
        case 1:
          Serial.println("Mute");
          break;
        case 2:
          Serial.println("Lock");
          break;
        case 3:
          Serial.println("PlayPause");
          break;
        default:
          // Handle other cases here
          break;
      }
       
      rotating = true;
    }
  } else {
    rotating = false;
  }

  if (buttonState == LOW && lastButtonState == HIGH) {
    counter++;

    if (counter > 3) {
      counter = 1;
    }

    switch (counter) {
      case 1:  // Action for Volume Control ?? BLUE
        Serial.println("Counter 1 action");
        primaryColors(1, 0, 0);
        break;
      case 2: // Action for Brightness Control ?? MAG
        Serial.println("Counter 2 action");
        primaryColors(0, 1, 0);
        break;
      case 3:// Action for Video Seek Control ?? YELLOW
        Serial.println("Counter 3 action");
        primaryColors(0, 0, 1);
        break;
      default:
        break;
    }
  }

  // Update the last button state
  lastButtonState = buttonState;
}
