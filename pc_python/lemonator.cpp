#include "lemonator_proxy.hpp"

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include "pybind11/pybind11.h"
#pragma GCC diagnostic pop

namespace py = pybind11;

PYBIND11_MODULE( lemonator, m ) {
	
   py::enum_< hwlib::buffering >( m, "buffering")
      .value( "unbuffered", hwlib::buffering::unbuffered )
      .value( "buffered", hwlib::buffering::buffered )
      .export_values();

   py::class_< output_proxy >( m, "output_proxy" )
      .def_readwrite( "port", &output_proxy::port )
      .def_readwrite( "s", &std::string )
      .def( "output_proxy", &output_proxy::output_proxy, "", py::arg("port"), py::arg("s") ) 
      .def( "set", &output_proxy::set, "",
         py::arg("v"), py::arg("buffering") = hwlib::buffering::unbuffered );
   
   py::class_< lemonator_proxy >( m, "lemonator" )
      .def( py::init< int >() )
      .def_readonly( "led_yellow", &lemonator_proxy::p_led_yellow )
      .def_readwrite( "port", &lemonator_proxy::port )
      .def_readwrite( "lcd", &lemonator_proxy::p_lcd )
      .def_readwrite( "keypad", &lemonator_proxy::p_keypad)
      .def_readwrite( "distance", &lemonator_proxy::p_distance)
      .def_readwrite( "color", &lemonator_proxy::p_color)
      .def_readwrite( "temperature", &lemonator_proxy::p_temperature)
      .def_readwrite( "reflex", &lemonator_proxy::p_reflex)
      .def_readwrite( "heater", &lemonator_proxy::p_heater)
      .def_readwrite( "sirup_pump", &lemonator_proxy::p_sirup_pump)
      .def_readwrite( "sirup_valve", &lemonator_proxy::p_sirup_valve)
      .def_readwrite( "water_pump", &lemonator_proxy::p_water_pump)
      .def_readwrite( "water_valve", &lemonator_proxy::p_water_valve)
      .def_readonly( "led_green", &lemonator_proxy::p_led_green);

   py::class_< sensor_proxy >(m, "sensor_proxy")
      .def( "read_mc", &sensor_proxy::read_mc )
      .def( "read_mm", &sensor_proxy::read_mm )
      .def( "read_rgb", &sensor_proxy::read_rgb )
      .def( "getc", &sensor_proxy::getc )
      .def( "get", &sensor_proxy::get, "", py::arg("buf") = hwlib::buffering::unbuffered );

   py::class_< lcd_proxy >(m, "lcd_proxy")
      .def_readwrite( "port", &lcd_proxy::port )
      .def( "lcd_proxy", &lcd_proxy::lcd_proxy, "", py::arg("port") )
      .def( "putc", &lcd_proxy::putc, "", py::arg("c") );

   py::class_< serial_port>(m, "serial_port")
      .def_readwrite( "p", &serial_port::p )
      .def_readwrite( "log_transactions", &serial_port::log_transactions )
      .def_readwrite( "log_characters", &serial_port::log_characters)
      .def( "serial_port", &serial_port::serial_port, py::arg("p"), py::arg("log_transactions"), py::arg("log_characters") )
      .def( "read", &serial_port::read )
      .def( "write", &serial_port::write, "", py::arg("s") )
      .def( "clear", &serial_port::clear )
      .def( "transaction", &serial_port::transaction, "", py::arg("s"), py::arg("response") = true );
}

