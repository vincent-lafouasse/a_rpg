.PHONY: all debug release run run-release clean fmt b r rel

all: debug

# Configure only when CMakeLists change or build dir is new
build/debug/build.ninja: CMakeLists.txt src/CMakeLists.txt
	cmake -B build/debug -G Ninja -DCMAKE_BUILD_TYPE=Debug

build/release/build.ninja: CMakeLists.txt src/CMakeLists.txt
	cmake -B build/release -G Ninja -DCMAKE_BUILD_TYPE=Release

debug: build/debug/build.ninja
	cmake --build build/debug

release: build/release/build.ninja
	cmake --build build/release

run: debug
	./build/debug/bin/rpg

run-release: release
	./build/release/bin/rpg

clean:
	rm -rf build

fmt:
	clang-format -i $(shell find src -name '*.cpp' -o -name '*.hpp' -o -name '*.h')

b: debug
r: run
rel: release
