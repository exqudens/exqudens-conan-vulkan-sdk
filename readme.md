# exqudens-conan-vulkan-sdk

## how-to-build

1. `cmake --preset <preset-name>`
2. `cmake --build --preset <preset-name> --target cmake-install`

## how-to-export

1. `cmake --preset <preset-name>`
2. `cmake --build --preset <preset-name> --target conan-export`

## how-to-export-all

1. `conan remove -c 'vulkan-sdk'`
2. `git clean -xdf`
3. `cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | xargs -I '{}' bash -c "cmake --preset {} || exit 255"`
4. `cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | xargs -I '{}' bash -c "cmake --build --preset {} --target conan-export || exit 255"`

