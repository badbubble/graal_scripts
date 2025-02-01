#!/bin/bash

# download benchmark
#wget https://github.com/renaissance-benchmarks/renaissance/releases/download/v0.16.0/renaissance-gpl-0.16.0.jar

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DATA_DIR="$SCRIPT_DIR/data"
BENCHMARK_DIR="$SCRIPT_DIR/renaissance-gpl-0.16.0.jar"
export LC_ALL=C

rm -rf "$DATA_DIR"
mkdir -p "$DATA_DIR"

TIMING_LOG="$DATA_DIR/jit_timing_result.txt"
echo "Benchmark Timing Results - $(date)" > "$TIMING_LOG"
echo "----------------------------------------" >> "$TIMING_LOG"

cd ../graal_data_collection/compiler
mx build

JVM_OPTS="-XX:+UnlockExperimentalVMOptions -XX:+EnableJVMCI -XX:+UseJVMCICompiler"

BENCHMARKS=(
    "als"
    "chi-square"
    "dec-tree"
    "gauss-mix"
    "log-regression"
    "movie-lens"
    "naive-bayes"
    "page-rank"
    "akka-uct"
    "fj-kmeans"
    "reactors"
    "db-shootout"
    "neo4j-analytics"
    "future-genetic"
    "mnemonics"
    "par-mnemonics"
    "rx-scrabble"
    "scrabble"
    "dotty"
    "philosophers"
    "scala-doku"
    "scala-kmeans"
    "scala-stm-bench7"
    "finagle-chirper"
    "finagle-http"
    "dummy-empty"
    "dummy-failing"
    "dummy-param"
    "dummy-setup-failing"
    "dummy-teardown-failing"
    "dummy-validation-failing"
)

# for
for benchmark in "${BENCHMARKS[@]}"; do
    echo "Running benchmark: $benchmark"
    echo "Running $benchmark..." >> "$TIMING_LOG"
    
    start_time=$(date +%s.%N)
    
    mx vm $JVM_OPTS -jar "$BENCHMARK_DIR" "$benchmark"
    
    end_time=$(date +%s.%N)
    duration=$(echo "$end_time - $start_time" | bc -l)
    
    printf "Time taken: %.9f seconds\n" $duration >> "$TIMING_LOG"
    echo "----------------------------------------" >> "$TIMING_LOG"
    
    if [ -f "data.csv" ]; then
        mv data.csv "$DATA_DIR/${benchmark}_data.csv"
        echo "Created $DATA_DIR/${benchmark}_data.csv"
    else
        echo "Warning: data.csv not found for $benchmark"
        echo "Warning: data.csv not generated" >> "$TIMING_LOG"
    fi
    
    echo "----------------------------------------"
done

echo "All benchmarks completed!"
echo "Timing results saved in $TIMING_LOG"
