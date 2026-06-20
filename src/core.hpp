#pragma once

#include <array>

#define FLOAT(expr) (static_cast<float>(expr))

template <typename T, std::size_t W, std::size_t H>
struct FlatArray {
    static constexpr int width = W;
    static constexpr int height = H;

    std::array<T, W * H> inner{};

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
