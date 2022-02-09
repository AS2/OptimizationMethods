# CMakeList.txt: проект CMake для simplex-method; включите исходный код и определения,
# укажите здесь логику для конкретного проекта.
#
cmake_minimum_required (VERSION 3.8)

# Добавьте источник в исполняемый файл этого проекта.
add_executable (simplex-method "simplex-method.cpp" "simplex-method.h" "canon_task.h" "canon_task.cpp" "error.h")

# TODO: Добавьте тесты и целевые объекты, если это необходимо.
