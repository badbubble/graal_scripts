#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export LC_ALL=C

rm -rf benchmarks && mkdir -p benchmarks

TIMING_LOG="benchmarks/execution_times.txt"
echo "Native Image Execution Times - $(date)" > "$TIMING_LOG"
echo "----------------------------------------" >> "$TIMING_LOG"

echo "Extracting renaissance benchmark jar..."
unzip renaissance-gpl-0.16.0.jar -d benchmarks

BENCHMARKS=(
    "akka-uct"
    "fj-kmeans"
    "future-genetic"
    "mnemonics"
    "par-mnemonics"
    "rx-scrabble"
    "scala-doku"
    "scala-kmeans"
)

process_benchmark() {
    local benchmark=$1
    echo "Processing benchmark: $benchmark"
    
    local config_dir="benchmarks/${benchmark}-config"
    mkdir -p "$config_dir"

    echo "Generating native-image configuration..."
    java -agentlib:native-image-agent=config-output-dir="$config_dir" \
         -jar "benchmarks/single/${benchmark}.jar" all

    # build native image
    rm -rf "${benchmark}-original"
    echo "Building native image..."
    native-image \
        -march=compatibility \
        --no-server \
        --initialize-at-build-time \
        --report-unsupported-elements-at-runtime \
        --allow-incomplete-classpath \
        -H:+UnlockExperimentalVMOptions \
        -H:+ReportExceptionStackTraces \
        -H:ConfigurationFileDirectories="$config_dir" \
        -jar "benchmarks/single/${benchmark}.jar" "${benchmark}-original"

    echo "Running native image..."
    echo "Running $benchmark..." >> "$TIMING_LOG"
    { /usr/bin/time -f "Execution time: %e seconds" "./${benchmark}-original" all 2>&1 1>&3 | grep -v "WARNING" >&2; } 3>&1 2>> "$TIMING_LOG"
    echo "----------------------------------------" >> "$TIMING_LOG"
}

# benchmark for loop
for benchmark in "${BENCHMARKS[@]}"; do
    process_benchmark "$benchmark"
done

echo "All benchmarks processed successfully!"
echo "Execution times saved in $TIMING_LOG"