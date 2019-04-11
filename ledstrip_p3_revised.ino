// Made by Hannah van Iterson and Rachel Feldman(2019), 2nd year Bachelor student at the Department of Industrial Design at the TU/e.
// This code was inspired by :
// https://www.instructables.com/id/RGB-LED-Montion-Sensor-Lamp/
// https://gathering.tweakers.net/forum/list_messages/1694393?data%5Bfilter_pins%5D=1
// https://forum.arduino.cc/index.php?topic=98735.0
//
// This code was revised by and created with help of:
// Bas van Rossem, 2nd year HBO ICT Student at the Hogeschool Utrecht, Richting: TI (Technische Informatica)


//-----------------------VARIABLES-----------------------//
#define REDPIN 3
#define GREENPIN 5
#define BLUEPIN 6
#define FADESPEED 25      // make this higher to slow down

byte r, g, b;
String colour;              // which colour is currently being displayed


//-----------------------SETUP-----------------------//
void setup() {
  pinMode(REDPIN, OUTPUT);
  pinMode(GREENPIN, OUTPUT);
  pinMode(BLUEPIN, OUTPUT);

  Serial.begin(9600);

  // fade from off to red
  for (r = 0; r < 255; r++) {
    analogWrite(REDPIN, r);
    colour = 'Red';
    delay(FADESPEED);
  }
}


//-----------------------COLOURLOOPS-----------------------//
void redtoyellow () {
  int r, g, b;
  // fade from red to yellow
  for (g = 0; g < 255; g++) {
    analogWrite(GREENPIN, g);
    colour = 'Yellow';
    delay(FADESPEED);
  }
}
void yellowtogreen () {
  int r, g, b;
  // fade from yellow to green
  for (r = 255; r > 0; r--) {
    analogWrite(REDPIN, r);
    colour = 'Green';
    delay(FADESPEED);
  }
}
void greentoyellow () {
  int r, g, b;
  // fade from green to yellow
  for (r = 0; r < 255; r++) {
    analogWrite(REDPIN, r);
    colour = 'Yellow';
    delay(FADESPEED);
  }
}
void yellowtored () {
  int r, g, b;
  // fade from yellow to red
  for (g = 255; g > 0; g--) {
    analogWrite(GREENPIN, g);
    colour = 'Red';
    delay(FADESPEED);
  }
}


//-----------------------ACTUAL PROGRAM-----------------------//
void loop() {
  if (Serial.readString () == 'highkey') {
    if (colour == 'Red') {                       //a lot of typing has been done the past 10 min
      //do nothing
    }
    else if (colour == 'Yellow') {
      yellowtored ();
    }
    else if (colour == 'Green') {
      greentoyellow ();
      yellowtored ();
    }
  }

  else if (Serial.readString () == 'lowkey') {       //a low amount of typing has  been done the past 10 min
    if (colour == 'Green') {
      //do nothing
    }
    else if (colour == 'Red') {
      redtoyellow ();
      yellowtogreen ();
    }
    else if (colour == 'Yellow') {
      yellowtogreen ();
    }
  }
  
  else if (Serial.readString() == 'averagekey') {  //an average amount of typing has been done the past 10 min
    if (colour == 'Yellow') {
      //do nothing
    }
    else if (colour == 'Red') {
      redtoyellow ();
    }
    else if (colour == 'Green') {
      greentoyellow ();
    }
  }

}


