/// Author: Graham Joonsar ///
/// For the Whale 4 onboard control box ///
/// All thrusters are treated as servos, the arm only has steppers ///

#include <Servo.h>

// Arm Servos
Servo TWIST; int TWIST_val = 1500;
Servo TILT;  int TILT_val = 1500;

// Arm Stepper Motor
#define CLAW 25
#define CLAW_DIR 47
int CLAW_val = 0;
// This one is to keep track of the current position of the claw
int CLAW_pos = 0;

// Horizontal Motors
Servo HTL; int HTL_val = 1500;
Servo HTR; int HTR_val = 1500;
Servo HBL; int HBL_val = 1500;
Servo HBR; int HBR_val = 1500;

// Vertical Motors
Servo VTL; int VTL_val = 1500;
Servo VTR; int VTR_val = 1500;
Servo VBL; int VBL_val = 1500;
Servo VBR; int VBR_val = 1500;

Servo CAM_TILT; int CAM_TILT_val = 1500;

// Data comes in as
// TILT,TWIST,CLAW,
// HTL,HTR,HBL,HBR,
// VTL,VTR,VBL,VBR,
// CAM_TILT
//1521,1501,0,1500,1500,1500,1500,1500,1500,1500,1500,1530,\n
void ReadData(){
    // Buffer Data
    char buffer[96];
    Serial.readBytesUntil('\n', buffer, 96);
    
    TILT_val = atoi(strtok(buffer, ","));
    TWIST_val = atoi(strtok(NULL, ","));
    CLAW_val = atoi(strtok(NULL, ","));

    HTL_val = atoi(strtok(NULL, ","));
    HTR_val = atoi(strtok(NULL, ","));
    HBL_val = atoi(strtok(NULL, ","));
    HBR_val = atoi(strtok(NULL, ","));
    

    VTL_val = atoi(strtok(NULL, ","));
    VTR_val = atoi(strtok(NULL, ","));
    VBL_val = atoi(strtok(NULL, ","));
    VBR_val = atoi(strtok(NULL, ","));

    CAM_TILT_val = atoi(strtok(NULL, ","));
    
    Serial.flush();
}

void WriteToClaw(){
//  Serial.println(CLAW_pos);
//  if(CLAW_val == CLAW_pos)return;
//  if(CLAW_val > CLAW_pos){
//    digitalWrite(CLAW_DIR, HIGH);
//    //CLAW_pos++;
//  }else{
//    digitalWrite(CLAW_DIR, LOW);
//    //CLAW_pos--;
//  }
  if(CLAW_val == 0)return;
  if(CLAW_val == 1){
    digitalWrite(CLAW_DIR, HIGH);
  }else{
    digitalWrite(CLAW_DIR, LOW);
  }
  digitalWrite(CLAW, HIGH);
  delayMicroseconds(200);
  digitalWrite(CLAW, LOW);
  delayMicroseconds(200);
}

void WriteToMotors(){
    TWIST.writeMicroseconds(TWIST_val);
    TILT.writeMicroseconds(TILT_val);

    HTL.writeMicroseconds(HTL_val);
    HTR.writeMicroseconds(HTR_val);
    HBL.writeMicroseconds(HBL_val);
    HBR.writeMicroseconds(HBR_val);
    
    VTL.writeMicroseconds(VTL_val);
    VTR.writeMicroseconds(VTR_val);
    VBL.writeMicroseconds(VBL_val);
    VBR.writeMicroseconds(VBR_val);

    CAM_TILT.writeMicroseconds(CAM_TILT_val);
}

void setup(){
    Serial.begin(115200);

    pinMode(CLAW, OUTPUT);
    pinMode(CLAW_DIR, OUTPUT);
    TILT.attach(48);
    TWIST.attach(43);
    
    HTL.attach(51);
    HTR.attach(44);
    HBL.attach(52);
    HBR.attach(38);
    
    VTL.attach(27);
    VTR.attach(30);
    VBL.attach(34);
    VBR.attach(22);

    CAM_TILT.attach(33);

    WriteToMotors();
}

void loop(){
    if (Serial.available()){
        ReadData();
    }
    WriteToMotors();
    // The claw has to move a lot so we shouldn't wait to recieve a message
    WriteToClaw();
}
