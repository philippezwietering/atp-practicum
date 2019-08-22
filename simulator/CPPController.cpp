/*cppimport
<%
setup_pybind11(cfg)
cfg['compiler_args'] = ['-fvisibility=hidden']
%>
*/

// The above is necessary for cppimport to find the file so it can be easily loaded into Python

#include "CPPController.hpp"

Controller::Controller(py::object& pumpA, py::object& pumpB, py::object& valveA, py::object& valveB, py::object& ledRedA, py::object& ledGreenA,
                       py::object& ledRedB, py::object& ledGreenB, py::object& ledGreenM, py::object& ledYellowM, py::object& heater, py::object& temperature,
                       py::object& level, py::object& presence, py::object& colour, py::object& keypad, py::object& lcd) 
                       : pumpA(pumpA), pumpB(pumpB), valveA(valveA), valveB(valveB), ledRedA(ledRedA), ledGreenA(ledGreenA), ledRedB(ledRedB), ledGreenB(ledGreenB),
                         ledGreenM(ledGreenM), ledYellowM(ledYellowM), heater(heater), temperature(temperature), level(level), 
                         presence(presence), colour(colour), keypad(keypad), lcd(lcd) 
    {
        aLevel = Constants.attr("storageMax").cast<float>();
        bLevel = aLevel;

        state = IDLE;
        errorState = NONE;

        inputLevel = "";
        inputTemperature = "";
        inputRatio = "";
        latestKeyPress = "";

        targetLevel = -1;
        startLevel = -1;
        targetTemperature = -1;
        targetRatio = -1;
    }

void Controller::initialize(){
    lcd.attr("clear")();
    while(std::string(py::str(keypad.attr("pop")())).compare("\x00") == 0){
        continue;
    }
}

void Controller::update(){
    updateLeds();
    latestKeyPress = std::string(py::str(keypad.attr("pop")()));

    lcd.attr("pushString")("\x0c    LEMONATOR\n--------------------\n");

    if(errorState != NONE){
        state = ERROR;
        stopFlow();

        inputLevel = "";
        inputTemperature = "";
        inputRatio = "";

        displayError();
    }

    if(pumpA.attr("isOn")().cast<bool>()){
        if(aLevel <= 0){
            stopFlow();
            errorState = EMPTY_VESSEL_A;
        }
    }

    if(pumpB.attr("isOn")().cast<bool>()){
        if(bLevel <= 0){
            stopFlow();
            errorState = EMPTY_VESSEL_B;
        }
    }

    if((inputTemperature.compare("") != 0 && state != USER_SELECTING_HEAT) || targetTemperature != -1){
        handleHeater();
    }

    // State machine
    switch(state){
        case IDLE : idle(); break;
        case USER_SELECTING_RATIO: userSelectingRatio(); break;
        case USER_SELECTING_VOLUME: userSelectingVolume(); break;
        case USER_SELECTING_HEAT: userSelectingHeat(); break;
        case DISPENSING_A: dispensingAState(); break;
        case DISPENSING_B: dispensingBState(); break;
        default: break;
    }
}

void Controller::idle(){
    checkHeckje();
    lcd.attr("pushString")("Press A to start\nPress # to cancel");

    if(latestKeyPress.compare("A") == 0){
        state = USER_SELECTING_RATIO;
    }
}

void Controller::userSelectingRatio(){
    checkHeckje();

    if(isdigit(latestKeyPress.front())){
        inputRatio += latestKeyPress;
    }

    if(latestKeyPress.compare("*") == 0){
        if(inputRatio.compare("") == 0 || !isNumeric(inputRatio) || std::stof(inputRatio) <= 0.0){
            errorState = INVALID_INPUT;
            return;
        }
        targetRatio = std::stof(inputRatio);
        inputRatio = "";
        state = USER_SELECTING_VOLUME;
    }
    lcd.attr("pushString")("Desired vol. ratio:\n1 to " + inputRatio + " | B to A (*)");
}

