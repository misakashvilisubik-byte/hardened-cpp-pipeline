#include <array>
#include <cstdint>
#include <cstddef>  

struct alignas(64) ResourceTable {
  
    static constexpr std::array<uint8_t, 16> data = {
        0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
        0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10
    };
};

template<std::size_t N> // Используем std::size_t
struct Obfuscator {
    static constexpr uint8_t transform(uint8_t v, std::size_t i) {
        return (v ^ 0xAA) + (i % 7);
    }
};

template<typename T>
[[gnu::always_inline]] void execute_logic(T& context) {
    for (std::size_t i = 0; i < T::data.size(); ++i) {
        uint8_t val = Obfuscator<16>::transform(T::data[i], i);
        // context.apply(val); 
    }
}

int main() {
    ResourceTable ctx;
    execute_logic(ctx);
    return 0;
}
