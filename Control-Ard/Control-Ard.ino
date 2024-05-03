#include "IRremote.hpp"
#include <LiquidCrystal.h>

#define DECODE_NEC
#define IR_RECEIVE_PIN 2

const int rs = 12, en = 11, d4 = 6, d5 = 5, d6 = 4, d7 = 3;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  pinMode(8, OUTPUT);
  digitalWrite(8, LOW);
  analogWrite(9,35); //Contraste
  analogWrite(10,200); //Brillo
  lcd.begin(16,2);
  Serial.begin(9600);
  IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK);  
}

void loop() {
  String cadena1 = ""; // Para almacenar la primera parte de la cadena
  String cadena2 = ""; // Para almacenar la segunda parte de la cadena
  byte data[31];
  if (Serial.available()){
    delay(100);
    lcd.clear();
    while (Serial.available() >= sizeof(data)) {
      for (int i = 0; i < sizeof(data); i++){
        data[i] = Serial.read();
      }
    }
  }
  for (int i = 1; i <= 16; i++){
    int j = i - 1;
    lcd.setCursor(j, 0);
    lcd.write(data[i]);
    Serial.write(data[i]);
    delay(10);
  }
  for (int i = 17; i <= sizeof(data); i++){
    int j = i - 17;
    lcd.setCursor(j - 17, 1);
    lcd.write(data[i]);
  }

  if (IrReceiver.decode()) {
    if (IrReceiver.decodedIRData.protocol == NEC) Serial.println(IrReceiver.decodedIRData.command, HEX);
      delay(50);
      IrReceiver.resume();
  }
}