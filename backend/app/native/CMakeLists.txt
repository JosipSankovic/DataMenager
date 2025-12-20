cmake_minimum_required(VERSION 3.10)

project(fast_augmentation VERSION 1.0)

#ukljucivanje pybind
include(FetchContent)
FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11
  GIT_TAG        v2.11.1
)
FetchContent_MakeAvailable(pybind11)
cmake_policy(SET CMP0074 NEW)
find_package(OpenCV REQUIRED)
find_package(nlohmann_json REQUIRED)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include_directories(include src)
add_executable(fast_augmentation_cli
  src/main.cpp
 src/augmentator.cpp
)
# target_include_directories(fast_augmentation_cli PRIVATE ${CMAKE_SOURCE_DIR}/include)

target_link_libraries(fast_augmentation_cli PRIVATE ${OpenCV_LIBS} nlohmann_json::nlohmann_json)


# --- 3. Python Modul (Ovo je novo!) ---
# Naziv targeta "fast_augmentation" mora odgovarati onome u PYBIND11_MODULE u bindings.cpp
pybind11_add_module(fast_augmentation 
    src/bindings.cpp 
    src/augmentator.cpp 
)

# Linkanje biblioteka na modul
target_link_libraries(fast_augmentation PRIVATE ${OpenCV_LIBS} nlohmann_json::nlohmann_json)

# Postavke za Windows (da se modul zove ispravno)
set_target_properties(fast_augmentation PROPERTIES PREFIX "${PYTHON_MODULE_PREFIX}")
set_target_properties(fast_augmentation PROPERTIES SUFFIX "${PYTHON_MODULE_EXTENSION}")

# --- DODAJTE OVO NA KRAJ ---
# Ovo kaže: "Kopiraj gotovi modul (fast_augmentation) u korijen paketa"
install(TARGETS fast_augmentation DESTINATION .)