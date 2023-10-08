#include <Arduino.h>

#define CLK 2        // CLK 
#define DATA 4       // DT  
#define encoderSW 3  // SW  

const int leftbuttonPin = 7;  
const int rightbuttonPin = 8 ; 

const int redPin = 9;     
const int greenPin = 6;   
const int bluePin = 5;    

int prev_c = 0;
static uint8_t prevNextCode = 0;
static uint16_t store = 0;
boolean rotating = false;

int leftbuttonState = HIGH;      // The initial state of the button (assume not pressed)
int leftlastButtonState = HIGH;  // The previous state of the button

int rightbuttonState = HIGH;      // The initial state of the button (assume not pressed)
int rightlastButtonState = HIGH;  // The previous state of the button

int counter = 0;             // Counter to keep track of the value

void setup() {
  pinMode(CLK, INPUT);
  pinMode(CLK, INPUT_PULLUP);
  pinMode(DATA, INPUT);
  pinMode(DATA, INPUT_PULLUP);

  pinMode(leftbuttonPin, INPUT_PULLUP);  
  pinMode(rightbuttonPin, INPUT_PULLUP);

  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);

  Serial.begin(115200);
  // Serial.println("KY-040 Start:");
}