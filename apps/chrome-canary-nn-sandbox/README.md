# Chrome Canary Neural Sandbox

Status: PROTOTYPED / EXPERIMENTAL

## Scope
The app isolates neural computation in a Web Worker and uses SharedArrayBuffer for shared memory between the main thread and worker. TensorFlow.js is loaded in the worker and attempts WebGPU first, with fallback to the available TensorFlow.js backend.

## Files
- index.html — browser sandbox and runtime test UI.
- manifest.json — Chrome MV3 sandbox configuration.
- nn_sandbox_engine.js — worker-side TensorFlow.js/WebGPU engine.
- sw.js — service-worker response wrapper used by static hosting to establish cross-origin isolation where the browser permits it.
- guide_deployment.md — deployment and validation notes.

## Local run
Run from this directory:
python -m http.server 8080
Open http://localhost:8080/
Do not use file://.

## Chrome Canary extension
Open chrome://extensions, enable Developer mode, choose Load unpacked, and select this directory.

## Verification
Confirm crossOriginIsolated === true and SharedArrayBuffer is defined. Then run the worker inference test and record the selected backend. Use DevTools Performance and WebGPU inspection tools for measurements.

## Deployment boundary
GitHub Pages can publish the static files, but the deployed application must be tested for crossOriginIsolated === true. If the hosting response path does not establish the required isolation headers, the SharedArrayBuffer path remains unavailable and a header-capable host is required.

This repository entry does not claim GPU performance, training results, or production security certification that have not been measured.