void Controller::userSelectingVolume(){
    checkHeckje();

    if(isdigit(latestKeyPress.front())){
        inputLevel += latestKeyPress;
    }

    if(latestKeyPress.compare("*") == 0){
        if(inputLevel.compare("") == 0 || !isNumeric(inputLevel) || std::stof(inputLevel) <= 0.0){
            errorState = INVALID_INPUT;
            return;
        }

        targetLevel = std::stof(inputLevel);
        if(targetLevel / (targetRatio + 1) > bLevel){
            errorState = B_SHORTAGE;
            return;
        }

        if(targetLevel * targetRatio / (targetRatio + 1) > aLevel){
            errorState = A_SHORTAGE;
            return;
        }

        startLevel = level.attr("_convertToValue")().cast<float>();
        if(startLevel + targetLevel > Constants.attr("liquidMax").cast<float>()){
            errorState = INVALID_INPUT;
            return;
        }

        inputLevel = "";
        state = USER_SELECTING_HEAT;
    }
    lcd.attr("pushString")("Desired volume:\n" + inputLevel + " ml (*)");
}

void Controller::userSelectingHeat(){
    checkHeckje();

    if(isdigit(latestKeyPress.front())){
        inputTemperature += latestKeyPress;
    }

    if(latestKeyPress.compare("*") == 0){
        if(inputTemperature.compare("") == 0 || !isNumeric(inputTemperature)){
            errorState = INVALID_INPUT;
            return;
        }

        targetTemperature = std::stof(inputTemperature);
        if(targetTemperature < Constants.attr("environmentTemp").cast<float>()){
            targetTemperature = Constants.attr("environmentTemp").cast<float>();
        }
        else if(targetTemperature > 90){
            targetTemperature = -1;
            errorState = TEMP_TOO_HIGH;
            return;
        }

        inputTemperature = "";
        state = DISPENSING_B;
    }
    lcd.attr("pushString")("Desired temperature:\n" + inputTemperature + " deg C (*)");
}

void Controller::dispensingAState(){
    checkHeckje();

    if(!(presence.attr("readValue")().cast<bool>())){
        stopFlow();
        errorState = CUP_REMOVED;
        return;
    }

    dispenseA();

    float desiredALevel = startLevel + targetLevel;
    float currentLevel = level.attr("_convertToValue")().cast<float>();
    if(currentLevel >= desiredALevel){
        stopFlow();
        aLevel -= targetLevel * targetRatio / (targetRatio + 1);
        state = IDLE;
    }

    std::string levelString = std::to_string((int)currentLevel);
    std::string desiredString = std::to_string((int)desiredALevel);
    lcd.attr("pushString")("Dispensing A\n" + levelString + " / " + desiredString + " progress");
}

void Controller::dispenseA(){
    if(!(pumpA.attr("isOn")().cast<bool>())){
        pumpA.attr("switchOn")();
    }

    if(valveA.attr("isOn")().cast<bool>()){
        valveA.attr("switchOff")();
    }
}

void Controller::dispensingBState(){
    checkHeckje();

    if(!(presence.attr("readValue")().cast<bool>())){
        stopFlow();
        errorState = CUP_REMOVED;
        return;
    }

    dispenseB();

    float desiredBLevel = startLevel + targetLevel / (targetRatio + 1);
    py::print(py::cast(desiredBLevel));
    float currentLevel = level.attr("_convertToValue")().cast<float>();
    if(currentLevel >= desiredBLevel){
        stopFlow();
        bLevel -= targetLevel / (targetRatio + 1);
        state = DISPENSING_A;
    }

    std::string levelString = std::to_string((int)currentLevel);
    std::string desiredString = std::to_string((int)desiredBLevel);
    lcd.attr("pushString")("Dispensing B\n" + levelString + " / " + desiredString + " progress");
}

