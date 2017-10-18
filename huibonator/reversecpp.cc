#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include "pybind11/pybind11.h"
#include "pybind11/embed.h"
#pragma GCC diagnostic pop

namespace py = pybind11

int main void(){

    Py_Initialize():
    wchar_t wstr[32];
    wchar_t* args = {wstr};
    std::mbstowcs(wstr, "lemonator", 9);
    PySys_SetArgv(1, &args);

    auto simProxy = py::module::import("Simproxy")
}
