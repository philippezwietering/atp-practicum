#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include "pybind11/pybind11.h"
#include "pybind11/embed.h"
#include "pybind11/eval.h"
#include <iostream>
#include <thread>
#pragma GCC diagnostic pop

namespace py = pybind11;

// class Controller{
//
//     py::object proxyMod;
//     py::object plantMod;
//     py::object proxy;
//
// public:
//
//     Controller(){
//         Py_Initialize();
//         wchar_t wstr[32];
//         wchar_t* args = {wstr};
//         std::mbstowcs(wstr, "lemonator", 9);
//         PySys_SetArgv(1, &args);
//
//         proxyMod = py::module::import("Simproxy").attr("lemonator");
//         plantMod = py::module::import("Simulator").attr("Plant");
//         proxy = proxyMod(plantMod());
//     }
//
//     void update(void){
//         proxy.attr("led_yellow").attr("set")(1);
//         proxy.attr("led_yellow").attr("set")(0);
//     }
//
// };
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
    auto simProxyModule = py::module::import("Simproxy").attr("lemonator");
    auto Simulator = py::module::import("Simulator").attr("Simulator");

    py::object Controller = controllerModule();
    py::object plant  = Plant();
    py::object adapter = simProxyModule(plant);
    py::object sim = Simulator(plant, Controller, true);


    // while(true){
    //
    //     sim.attr("run")(false);
    //
    //
    //
    //     auto dong = py::dict(plant.attr("_effectors"));
    //
    //     py::print(dong["led_yellow"].attr("isOn")());
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
