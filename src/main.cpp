#include <array>
#include <string>
#include <string_view>

#include <raylib.h>
#include <tinyxml2.h>

#include "parse.hpp"

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

struct LogicalTile {
    bool traversable;
};

struct VisualTile {
    uint32_t offset;
    uint32_t tile_size;
};

class Map {
   public:
    using Line = std::vector<int>;
    using Layer = std::vector<Line>;

    static constexpr int width = 10;
    static constexpr int height = 5;
};

class MapLoader {
   private:
    static int read_int_attribute_or_die(const tinyxml2::XMLElement* const e,
                                         const char* attribute)
    {
        int out = 0;
        const IntParseError err = read_int(e->Attribute(attribute), &out);
        if (err != IntParseError::ok) {
            std::fprintf(stderr, "fatal: <%s> attribute '%s': %s\n", e->Name(),
                         attribute, message(err));
            std::abort();
        }
        return out;
    }

   public:
    static Map load_map(std::string_view path)
    {
        const std::string map_dir = "assets/maps/";
        const std::string map_path = map_dir + std::string{path};

        using namespace tinyxml2;
        XMLDocument map_xml;
        map_xml.LoadFile(map_path.c_str());

        const XMLElement* const root = map_xml.FirstChildElement("map");
        const int width = read_int_attribute_or_die(root, "width");
        const int height = read_int_attribute_or_die(root, "height");
        const int tilewidth = read_int_attribute_or_die(root, "tilewidth");
        const int tileheight = read_int_attribute_or_die(root, "tileheight");

        std::printf("width:\t\t%i\n", width);
        std::printf("height:\t\t%i\n", height);
        std::printf("tilewidth:\t%i\n", tilewidth);
        std::printf("tileheight:\t%i\n", tileheight);

        return {};
    }
};

class Renderer {
   public:
    static constexpr int s_tile_size = 64;

   private:
    static constexpr const char* s_window_name = "rpg";
    static constexpr int s_target_fps = 60;
    static constexpr std::string_view s_sprite_dir = "assets/sprites/";
    static constexpr int s_window_width = s_tile_size * Map::width;
    static constexpr int s_window_height = s_tile_size * Map::height;

   public:
    Renderer() : m_tile()
    {
        InitWindow(s_window_width, s_window_height, s_window_name);
        SetTargetFPS(s_target_fps);

        const std::string sprite_dir{s_sprite_dir};
        const std::string tile_dir =
            sprite_dir + "kenney_micro-roguelike/Tiles/Colored/";
        const std::string tile_path = tile_dir + "tile_0000.png";
        m_tile = LoadTexture(tile_path.c_str());
    }
    ~Renderer()
    {
        UnloadTexture(m_tile);
        CloseWindow();
    }

    void render(const Map& map) const
    {
        (void)map;  // not actually using a map yet, just spamming a tile
        BeginDrawing();
        ClearBackground(RAYWHITE);

        for (int row = 0; row < Map::height; ++row) {
            for (int col = 0; col < Map::width; ++col) {
                Rectangle src{0, 0, FLOAT(m_tile.width), FLOAT(m_tile.height)};
                Rectangle dst{
                    FLOAT(col * s_tile_size),
                    FLOAT(row * s_tile_size),
                    FLOAT(s_tile_size),
                    FLOAT(s_tile_size),
                };
                DrawTexturePro(m_tile, src, dst, {0, 0}, 0.0f, WHITE);
            }
        }

        EndDrawing();
    }

   private:
    Texture2D m_tile;
};

int main()
{
    Renderer renderer;
    Map map = MapLoader::load_map("test1.tmx");

    while (!WindowShouldClose()) {
        renderer.render(map);
    }
}
