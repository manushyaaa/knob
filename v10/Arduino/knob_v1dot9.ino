/*
 10/10/2023 - V1.9 with OLED Screen
 - added Enchanced Rot 
 - added actions
 - added time 
*/

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

String version = "v1.9";

#define CLK 5        // CLK pin of the rotary encoder
#define DATA 6       // DT pin of the rotary encoder
#define encoderSW 7  // SW pin of the rotary encoder#include <Arduino.h>

#define SCREEN_WIDTH 128  // OLED display width, in pixels
#define SCREEN_HEIGHT 32  // OLED display height, in pixels

const int buttonPin = 2;      // Main button    
const int leftbuttonPin = 3;  // Left button 
const int rightbuttonPin = 4; // Right button  

int prev_c = 0;
static uint8_t prevNextCode = 0;
static uint16_t store = 0;
boolean rotating = false;

int buttonState = HIGH;       
int lastButtonState = HIGH;   

int leftbuttonState = HIGH;      
int leftlastButtonState = HIGH;  

int rightbuttonState = HIGH;      
int rightlastButtonState = HIGH;   

int counter = 0;                   // Counter to keep track of the modes
unsigned long previousMillis = 0;  
const long interval = 1000;        // Interval in milliseconds (1 second)

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

const unsigned char bongocat[] PROGMEM = {
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x01, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x10, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x1c, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xe0,
  0x07, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x70, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x0c, 0x00, 0x00, 0x0f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0c, 0x18, 0x00, 0x00, 0x00,
  0xc0, 0x00, 0x00, 0x00, 0x00, 0x31, 0xe0, 0x00, 0x00, 0x00, 0x30, 0x78, 0x00, 0x00, 0x00, 0x60,
  0xc0, 0x00, 0x00, 0x00, 0x0f, 0x88, 0x00, 0x00, 0x00, 0x40, 0x40, 0x00, 0x00, 0x00, 0x00, 0x08,
  0x00, 0x00, 0x00, 0x40, 0x00, 0x60, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x40, 0x00, 0x60,
  0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0xc0, 0x40, 0x00, 0x04, 0x80, 0x00, 0x00, 0x10, 0x00, 0x00,
  0x3e, 0x40, 0x00, 0x03, 0xc0, 0x03, 0xe0, 0x10, 0x00, 0x00, 0x00, 0xf8, 0x00, 0x00, 0x00, 0x06,
  0x18, 0x20, 0x00, 0x00, 0x00, 0x07, 0xc0, 0x00, 0x00, 0x74, 0x08, 0x20, 0x00, 0x00, 0x00, 0x00,
  0x1f, 0x00, 0x00, 0x04, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf8, 0x00, 0x0c, 0x00, 0x18,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0xc0, 0x04, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x1f, 0x04, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xfe, 0x00, 0x04, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0xe0, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x0f, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xfa, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x1f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x60, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
};

void setup() {

  pinMode(CLK, INPUT);
  pinMode(CLK, INPUT_PULLUP);
  pinMode(DATA, INPUT);
  pinMode(DATA, INPUT_PULLUP);

  pinMode(buttonPin, INPUT_PULLUP);   
  pinMode(leftbuttonPin, INPUT_PULLUP);
  pinMode(rightbuttonPin, INPUT_PULLUP);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;)
      ;
  }

  delay(300);

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 25);

  display.println("Knob " + version);
  display.drawBitmap(63, 0, bongocat, 75, 32, WHITE);
  display.display();

  Serial.begin(115200);

}

void loop() {

  unsigned long currentMillis = millis();
  static int8_t c, val;

  buttonState = digitalRead(buttonPin);
  leftbuttonState = digitalRead(leftbuttonPin);
  rightbuttonState = digitalRead(rightbuttonPin);

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
  if (rightbuttonState == LOW && rightlastButtonState == HIGH) {
 
    switch (counter) {

      case 1:
        Serial.println("MediaChangeR");
        break;

      case 2:
        Serial.println("ShutdownR");
        break;

      case 3:
        Serial.println("Next");
        break;

      case 4:
        Serial.println("ChangeModeR");
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
          break;
      }      
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
          break;
      }
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
          break;
      }
      rotating = true;
    }
  } 
  else {
    rotating = false;
  }

  if (buttonState == LOW && lastButtonState == HIGH) {
    counter++;

    if (counter > 4) {
      counter = 1;
    }

    switch (counter) {
      case 1:  // Action for Volume Control 
        display.fillRect(0, 0,65, 32, BLACK);
 
        display.setCursor(0, 10);
        display.println("SYS VOL");

        display.setCursor(0, 23);
        display.println("Media");

        display.setCursor(35, 23);
        display.println("Media");

        display.display();
        delay(300);  // Debounce delay
        break;

      case 2:  // Action for Brightness Control  
       display.fillRect(0, 0,65, 32, BLACK);
        display.setCursor(0, 10);

        display.println("SCREEN");

        display.setCursor(0, 23);
        display.println("Shut");

        display.setCursor(35, 23);
        display.println("TskM");

        display.display();
        delay(300);  // Debounce delay
        break;

      case 3:  // Action for Spotify Control 
        display.fillRect(0, 0,65, 32, BLACK);
        display.setCursor(0, 10);

        display.println("SPOTIFY");

        display.setCursor(0, 23);
        display.println("Next");

        display.setCursor(35, 23);
        display.println("Prev");

        display.display();
        delay(300);  // Debounce delay
        break;

      case 4:  // Action for Video Seek Control
        display.fillRect(0, 0,65, 32, BLACK);
        display.setCursor(0, 10);

        display.println("WLED");

        display.setCursor(0, 23);
        display.println("Mode");

        display.setCursor(35, 23);
        display.println("Color");

        display.display();
        delay(300);;  // Debounce delay
        break;
     
      default:
        break;
    }
  }

  // Update the last button state
  lastButtonState = buttonState;
  leftlastButtonState = leftbuttonState;
  rightlastButtonState = rightbuttonState;

  //for getting time
  if (counter != 0){
   if (currentMillis - previousMillis >= interval) {
      previousMillis = currentMillis;
      Serial.println("GetTime");
      if (Serial.available() > 0) {
        String data = Serial.readStringUntil('\n');
        display.fillRect(63, 0, 75, 32 , BLACK);
        
        display.setCursor(80, 10);
        display.println(data);
        display.display();
      }   
    }
  }
}

// Read the rotary encoder --> with precision.
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
