.PHONY: all
all: build

.PHONY: build
build: ./build/src/rpg

./build/src/rpg:
	cmake -B build -G Ninja
	cmake --build build --target rpg

.PHONY: build
run: build
	./build/src/rpg


.PHONY: format
format:
	clang-format -i $(shell find src -name '*.cpp' -or -name '*.hpp' -or -name '*.h')

.PHONY: b r t vt fmt
b: build
r: run
t: test
vt: verbose_test
fmt: format
