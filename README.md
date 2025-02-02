# Machine Learning-Driven Method Inlining Optimization for GraalVM
This project implements machine learning-based optimization for method inlining in GraalVM, aiming to improve compilation performance.

## Prerequisites
* Docker

## Setup and Usage
### 1. Docker Environment Setup
```bash
# Pull the required Docker image
docker pull etcartman/graalml:v1

# Create and enter container
docker run -it -d --name graalvm etcartman/graalml:v1
docker exec -it graalvm bash
```
### 2. Runtime Data Collection
```bash
# Navigate to compiler directory
cd /root/Projects/graal_data_collection/compiler/

# Set Java environment
export JAVA_HOME=/root/.mx/jdks/labsjdk-ce-21-jvmci-23.1-b33

# Clear previous data if exists
rm /root/Projects/data.csv

# Collect JIT runtime data(one round)
mx vm -XX:+UnlockExperimentalVMOptions -XX:+EnableJVMCI \
    -XX:+UseJVMCICompiler \
    -jar /root/Projects/benchmarks/single/akka-uct.jar all -r 1
```
### 3. Machine Learning Predictions
```bash
# Activate Python virtual environment
source /root/Projects/graal_scripts/.venv/bin/activate

# Generate ML predictions
python /root/Projects/graal_scripts/ml_code/predict.py
```

### 4. Configuration Generation
```bash
# Navigate to project root
cd /root/Projects/

# Clear Java environment variable
unset JAVA_HOME

# Generate configuration files
java -agentlib:native-image-agent=config-output-dir=./config \
    -jar /root/Projects/benchmarks/single/akka-uct.jar all
```
### 5. Native Image Build

```bash
# Navigate to SubstrateVM directory
cd /root/Projects/graal_data_collection/substratevm

# Set Java environment
export JAVA_HOME=/root/.mx/jdks/labsjdk-ce-21-jvmci-23.1-b33

# Build native image with ML optimizations
mx native-image \
    -march=native \
    --no-server \
    --initialize-at-build-time \
    --report-unsupported-elements-at-runtime \
    --allow-incomplete-classpath \
    -H:Name=/root/Projects/akka-uct-ml \
    -H:+ReportExceptionStackTraces \
    -H:ConfigurationFileDirectories=/root/Projects/config \
    -jar /root/Projects/benchmarks/single/akka-uct.jar
```

### 6. Execution
```bash
cd /root/Projects/
time ./akka-uct-ml all
```
