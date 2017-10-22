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

//py::object bufferingModule = py::module::import("buffering").attr("buffering");

class Setter{
    std::string s;
    py::object proxy;

public:

    Setter(){}

    Setter(std::string s, py::object proxy): s(s), proxy(proxy){}

    void set(bool c){
        if(c){
            proxy.attr(s.c_str()).attr("set")(1);
        } else {
            proxy.attr(s.c_str()).attr("set")(0);
        }
    }
};

class Getter{
    std::string s;
    py::object proxy;

public:
    Getter(){}

    Getter(std::string s, py::object proxy): s(s), proxy(proxy){}

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
        return proxy.attr(s.c_str()).attr("get")(py::cast(buf)).cast<bool>();//Hij pakt deze cast niet en hij laadt de module bovenaan niet
    }
};

// class LCDScreen{
//     std::string s;
//     py::object proxy;

// public:
//     LCDScreen(){}

//     LCDScreen(std::string s, py::object proxy): s(s), proxy(proxy){}

//     void putc(char c){
//         proxy.attr(s.c_str()).attr("putc")(py::cast(c));
//     }
// };

class SerialPort{
    std::string s;
    py::object proxy;

public:
    SerialPort(){}

    SerialPort(std::string s, py::object proxy): s(s), proxy(proxy){}

    char read(){
        proxy.attr(s.c_str()).attr("read")().cast<char>();
    }

    void write(std::string & text){
        proxy.attr(s.c_str()).attr("write")(py::cast(text));
    }

    void clear(){
        proxy.attr(s.c_str()).attr("clear")();
    }

    std::string transaction(std::string &text, bool response = true){
        proxy.attr(s.c_str()).attr("transaction")(py::cast(text), py::cast(response)).cast<std::string>();
    }
};

class cppAdapter{
    py::object &plantMod;
    py::object proxyMod;
    py::object proxy;

public:

    Setter led_yellow;
    Setter led_green;
    Setter heater;
    Setter sirup_pump;
    Setter sirup_valve;
    Setter water_pump;
    Setter water_valve;
    SerialPort port;

    //LCDScreen lcd;
    Getter keypad;
    Getter distance;
    Getter temperature;
    Getter reflex;

    cppAdapter(py::object &plantmod) : plantMod(plantmod) {
        proxyMod = py::module::import("Simproxy").attr("lemonator");
        proxy = proxyMod(plantmod);
        led_yellow = Setter("led_yellow", proxy);
        led_green = Setter("led_green", proxy);
        heater = Setter("heater", proxy);
        sirup_pump = Setter("sirup_pump", proxy);
        sirup_valve = Setter("sirup_valve", proxy);
        water_pump = Setter("water_pump", proxy);
        water_valve = Setter("water_valve", proxy);
        port = SerialPort("port", proxy);
        //lcd = LCDScreen("lcd", proxy);
        keypad = Getter("keypad", proxy);
        distance = Getter("distance", proxy);
        temperature = Getter("temperature", proxy);
        reflex = Getter("reflex", proxy);
    }
};
