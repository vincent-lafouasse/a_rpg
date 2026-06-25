#pragma once

//! core module
// is included by pretty much everybody
// includes no-one, generally has no dependencies beyond libc[++]

#include <array>
#include <concepts>
#include <type_traits>

#define FLOAT(expr) (static_cast<float>(expr))

template <typename T>
concept Vec2Scalar = std::same_as<T, int> || std::same_as<T, float>;

template <Vec2Scalar T>
struct Vec2 {
    T x{};
    T y{};
};

using Vec2f = Vec2<float>;
using Vec2i = Vec2<int>;

template <typename T, std::size_t W, std::size_t H>
struct FlatArray {
    static constexpr int width = W;
    static constexpr int height = H;

    std::array<T, W * H> inner;

    [[nodiscard]] static bool in_bounds(int const x, int const y)
    {
        return x >= 0 && x < W && y >= 0 && y < H;
    }

    [[nodiscard]] const T& at(int const row, const int col) const
    {
        return inner[row * W + col];
    }

    [[nodiscard]] T& at(int const row, const int col)
    {
        return inner[row * W + col];
    }
};
