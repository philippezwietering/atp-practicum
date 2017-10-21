#pragma once
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include "pybind11/pybind11.h"
#include "pybind11/embed.h"
#include "pybind11/eval.h"
#include <iostream>
#include <string>
#include "hwlib.hpp"
#pragma GCC diagnostic pop

namespace py = pybind11;

class Setter{
    std::string &s;
    py::object proxy;

public:

    Setter(){}

    Setter(std::string &s, py::object proxy): s(s), proxy(proxy){}

    void set(bool c){
        if(c){
            proxy.attr(s.c_str()).attr("set")(1);
        } else {
            proxy.attr(s.c_str()).attr("set")(0);
        }
    }
};

class Getter{
    std::string &s;
    py::object proxy;

public:
    Getter(){}

    Getter(std::string &s, py::object proxy): s(s), proxy(proxy){}

    int read_mm(){
        return proxy.attr(s.c_str()).attr("read_mm")().cast<int>();
    }

    int read_mc(){
        return proxy.attr(s.c_str()).attr("read_mc")().cast<int>();
    }

    char getc(){
        return proxy.attr(s.c_str()).attr("getc")().cast<char>();
    }

    bool get(hwlib::buffering buf = hwlib::buffering::unbuffered){
        return proxy.attr(s.c_str()).attr("get")(buf).cast<bool>();
    }
};

class LCDScreen{
    std::string &s;
    py::object proxy;

public:
    LCDScreen();

    LCDScreen(std::string &s, py::object proxy): s(s), proxy(proxy){}

    void putc(char c){
        proxy.attr(s.c_str()).attr("putc")(c);
    }
};

class SerialPort{
    std::string &s;
    py::object proxy;

public:
    SerialPort();

    SerialPort(std::string &s, py::object proxy): s(s), proxy(proxy){}

    char read(){
        proxy.attr(s.c_str()).attr("read")().cast<char>();
    }

    void write(std::string & text){
        proxy.attr(s.c_str()).attr("write")(text);
    }

    void clear(){
        proxy.attr(s.c_str()).attr("clear")();
    }

    std::string transaction(std::string &text, bool response = true){
        proxy.attr(s.c_str()).attr("transaction")(text, response).cast<std::string>();
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
