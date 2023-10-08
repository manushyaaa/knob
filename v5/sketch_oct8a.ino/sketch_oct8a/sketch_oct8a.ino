#include <Arduino.h>

#define CLK 2        // CLK pin of the rotary encoder
#define DATA 4       // DT pin of the rotary encoder
#define encoderSW 3  // SW pin of the rotary encoder#include <Arduino.h>

const int buttonPin = 7;  // The digital pin where the button is connected
const int leftbuttonPin = 8;  // The digital pin where the button is connected


const int redPin = 9;     // Use a different PWM pin
const int greenPin = 6;   // Use a different PWM pin
const int bluePin = 5;    // Use a different PWM pin

int prev_c = 0;
static uint8_t prevNextCode = 0;
static uint16_t store = 0;
boolean rotating = false;

int buttonState = HIGH;      // The initial state of the button (assume not pressed)
int lastButtonState = HIGH;  // The previous state of the button
int leftbuttonState = HIGH;      // The initial state of the button (assume not pressed)
int leftlastButtonState = HIGH;  // The previous state of the button

int counter = 0;             // Counter to keep track of the value

void setup() {
  
  pinMode(CLK, INPUT);
  pinMode(CLK, INPUT_PULLUP);
  pinMode(DATA, INPUT);
  pinMode(DATA, INPUT_PULLUP);

  pinMode(buttonPin, INPUT_PULLUP);  // Enable internal pull-up resistor
  pinMode(leftbuttonPin, INPUT_PULLUP); 

  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);

  Serial.begin(115200);
  // Serial.println("KY-040 Start:");
}
void primaryColors(int redValue, int greenValue, int blueValue) {
  digitalWrite(redPin, redValue);
  digitalWrite(greenPin, greenValue);
  digitalWrite(bluePin, blueValue);
}
void loop() {
 
  static int8_t c, val;
  buttonState = digitalRead(buttonPin);
  leftbuttonState = digitalRead(leftbuttonPin);
 

  if (leftbuttonState == LOW && leftlastButtonState == HIGH) {
    
    switch (counter) {
      case 1:  
        Serial.println("MediaChange");       
        break;
      case 2:   
        Serial.println("Shutdown"); 
        break;
      case 3:   
        Serial.println("Previous");
        break;
      case 4:   
        Serial.println("ChangeMode"); 
        break;
      default:
        break;
    }
  }

  if (val = read_rotary()) {
    prev_c = c;
    c += val;

    if (prev_c < c) {
      switch (counter) {
        case 1:
          Serial.println("VolumeUp");
          break;
        case 2:
          Serial.println("BrightnessUp");
          break;
        case 3:
          Serial.println("MusicSeekUp");
          break;
        case 4:
          Serial.println("LightUp");
          break;
        default:
          // Handle other cases here
          break;
      }

      // Serial.println("forward");
    }
    if (prev_c > c) {

      switch (counter) {
        case 1:
          Serial.println("VolumeDown");
          break;
        case 2:
          Serial.println("BrightnessDown");
          break;
        case 3:
          Serial.println("MusicSeekDown");
          break;
       case 4:
          Serial.println("LightDown");
          break;
        default:
          // Handle other cases here
          break;
      }
      // Serial.println("backward");
    }
  }

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
        case 4:
          Serial.println("Power");
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

    if (counter > 4) {
      counter = 1;
    }

    switch (counter) {
      case 1:  // Action for Volume Control ?? BLUE
        Serial.println("Counter 1 action");
        primaryColors(1, 0, 0);
        break;
      case 2:  // Action for Brightness Control ?? MAG
        Serial.println("Counter 2 action");
        primaryColors(0, 1, 0);
        break;
      case 3:  // Action for Video Seek Control ?? YELLOW
        Serial.println("Counter 3 action");
        primaryColors(0, 0, 1);
        break;
      case 4:  // Action for Video Seek Control ?? YELLOW
        Serial.println("Counter 4 action");
        primaryColors(0, 1, 1);
        break;
      default:
        break;
    }
  }
  // Update the last button state
  lastButtonState = buttonState;
  leftlastButtonState = leftbuttonState;
}

// A vald CW or  CCW move returns 1, invalid returns 0.
int8_t read_rotary() {
  static int8_t rot_enc_table[] = { 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0 };

  prevNextCode <<= 2;
  if (digitalRead(DATA)) prevNextCode |= 0x02;
  if (digitalRead(CLK)) prevNextCode |= 0x01;
  prevNextCode &= 0x0f;

  if (rot_enc_table[prevNextCode]) {
    store <<= 4;
    store |= prevNextCode;

    if ((store & 0xff) == 0x2b) return -1;
    if ((store & 0xff) == 0x17) return 1;
  }
  return 0;
}
