int voltage, current, readingType = 0;
byte status;

void setup() {
    // ADMUX = ADMUX & B00111111 set analog reference to external with registry
    ADCSRA = ADCSRA | B00000100;
    ADCSRA = ADCSRA & B11111100;
    analogReference(EXTERNAL);
    Serial.begin(115200); // TODO: adjust

    pinMode(A0, INPUT); // current value
    pinMode(A1, INPUT); // current offset
    pinMode(A2, INPUT); // voltage value
    pinMode(A3, INPUT); // voltage offset
    delay(5000);    // wait for the offset capacitors to charge
}

void loop() {
    if (Serial.available() > 0) {
        readingType = Serial.read();
        delay(1);
    }
    if (readingType > 0) {
        status = B00000000;
        if (readingType == 1) {
            voltage = analogRead(A2)-analogRead(A3);
        }
        current = analogRead(A0)-analogRead(A1);
        if (readingType == 1) {
            Serial.write(abs(voltage) >> 2);
        }
        Serial.write(abs(current) >> 2);
        if (voltage < 0 && readingType == 1) {
            status |= B00000001;
        }
        if (current < 0) {
            status |= B00000010;
        }
        Serial.write(status);
    }
    delayMicroseconds(300);
}
