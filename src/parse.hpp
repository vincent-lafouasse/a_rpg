#pragma once

#include <cerrno>
#include <climits>
#include <cstdlib>

enum class IntParseError {
    ok,
    null_input,
    empty,
    invalid_char,
    overflow,
    trailing,
};

static inline const char* message(IntParseError e)
{
    switch (e) {
        case IntParseError::ok:
            return "ok";
        case IntParseError::null_input:
            return "null input";
        case IntParseError::empty:
            return "empty string";
        case IntParseError::invalid_char:
            return "invalid character";
        case IntParseError::overflow:
            return "value out of range";
        case IntParseError::trailing:
            return "trailing characters after number";
    }
}

// Returns IntParseError::ok and writes to *out on success.
// On failure, *out is unchanged.
static inline IntParseError read_int(const char* s, int* out)
{
    if (s == nullptr)
        return IntParseError::null_input;
    if (*s == '\0')
        return IntParseError::empty;

    char* end;
    errno = 0;
    const long val = std::strtol(s, &end, 10);

    if (end == s)
        return IntParseError::invalid_char;
    if (*end != '\0')
        return IntParseError::trailing;
    if (errno == ERANGE || val < INT_MIN || val > INT_MAX)
        return IntParseError::overflow;

    *out = static_cast<int>(val);
    return IntParseError::ok;
}
