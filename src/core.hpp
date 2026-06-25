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

    static const Vec2 zero;
    static const Vec2 e_x;
    static const Vec2 e_y;

    [[nodiscard]] static constexpr Vec2 add(Vec2 a, Vec2 b)
    {
        return {.x = a.x + b.x, .y = a.y + b.y};
    }

    [[nodiscard]] static constexpr Vec2 sub(Vec2 a, Vec2 b)
    {
        return {.x = a.x - b.x, .y = a.y - b.y};
    }

    [[nodiscard]] static constexpr Vec2 negate(Vec2 v)
    {
        return {.x = -v.x, .y = -v.y};
    }

    [[nodiscard]] static constexpr T dot(Vec2 a, Vec2 b)
    {
        return a.x * b.x + a.y * b.y;
    }

    [[nodiscard]] static constexpr Vec2 scale(Vec2 v, T scalar)
    {
        return {.x = scalar * v.x, .y = scalar * v.y};
    }
};

template <Vec2Scalar T>
inline constexpr Vec2<T> Vec2<T>::zero = {};
template <Vec2Scalar T>
inline constexpr Vec2<T> Vec2<T>::e_x = {.x = static_cast<T>(1)};
template <Vec2Scalar T>
inline constexpr Vec2<T> Vec2<T>::e_y = {.y = static_cast<T>(1)};

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
