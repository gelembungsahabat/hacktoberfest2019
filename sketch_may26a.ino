    int inByte = 0;  
    int lightSensor = 0;  
    void setup() {  
      Serial.begin(9600);  
      while (!Serial) {  
        ; // wait for serial port to connect. Needed for native USB  
      }  
    }  
      
    void loop() {  
      if (Serial.available() > 0) //Waiting for request   
      {  
           inByte = Serial.read();  
           Serial.println(inByte);  
      }  
    }  
