/// Author: Graham Joonsar ///
/// For the Whale 4 onboard control box ///
/// All thrusters are treated as servos, the arm only has steppers ///

#include <Servo.h>
#include <Stepper.h>

/// Setting up the tilt stepper ///
// TODO MAKE THE PIN NUMBERS ACCURATE
const int SPR = 200;
Stepper TILT_stepper (SPR, 8, 9, 10, 11);   int TILT_val  = 0;
Stepper TWIST_stepper(SPR, 12, 13, 14, 15); int TWIST_val = 0;
Stepper CLAW_stepper (SPR, 16, 17, 18, 19); int CLAW_val  = 0;

// TODO find out actually good speeds for these
TILT_stepper.setSpeed(10);
TWIST_stepper.setSpeed(10);
CLAW_stepper.setSpeed(10);

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

void WriteToMotors(){
    TILT_stepper.step(TILT_val);
    TWIST_stepper.step(TWIST_val);
    CLAW_stepper.step(CLAW_val);

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
    Serial.begin(9600);

    // PIN # NEED TO BE UPDATED!!!
    HTL.attach(22);
    HTR.attach(51);
    HBL.attach(30);
    HBR.attach(38);
    
    VTL.attach(0);
    VTR.attach(0);
    VBL.attach(0);
    VBR.attach(0);

    CAM_TILT.attach(33);

    WriteToMotors();
}

void loop(){
    if (Serial.available()){
        ReadData();
        WriteToMotors();
    }
}
