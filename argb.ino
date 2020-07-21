#include <Adafruit_NeoPixel.h>

#define PIXEL_PIN    6    // Digital IO pin connected to the NeoPixels.
#define PIXEL_COUNT 18

#define BUTTON_PIN 4

// Parameter 1 = number of pixels in strip,  neopixel stick has 8
// Parameter 2 = pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_RGB     Pixels are wired for RGB bitstream
//   NEO_GRB     Pixels are wired for GRB bitstream, correct for neopixel stick
//   NEO_KHZ400  400 KHz bitstream (e.g. FLORA pixels)
//   NEO_KHZ800  800 KHz bitstream (e.g. High Density LED strip), correct for neopixel stick
Adafruit_NeoPixel strip = Adafruit_NeoPixel(PIXEL_COUNT, PIXEL_PIN, NEO_GRB + NEO_KHZ800);

uint16_t rainbowCycle_j, rainbowCycle_j2;
uint16_t theaterChase_i;
uint16_t theaterChaseRainbow_j;

String inputString;       // a String to hold incoming data
bool stringComplete;  // whether the string is complete
bool status_led;

void setup() {
  inputString = 130;
  stringComplete = true;
  status_led = true;
  
  Serial.begin(9600);
  
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
}

void loop() {  
  if (digitalRead(BUTTON_PIN) == HIGH) {
    if (inputString[0] == '0') {
      inputString[0] = '1';
    } else if (inputString[0] == '1') {
      inputString[0] = '0';
    }
    
    while (digitalRead(BUTTON_PIN) == HIGH) { 
      delay(200);
     
    }
  }

  if (stringComplete) {
    if (inputString[0] == '0') {
      colorWipe(0,0,0);
      inputString[0] = '0';
      
    } else if(inputString[0] == '1'){
      if(inputString[1] == '0'){
        colorWipe(inputString.substring(2,5).toInt(), inputString.substring(5,8).toInt(), inputString.substring(8,11).toInt());
        
      } else if(inputString[1] == '1'){
        theaterChase(strip.Color(inputString.substring(2,5).toInt(), inputString.substring(5,8).toInt(), inputString.substring(8,11).toInt()));
        
      } else if(inputString[1] == '2'){
        cpuBasedColor(inputString.substring(2,5).toInt());
        
      } else if(inputString[1] == '3'){
        if(inputString[2] == '0'){
          rainbowCycle();
          
        } else if(inputString[2] == '1'){
          rainbowCycle_2();
          
        } else if(inputString[2] == '2'){
          theaterChaseRainbow();
          
        }
      }
    }
  }
}

void cpuBasedColor(byte load){
  byte r, g, b;

  r = 255;
  g = b = 255 - map(load, 0, 100, 0, 255);

  colorWipe(r, g, b);
}

// Fill the dots one after the other with a color
void colorWipe(int r, int g, int b) {
  for(int i; i < strip.numPixels(); i++){
    strip.setPixelColor(i, r, g, b);
    strip.show();
  }
}

// Slightly different, this makes the rainbow equally distributed throughout
void rainbowCycle() {
  if(rainbowCycle_j < 256) {
    for(int rainbowCycle_i = 0; rainbowCycle_i < strip.numPixels(); rainbowCycle_i++) {
      strip.setPixelColor(rainbowCycle_i, Wheel(((rainbowCycle_i * 256 / strip.numPixels()) + rainbowCycle_j) & 255, rainbowCycle_i));
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
      strip.setPixelColor(rainbowCycle_i, Wheel(rainbowCycle_j2, rainbowCycle_i));
    }
    rainbowCycle_j2++;

    strip.show();
    delay(10);
  } else{
    rainbowCycle_j2 = 0;
  }
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos, int index) {
  WheelPos = 255 - WheelPos;
  byte r, g, b;
  
  if (WheelPos < 85) {
    r = 255 - WheelPos * 3;
    g = 0;
    b =  WheelPos * 3;
  }else if (WheelPos < 170) {
    WheelPos -= 85;
    
    r = 0;
    g = WheelPos * 3;
    b = 255 - WheelPos * 3;
  }else {
    WheelPos -= 170;
    
    r = WheelPos * 3;
    g = 255 - WheelPos * 3;
    b = 0;
  }
    
  return strip.Color(r, g, b);
}

//Theatre-style crawling lights.
void theaterChase(uint32_t c) {
  if(theaterChase_i < strip.numPixels()){
    strip.setPixelColor(theaterChase_i, strip.Color(0, 0, 0));
    theaterChase_i++;

    if(theaterChase_i == strip.numPixels()){
      theaterChase_i = 0;
    }
    
    strip.setPixelColor(theaterChase_i, c);
    strip.setPixelColor(theaterChase_i + 1, c);
    strip.setPixelColor(theaterChase_i + 2, c);
    strip.show();
    delay(40);
  }    
}

//Theatre-style crawling lights with rainbow effect
void theaterChaseRainbow() {
  if(theaterChaseRainbow_j < 256) {
    theaterChase(Wheel(theaterChaseRainbow_j, -1));
    theaterChaseRainbow_j++;
  } else{
    theaterChaseRainbow_j = 0;
 }
}
  
void serialEvent() {
  if (stringComplete) {
    inputString = "";
    stringComplete = false;
  }
  
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      inputString += inChar;
    }
  }
}
