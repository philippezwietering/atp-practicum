/*cppimport
<%
setup_pybind11(cfg)
cfg['compiler_args'] = ['-fvisibility=hidden']
%>
*/

// The above is necessary for cppimport to find the file so it can be easily loaded into Python

#include "CPPController.hpp"

Controller::Controller(py::object& pumpA, py::object& pumpB, py::object& valveA, py::object& valveB, py::object& redLedA, py::object& greenLedA,
                       py::object& redLedB, py::object& greenLedB, py::object& greenLedM, py::object& yellowLedM, py::object& heater, py::object& temperature,
                       py::object& colour, py::object& level, py::object& presence, py::object& keypad, py::object& lcd) 
                       : pumpA(pumpA), pumpB(pumpB), valveA(valveA), redLedA(redLedA), greenLedA(greenLedA), redLedB(redLedB), greenLedB(greenLedB),
                         greenLedM(greenLedM), yellowLedM(yellowLedM), heater(heater), temperature(temperature), colour(colour), level(level), 
                         presence(presence), keypad(keypad), lcd(lcd) 
    {
        py::object storageMax = Constants.attr("storageMax");
        aLevel = py::cast<float>(storageMax);
        bLevel = aLevel;
    }

void Controller::initialize(){

}

void Controller::update(){

}

void Controller::idle(){

}

void Controller::userSelectingRatio(){

}

void Controller::userSelectingVolume(){

}

void Controller::userSelectingHeat(){

}

void Controller::dispensingAState(){

}

void Controller::dispensingA(){

}

void Controller::dispensingBState(){

}

void Controller::dispensingB(){

}

void Controller::checkHeckje(){

}

void Controller::handleHeater(){

}

void Controller::stopFlow(){

}

void Controller::updateLeds(){

}

void Controller::displayError(){

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

// ErrorStates
py::enum_<ErrorStates>(module, "ErrorStates").value("NONE", ErrorStates::NONE)
                                             .value("INVALID_INPUT", ErrorStates::INVALID_INPUT)
                                             .value("TEMP_TOO_HIGH", ErrorStates::TEMP_TOO_HIGH)
                                             .value("EMPTY_VESSEL_A", ErrorStates::EMPTY_VESSEL_A)
                                             .value("EMPTY_VESSEL_B", ErrorStates::EMPTY_VESSEL_B)
                                             .value("CUP_REMOVED", ErrorStates::CUP_REMOVED)
                                             .value("A_SHORTAGE", ErrorStates::A_SHORTAGE)
                                             .value("B_SHORTAGE", ErrorStates::B_SHORTAGE)
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
                                            .def("dispensingA", &Controller::dispensingA)
                                            .def("dispensingBState", &Controller::dispensingBState)
                                            .def("dispensingB", &Controller::dispensingB)
                                            .def("checkHeckje", &Controller::checkHeckje)
                                            .def("handleHeater", &Controller::handleHeater)
                                            .def("stopFlow", &Controller::stopFlow)
                                            .def("updateLeds", &Controller::updateLeds)
                                            .def("displayError", &Controller::displayError)
                                            .def_readwrite("pumpA", &Controller::pumpA)
                                            .def_readwrite("pumpB", &Controller::pumpB)
                                            .def_readwrite("valveA", &Controller::valveA)
                                            .def_readwrite("valveB", &Controller::valveB)
                                            .def_readwrite("redLedA", &Controller::redLedA)
                                            .def_readwrite("greenLedA", &Controller::greenLedA)
                                            .def_readwrite("redLedB", &Controller::redLedB)
                                            .def_readwrite("greenLedB", &Controller::greenLedB)
                                            .def_readwrite("greenLedM", &Controller::greenLedM)
                                            .def_readwrite("yellowLedM", &Controller::yellowLedM)
                                            .def_readwrite("heater", &Controller::heater)
                                            .def_readwrite("temperature", &Controller::temperature)
                                            .def_readwrite("colour", &Controller::colour)
                                            .def_readwrite("level", &Controller::level)
                                            .def_readwrite("presence", &Controller::presence)
                                            .def_readwrite("keypad", &Controller::keypad)
                                            .def_readwrite("lcd", &Controller::lcd)
                                            .def_readwrite("state", &Controller::state)
                                            .def_readwrite("error", &Controller::error)
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