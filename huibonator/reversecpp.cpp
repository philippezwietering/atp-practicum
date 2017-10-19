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

    adapter.attr("led_yellow").attr("set")(1);

    auto dong = py::dict(plant.attr("_effectors"));

    py::print(dong["led_yellow"].attr("isOn")());

    adapter.attr("led_yellow").attr("set")(0);

    py::print(dong["led_yellow"].attr("isOn")());

    //std::cout << dong << std::endl;
}