void Controller::dispenseB(){
    if(!(pumpB.attr("isOn")().cast<bool>())){
        pumpB.attr("switchOn")();
    }

    if(valveB.attr("isOn")().cast<bool>()){
        valveB.attr("switchOff")();
    }
}

void Controller::checkHeckje(){
    if(latestKeyPress.compare("#") == 0){
        state = IDLE;
        stopFlow();
        heater.attr("switchOff")();
        targetTemperature = -1;
    }
}

void Controller::handleHeater(){
    if(!(presence.attr("readValue")().cast<bool>())){
        heater.attr("switchOff")();
        return;
    }

    if(targetTemperature >= 0 && temperature.attr("_convertToValue")().cast<float>() < targetTemperature){
        heater.attr("switchOn")();
    } else{
        heater.attr("switchOff")();
    }
}

void Controller::stopFlow(){
    valveA.attr("switchOn")();
    valveB.attr("switchOn")();

    if(pumpA.attr("isOn")().cast<bool>()){
        pumpA.attr("switchOff")();
    }
    if(pumpB.attr("isOn")().cast<bool>()){
        pumpB.attr("switchOff")();
    }
}

void Controller::updateLeds(){
    if(pumpA.attr("isOn")().cast<bool>() && !(valveA.attr("isOn")().cast<bool>())){
        ledGreenA.attr("switchOn")();
        ledRedA.attr("switchOff")();
    } else{
        ledGreenA.attr("switchOff")();
        ledRedA.attr("switchOn")();
    }

    if(pumpB.attr("isOn")().cast<bool>() && !(valveB.attr("isOn")().cast<bool>())){
        ledGreenB.attr("switchOn")();
        ledRedB.attr("switchOff")();
    } else{
        ledGreenB.attr("switchOff")();
        ledRedB.attr("switchOn")();
    }

    if(heater.attr("isOn")().cast<bool>()){
        ledYellowM.attr("switchOn")();
        ledGreenM.attr("switchOff")();
    } else{
        ledYellowM.attr("switchOff")();
        ledGreenM.attr("switchOn")();
    }
}

void Controller::displayError(){
    lcd.attr("pushString")("\x0c   ERROR\n--------------------\n");

    std::string errorMessage = "";
    switch(errorState){
        case NONE: return;
        case EMPTY_VESSEL_A: errorMessage = "Vessel A is empty"; break;
        case EMPTY_VESSEL_B: errorMessage = "Vessel B is empty"; break;
        case INVALID_INPUT: errorMessage = "Input is invalid"; break;
        case TEMP_TOO_HIGH: errorMessage = "Input temp is too high"; break;
        case CUP_REMOVED: errorMessage = "Cup was removed"; break;
        case A_SHORTAGE: errorMessage = "Too little in A"; break;
        case B_SHORTAGE: errorMessage = "Too little in B"; break;
        default: break;
    }

    lcd.attr("pushString")(errorMessage + "\nPress # to return");
    if(latestKeyPress.compare("#") == 0){
        state = IDLE;
        errorState = NONE;
    }
}

