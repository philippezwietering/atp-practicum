#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include "pybind11/pybind11.h"
#include "pybind11/embed.h"
#pragma GCC diagnostic pop

namespace py = pybind11

int main void(){
    py::scoped_interperter python;

    auto simproxy = py::module::import("Simproxy")
}
