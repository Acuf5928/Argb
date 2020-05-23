#include <Adafruit_NeoPixel.h>

#define PIXEL_PIN    6    // Digital IO pin connected to the NeoPixels.
#define PIXEL_COUNT 18

#define TEMP_MIN 0
#define TEMP_MAX 100

// Parameter 1 = number of pixels in strip,  neopixel stick has 8
// Parameter 2 = pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_RGB     Pixels are wired for RGB bitstream
//   NEO_GRB     Pixels are wired for GRB bitstream, correct for neopixel stick
//   NEO_KHZ400  400 KHz bitstream (e.g. FLORA pixels)
//   NEO_KHZ800  800 KHz bitstream (e.g. High Density LED strip), correct for neopixel stick
Adafruit_NeoPixel strip = Adafruit_NeoPixel(PIXEL_COUNT, PIXEL_PIN, NEO_GRB + NEO_KHZ800);

byte Mod;

uint16_t rainbowCycle_j, rainbowCycle_j2;
int theaterChase_i, theaterChase_i2;
int colorWipe_i;
int theaterChaseRainbow_j;

int cpu_temp;
int cpu_temp_fun_num = 1300;
int min_temp_act, max_temp_act;

String inputString = "";       // a String to hold incoming data
bool stringComplete = false;  // whether the string is complete

#define BUTTON_PIN 4
boolean status_led = false;

void setup() {
  Mod = 10;
  min_temp_act = cpu_temp_fun_num + TEMP_MIN;
  max_temp_act = cpu_temp_fun_num + TEMP_MAX;
  
  //Serial
  Serial.begin(115200);
  inputString.reserve(200);
  
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
}

void loop()
{  
  if (digitalRead(BUTTON_PIN) == HIGH) {
      status_led =! status_led;

    while (digitalRead(BUTTON_PIN) == HIGH) { 
      delay(200);  
    }
  }
  
  if (stringComplete) {
    int temp = inputString.toInt();
   
      if(temp != 0){
        if(temp >= cpu_temp_fun_num and temp < min_temp_act){
          Mod = 8;
        } else if(temp >= min_temp_act and temp <= max_temp_act){
          cpu_temp = temp - 1300;
          Mod = 13;
        } else if(temp > max_temp_act){
          Mod = 6;
        } else if (temp == 4) {
          status_led = false;
        } else{
          status_led = true;
          Mod = temp;  
          rainbowCycle_j = 0;
          rainbowCycle_j2 = 0;
          theaterChase_i = 0;
          colorWipe_i = 0;
          theaterChaseRainbow_j = 0;
        }
      }
    
    // clear the string:
    inputString = "";
    stringComplete = false;
  }
  startShow();
}

void startShow() {
  if (status_led == false) {
       colorWipe(strip.Color(0, 0, 0)); 
  } else {
    switch (Mod) {
      case 1: colorWipe(strip.Color(255, 0, 0));  // Red
        break;
      case 2: colorWipe(strip.Color(0, 255, 0));  // Green
        break;
      case 3: colorWipe(strip.Color(0, 0, 255));  // Blue
        break;
      case 5: colorWipe(strip.Color(255, 255, 255));    // White
        break;
      case 6: theaterChase(strip.Color(255, 0, 0));  // Red
        break;
      case 7: theaterChase(strip.Color(0, 255, 0));  // Green
        break;
      case 8: theaterChase(strip.Color(0, 0, 255));  // Blue
        break;
      case 9: theaterChase(strip.Color(255, 255, 255));    // White
        break;
      case 10: rainbowCycle();
        break;
      case 11: rainbowCycle_2();
        break;
      case 12: theaterChaseRainbow();
        break;
      case 13: cpu_temp_fun();
        break;
    } 
  }
}

void cpu_temp_fun(){
  byte r, g, b;

  r = (cpu_temp - TEMP_MIN) * 255 / (TEMP_MAX - TEMP_MIN);
  b = 255 - r;
  
  colorWipe(strip.Color(r, g, b));
}

// Fill the dots one after the other with a color
void colorWipe(uint32_t c) {
  if(colorWipe_i < strip.numPixels()){
    strip.setPixelColor(colorWipe_i, c);
    colorWipe_i++;
    strip.show();
    delay(50);
  }    
  else{
    colorWipe_i = 0;
  }
}

// Slightly different, this makes the rainbow equally distributed throughout
void rainbowCycle() {
  if(rainbowCycle_j < 256) {
    for(int rainbowCycle_i = 0; rainbowCycle_i < strip.numPixels(); rainbowCycle_i++) {
      strip.setPixelColor(rainbowCycle_i, Wheel(((rainbowCycle_i * 256 / strip.numPixels()) + rainbowCycle_j) & 255));
    }
    rainbowCycle_j++;

    strip.show();
    delay(10);
  }
 else{
  rainbowCycle_j = 0;
 }
}

void rainbowCycle_2() {
  if(rainbowCycle_j2 < 256) {
    for(int rainbowCycle_i = 0; rainbowCycle_i < strip.numPixels(); rainbowCycle_i++) {
      strip.setPixelColor(rainbowCycle_i, Wheel(rainbowCycle_j2));
    }
    rainbowCycle_j2++;

    strip.show();
    delay(10);
  }
 else{
  rainbowCycle_j2 = 0;
 }
}

//Theatre-style crawling lights.
void theaterChase(uint32_t c) {
  if(theaterChase_i < strip.numPixels()){
    strip.setPixelColor(theaterChase_i, strip.Color(0, 0, 0));
    theaterChase_i++;

    if(theaterChase_i == strip.numPixels()){
      theaterChase_i = 0;
    }
    
    if(theaterChase_i2 < strip.numPixels()){
    strip.setPixelColor(theaterChase_i2, strip.Color(0, 0, 0));
    theaterChase_i2++;

    if(theaterChase_i2 == strip.numPixels()){
      theaterChase_i2 = 0;
    }
    
    strip.setPixelColor(theaterChase_i, c);
    strip.show();
    delay(25);
    }
  }    
}

//Theatre-style crawling lights with rainbow effect
void theaterChaseRainbow() {
  if(theaterChaseRainbow_j < 256) {
    theaterChase(Wheel(theaterChaseRainbow_j));
    theaterChaseRainbow_j++;
  }
 else{
  theaterChaseRainbow_j = 0;
 }
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if (WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if (WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}


void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:

    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
