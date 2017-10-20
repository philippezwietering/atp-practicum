#pragma once
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include "pybind11/pybind11.h"
#include "pybind11/embed.h"
#include "pybind11/eval.h"
#include <iostream>
#include <string>
#pragma GCC diagnostic pop

namespace py = pybind11;

class Setter{
    std::string a;
    py::object proxy;

public:

    Setter(){}

    Setter(std::string a, py::object proxy): a(a), proxy(proxy){}

    void set(bool c){
        if(c){
            proxy.attr(a.c_str()).attr("set")(1);
        } else {
            proxy.attr(a.c_str()).attr("set")(0);
        }
    }
};

class cppAdapter{
    py::object &plantMod;
    py::object proxyMod;
    py::object proxy;

    public:

    Setter led_yellow;
    Setter led_green;

    cppAdapter(py::object &plantmod) : plantMod(plantmod) {
        proxyMod = py::module::import("Simproxy").attr("lemonator");
        proxy = proxyMod(plantmod);
        led_yellow = Setter("led_yellow", proxy);
        led_green = Setter("led_green", proxy);
    }
};
