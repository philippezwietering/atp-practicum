#pragma once

#include <pybind11/pybind11.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string>
#include <algorithm>
#include <cmath>

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

enum LemonatorErrors{
    NONE,
    INVALID_INPUT,
    TEMP_TOO_HIGH,
    EMPTY_VESSEL_A,
    EMPTY_VESSEL_B,
    CUP_REMOVED,
    A_SHORTAGE,
    B_SHORTAGE
};

// Took this from stackExchange, for the lack of std library
bool isNumeric(const std::string& input){
    return !input.empty() && std::find_if(input.begin(), 
        input.end(), [](char c) { return (!std::isdigit(c) && c != '.'); }) == input.end();
}

class Controller{
public:
// Member variables
    py::object pumpA;
    py::object pumpB;
    py::object valveA;
    py::object valveB;

    py::object ledRedA;
    py::object ledGreenA;
    py::object ledRedB;
    py::object ledGreenB;
    py::object ledGreenM;
    py::object ledYellowM;

    py::object heater;
    py::object temperature;
    py::object level;
    py::object presence;
    py::object colour;

    py::object keypad;
    py::object lcd;

    LemonatorState state;
    LemonatorErrors errorState;

    std::string inputLevel;
    std::string inputTemperature;
    std::string inputRatio;
    float targetLevel;
    float startLevel;
    float targetTemperature;
    float targetRatio;
    std::string latestKeyPress;

    float aLevel;
    float bLevel;

// Methods
    Controller(py::object& pumpA, py::object& pumpB, py::object& valveA, py::object& valveB, py::object& ledRedA, py::object& ledGreenA,
               py::object& ledRedB, py::object& ledGreenB, py::object& ledGreenM, py::object& ledYellowM, py::object& heater, py::object& temperature,
               py::object& level, py::object& presence, py::object& colour, py::object& keypad, py::object& lcd);
    void initialize();
    void update();
    void idle();
    void userSelectingRatio();
    void userSelectingVolume();
    void userSelectingHeat();
    void dispensingAState();
    void dispenseA();
    void dispensingBState();
    void dispenseB();
    void checkHeckje();
    void handleHeater();
    void stopFlow();
    void updateLeds();
    void displayError();
};