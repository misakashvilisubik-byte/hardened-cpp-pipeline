#include <array>
#include <cstdint>
 
struct alignas(64) ResourceTable {
    static constexpr std::array<uint8_t, 16> data = {
        #embed "optimized_kernel_weights.bin" limit(16)
    };
};

template<size_t N>
struct Obfuscator {
    static constexpr uint8_t transform(uint8_t v, size_t i) {
        return (v ^ 0xAA) + (i % 7);
    }
};

template<typename T>
[[gnu::always_inline]] void execute_logic(T& context) {
    for (size_t i = 0; i < T::data.size(); ++i) {
        uint8_t val = Obfuscator<16>::transform(T::data[i], i);
        context.apply(val); 
    }
}
