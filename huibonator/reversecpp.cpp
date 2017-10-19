#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include "pybind11/pybind11.h"
#include "pybind11/embed.h"
#include "pybind11/eval.h"
#include <iostream>
#pragma GCC diagnostic pop

namespace py = pybind11;

int main(void){

    //py::scoped_interpreter guard{};
    Py_Initialize();
    wchar_t wstr[32];
    wchar_t* args = {wstr};
    std::mbstowcs(wstr, "lemonator", 9);
    PySys_SetArgv(1, &args);

    auto Plant = py::module::import("Simulator").attr("Plant");
    auto simProxyModule = py::module::import("Simproxy").attr("lemonator");

    py::object plant  = Plant();
    py::object adapter = simProxyModule(plant);

    auto led_yellow = adapter.attr("led_yellow");

    led_yellow.attr("set")(1);

    auto dong = py::dict(plant.attr("_vessels"));

    auto obj = dong["a"];

    py::print(obj.attr("_pumping"));

    //std::cout << dong << std::endl;


}
