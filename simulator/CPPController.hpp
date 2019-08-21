#pragma once

#include <pybind11/pybind11.h>

namespace py = pybind11;

py::object Constants = py::module::import("Constants");

enum LemonatorState{
    IDLE,
    ERROR,
    DISPENSING_A,
    DISPENSING_B,
    USER_SELECTING_HEAT,
    USER_SELECTING_VOLUME,
    USER_SELECTING_RATIO
};

enum ErrorStates{
    NONE,
    INVALID_INPUT,
    TEMP_TOO_HIGH,
    EMPTY_VESSEL_A,
    EMPTY_VESSEL_B,
    CUP_REMOVED,
    A_SHORTAGE,
    B_SHORTAGE
};

class Controller{
public:
// Member variables
    py::object pumpA;
    py::object pumpB;
    py::object valveA;
    py::object valveB;

    py::object redLedA;
    py::object greenLedA;
    py::object redLedB;
    py::object greenLedB;
    py::object greenLedM;
    py::object yellowLedM;

    py::object heater;
    py::object temperature;
    py::object colour;
    py::object level;
    py::object presence;

    py::object keypad;
    py::object lcd;

    LemonatorState state;
    ErrorStates error;

    std::string inputLevel;
    std::string inputTemperature;
    std::string inputRatio;
    float targetLevel;
    float targetTemperature;
    float targetRatio;
    char latestKeyPress;

    float aLevel;
    float bLevel;

// Methods
    Controller(py::object& pumpA, py::object& pumpB, py::object& valveA, py::object& valveB, py::object& redLedA, py::object& greenLedA,
               py::object& redLedB, py::object& greenLedB, py::object& greenLedM, py::object& yellowLedM, py::object& heater, py::object& temperature,
               py::object& colour, py::object& level, py::object& presence, py::object& keypad, py::object& lcd);
    void initialize();
    void update();
    void idle();
    void userSelectingRatio();
    void userSelectingVolume();
    void userSelectingHeat();
    void dispensingAState();
    void dispensingA();
    void dispensingBState();
    void dispensingB();
    void checkHeckje();
    void handleHeater();
    void stopFlow();
    void updateLeds();
    void displayError();
};