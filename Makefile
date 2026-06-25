.PHONY: all debug release run run-release clean fmt b r rel re

all: debug

# Configure only when CMakeLists change or build dir is new
build/debug/build.ninja: CMakeLists.txt src/CMakeLists.txt
	cmake -B build/debug -G Ninja -DCMAKE_BUILD_TYPE=Debug
	ln -sf debug/compile_commands.json build/compile_commands.json

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

re: clean build

fmt:
	clang-format -i $(shell find src -name '*.cpp' -o -name '*.hpp' -o -name '*.h' | grep -v '\.gen\.')

b: debug
r: run
rel: release