// LemonatorStates
PYBIND11_MODULE(CPPController, module){
py::enum_<LemonatorState>(module, "LemonatorState").value("IDLE", LemonatorState::IDLE)
                                                   .value("ERROR", LemonatorState::ERROR)
                                                   .value("DISPENSING_A", LemonatorState::DISPENSING_A)
                                                   .value("DISPENSING_B", LemonatorState::DISPENSING_B)
                                                   .value("USER_SELECTING_HEAT", LemonatorState::USER_SELECTING_HEAT)
                                                   .value("USER_SELECTING_VOLUME", LemonatorState::USER_SELECTING_VOLUME)
                                                   .value("USER_SELECTING_RATIO", LemonatorState::USER_SELECTING_RATIO)
                                                   .export_values();

// LemonatorErrors
py::enum_<LemonatorErrors>(module, "LemonatorErrors").value("NONE", LemonatorErrors::NONE)
                                             .value("INVALID_INPUT", LemonatorErrors::INVALID_INPUT)
                                             .value("TEMP_TOO_HIGH", LemonatorErrors::TEMP_TOO_HIGH)
                                             .value("EMPTY_VESSEL_A", LemonatorErrors::EMPTY_VESSEL_A)
                                             .value("EMPTY_VESSEL_B", LemonatorErrors::EMPTY_VESSEL_B)
                                             .value("CUP_REMOVED", LemonatorErrors::CUP_REMOVED)
                                             .value("A_SHORTAGE", LemonatorErrors::A_SHORTAGE)
                                             .value("B_SHORTAGE", LemonatorErrors::B_SHORTAGE)
                                             .export_values();

py::class_<Controller>(module, "Controller").def(py::init<py::object&, py::object&, py::object&, py::object&, py::object&, 
                                                          py::object&, py::object&, py::object&, py::object&, py::object&, py::object&, 
                                                          py::object&, py::object&, py::object&, py::object&, py::object&, py::object&>())
                                            .def("initialize", &Controller::initialize)
                                            .def("update", &Controller::update)
                                            .def("idle", &Controller::idle)
                                            .def("userSelectingRatio", &Controller::userSelectingRatio)
                                            .def("userSelectingVolume", &Controller::userSelectingVolume)
                                            .def("userSelectingHeat", &Controller::userSelectingHeat)
                                            .def("dispensingAState", &Controller::dispensingAState)
                                            .def("dispenseA", &Controller::dispenseA)
                                            .def("dispensingBState", &Controller::dispensingBState)
                                            .def("dispenseB", &Controller::dispenseB)
                                            .def("checkHeckje", &Controller::checkHeckje)
                                            .def("handleHeater", &Controller::handleHeater)
                                            .def("stopFlow", &Controller::stopFlow)
                                            .def("updateLeds", &Controller::updateLeds)
                                            .def("displayError", &Controller::displayError)
                                            .def_readwrite("pumpA", &Controller::pumpA)
                                            .def_readwrite("pumpB", &Controller::pumpB)
                                            .def_readwrite("valveA", &Controller::valveA)
                                            .def_readwrite("valveB", &Controller::valveB)
                                            .def_readwrite("ledRedA", &Controller::ledRedA)
                                            .def_readwrite("ledGreenA", &Controller::ledGreenA)
                                            .def_readwrite("ledRedB", &Controller::ledRedB)
                                            .def_readwrite("ledGreenB", &Controller::ledGreenB)
                                            .def_readwrite("ledGreenM", &Controller::ledGreenM)
                                            .def_readwrite("ledYellowM", &Controller::ledYellowM)
                                            .def_readwrite("heater", &Controller::heater)
                                            .def_readwrite("temperature", &Controller::temperature)
                                            .def_readwrite("level", &Controller::level)
                                            .def_readwrite("presence", &Controller::presence)
                                            .def_readwrite("colour", &Controller::colour)
                                            .def_readwrite("keypad", &Controller::keypad)
                                            .def_readwrite("lcd", &Controller::lcd)
                                            .def_readwrite("state", &Controller::state)
                                            .def_readwrite("errorState", &Controller::errorState)
                                            .def_readwrite("inputLevel", &Controller::inputLevel)
                                            .def_readwrite("inputTemperature", &Controller::inputTemperature)
                                            .def_readwrite("inputRatio", &Controller::inputRatio)
                                            .def_readwrite("targetLevel", &Controller::targetLevel)
                                            .def_readwrite("targetTemperature", &Controller::targetTemperature)
                                            .def_readwrite("targetRatio", &Controller::targetRatio)
                                            .def_readwrite("latestKeyPress", &Controller::latestKeyPress)
                                            .def_readwrite("aLevel", &Controller::aLevel)
                                            .def_readwrite("bLevel", &Controller::bLevel);

}