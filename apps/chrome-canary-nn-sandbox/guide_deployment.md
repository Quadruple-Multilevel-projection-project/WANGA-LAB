# Deployment Guide — Chrome Canary Neural Sandbox

## Architecture
Main thread -> Web Worker -> TensorFlow.js/WebGPU
Main thread <-> SharedArrayBuffer <-> Web Worker

Required isolation:
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp

## Local
python -m http.server 8080

## Extension
Load the directory through chrome://extensions with Developer mode enabled.

## Validation
crossOriginIsolated === true
typeof SharedArrayBuffer !== "undefined"

Then execute the worker inference test and record the selected backend.

## Evidence status
The code establishes an experimental execution path. It does not establish a benchmark, training result, GPU throughput figure, or production security certification.
