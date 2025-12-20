#include <pybind11/pybind11.h>
#include "augmentator.hpp"

namespace py = pybind11;

PYBIND11_MODULE(fast_augmentation, m) {
    m.doc() = "Fast augmentation module implemented in C++"; // Optional module docstring

    m.def("process_json", &process_json, "Process augmentation from JSON string",
          py::arg("data"), py::arg("in_dir"), py::arg("out_dir"),py::arg("label_names"));
}