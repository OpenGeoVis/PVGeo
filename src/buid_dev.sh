pushd "$(dirname "$0")"

# filters under development:
for filename in ./filters/dev_*.py; do
    filtername="${filename%.*}"
    python2 python_filter_generator.py $filename "../build/$(basename "$filtername").xml"
done
sh ./build_plugins.sh
popd
