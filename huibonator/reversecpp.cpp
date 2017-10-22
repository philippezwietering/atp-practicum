#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include "pybind11/pybind11.h"
#include "pybind11/embed.h"
#include "pybind11/eval.h"
#include "cppadapter.hpp"
#include <iostream>
#pragma GCC diagnostic pop

namespace py = pybind11;

class MyController{

    cppAdapter &hw;

public:

    MyController(cppAdapter &adapt): hw(adapt){} //LCD doesn't work, otherwise we would say hello here

    void update(void){
        if(/* hw.keypad.getc() == 'A' &&*/ hw.reflex.get()){
            //Again, sadly can't talk to you. Come to think of it, we are just like WALL-E
            hw.sirup_valve.set(0);
            hw.sirup_pump.set(1);

            while(1){
                if(hw.distance.read_mm() < 110 || !hw.reflex.get()){
                    hw.sirup_valve.set(1);
                    hw.sirup_pump.set(0);
                    break; //Pull on the brakes!
                }
            }

            //How great it would be if we could say we are gonna do the water now
            hw.water_valve.set(0);
            hw.water_pump.set(1);

            while(1){
                if(hw.distance.read_mm() < 90 || !hw.reflex.get()){
                    hw.water_valve.set(1);
                    hw.sirup_pump.set(0);
                    break;
                }
            }
            //And we are done!
        }
    }

};
int main(void){

    // Controller ding = Controller();
    //
    //
    // //Controller *cls = &ding;
    // py::object obj = py::cast(&ding);

    //py::scoped_interpreter guard{};
    Py_Initialize();
    wchar_t wstr[32];
    wchar_t* args = {wstr};
    std::mbstowcs(wstr, "lemonator", 9);
    PySys_SetArgv(1, &args);


    auto controllerModule = py::module::import("Controller").attr("Controller");
    auto Plant = py::module::import("Simulator").attr("Plant");
    //auto simProxyModule = py::module::import("Simproxy").attr("lemonator");
    auto Simulator = py::module::import("Simulator").attr("Simulator");


    py::object Controller = controllerModule();
    py::object plant  = Plant();
    //py::object adapter = simProxyModule(plant);
    py::object sim = Simulator(plant, Controller, true);
    cppAdapter adapt = cppAdapter(plant);
    MyController dinga = MyController(adapt);

    //sim.attr("_Simulator__gui").attr("__run") = true;

    while(true){
        dinga.update();
        sim.attr("_Simulator__gui").attr("run")(true);
        //py::print(plant.attr("_effectors")["led_yellow"].attr("isOn")());
        // adapter.attr("led_yellow").attr("set")(1);
        // sim.attr("_Simulator__gui").attr("run")(true);
        // adapter.attr("led_yellow").attr("set")(0);
    }
    // while(true){
    //
    //     sim.attr("run")(false);
    //
    //
    //
    //     auto dong = py::dict(plant.attr("_effectors"));
    //
    //
    //
    //     sim.attr("run")(false);
    //
    //     adapter.attr("led_yellow").attr("set")(0);
    //
    //     py::print(dong["led_yellow"].attr("isOn")());
    //
    //     sim.attr("run")(false);
    // }

    //std::cout << dong << std::endl;
}
