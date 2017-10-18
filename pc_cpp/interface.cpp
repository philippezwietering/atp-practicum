#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include "pybind11/pybind11.h"
#pragma GCC diagnostic pop

namespace py = pybind11;

py::object py_plant = py::module::import("Simulator").attr("Plant");
py::object py_lemonator = py::module::import("Simproxy").attr("lemonator");
py::object py_simulator = py::module::import("Simulator").attr("Simulator");

// py::object py_led_yellow = py::module::import("Simproxy").attr("led_yellow");
// py::object py_led_green = py::module::import("Simproxy").attr("led_green");
// py::object py_water_pump = py::module::import("Simproxy").attr("water_pump");
// py::object py_sirup_pump = py::module::import("Simproxy").attr("sirup_pump");
// py::object py_heater = py::module::import("Simproxy").attr("heater");
// py::object py_lcd = py::module::import("Simproxy").attr("lcd");
// py::object py_colour = py::module::import("Simproxy").attr("colour");
// py::object py_distance = py::module::import("Simproxy").attr("distance");
// py::object py_reflex = py::module::import("Simproxy").attr("reflex");
// py::object py_keypad = py::module::import("Simproxy").attr("keypad");

py::object plant = py_plant.attr("__init__")();
py::object lemonator = py_lemonator.attr("__init__")(plant);
