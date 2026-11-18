/* Neural sandbox worker. SharedArrayBuffer communication; TensorFlow.js/WebGPU compute. */
importScripts("https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.22.0/dist/tf.min.js","https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-backend-webgpu@4.22.0/dist/tf-backend-webgpu.min.js");
let backend="cpu";
self.onmessage=async({data})=>{
  try{
    if(data.type==="INIT"){
      if(self.tf&&tf.findBackend("webgpu")){
        try{await tf.setBackend("webgpu");await tf.ready();backend=tf.getBackend();}
        catch(_){await tf.setBackend("cpu");await tf.ready();backend=tf.getBackend();}
      }else{await tf.ready();backend=tf.getBackend();}
      self.postMessage({type:"READY",message:"TensorFlow.js ready; backend = "+backend});return;
    }
    if(data.type==="INFER"){
      if(!(data.input instanceof SharedArrayBuffer)||!(data.output instanceof SharedArrayBuffer))throw new Error("INFER requires SharedArrayBuffer input/output.");
      const input=new Float32Array(data.input,0,data.length),output=new Float32Array(data.output,0,4);
      const x=tf.tensor1d(input),mean=tf.mean(x),max=tf.max(x),min=tf.min(x),sum=tf.sum(x);
      const values=await tf.stack([mean,max,min,sum]).data();output.set(values);
      x.dispose();mean.dispose();max.dispose();min.dispose();sum.dispose();
      self.postMessage({type:"RESULT",payload:{backend,sharedArrayBuffer:true,inputLength:data.length,output:Array.from(output)}});
    }
  }catch(err){self.postMessage({type:"ERROR",message:String(err&&err.message||err),stack:String(err&&err.stack||"")});}
};