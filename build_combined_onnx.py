import os
import h5py
import numpy as np
import onnx
from onnx import helper, TensorProto

def build_combined_onnx():
    official_onnx_path = 'scratch/mobilenetv2_official.onnx'
    weights_path = 'backend/model.weights.h5'
    output_onnx_path = 'backend/crop_disease_model.onnx'
    
    print("Loading official MobileNetV2 ONNX model...")
    model = onnx.load(official_onnx_path)
    graph = model.graph
    
    print("Loading custom trained weights from model.weights.h5...")
    with h5py.File(weights_path, 'r') as f:
        w1 = f['layers/dense/vars/0'][:]       # (1280, 128)
        b1 = f['layers/dense/vars/1'][:]       # (128,)
        w2 = f['layers/dense_1/vars/0'][:]     # (128, 6)
        b2 = f['layers/dense_1/vars/1'][:]     # (6,)
        
    print("Creating ONNX weight initializers...")
    init_w1 = helper.make_tensor('w1', TensorProto.FLOAT, w1.shape, w1.astype(np.float32).flatten().tolist())
    init_b1 = helper.make_tensor('b1', TensorProto.FLOAT, b1.shape, b1.astype(np.float32).flatten().tolist())
    init_w2 = helper.make_tensor('w2', TensorProto.FLOAT, w2.shape, w2.astype(np.float32).flatten().tolist())
    init_b2 = helper.make_tensor('b2', TensorProto.FLOAT, b2.shape, b2.astype(np.float32).flatten().tolist())

    graph.initializer.extend([init_w1, init_b1, init_w2, init_b2])

    print("Appending classification head nodes (MatMul -> Add -> Relu -> MatMul -> Add -> Softmax)...")
    node_matmul1 = helper.make_node('MatMul', inputs=['472', 'w1'], outputs=['dense1_matmul'])
    node_add1 = helper.make_node('Add', inputs=['dense1_matmul', 'b1'], outputs=['dense1_add'])
    node_relu1 = helper.make_node('Relu', inputs=['dense1_add'], outputs=['dense1_relu'])

    node_matmul2 = helper.make_node('MatMul', inputs=['dense1_relu', 'w2'], outputs=['dense2_matmul'])
    node_add2 = helper.make_node('Add', inputs=['dense2_matmul', 'b2'], outputs=['dense2_add'])
    node_softmax = helper.make_node('Softmax', inputs=['dense2_add'], outputs=['output_final'], axis=1)

    graph.node.extend([node_matmul1, node_add1, node_relu1, node_matmul2, node_add2, node_softmax])

    # Replace graph output with 'output_final'
    del graph.output[:]
    output_tensor = helper.make_tensor_value_info('output_final', TensorProto.FLOAT, [None, 6])
    graph.output.append(output_tensor)

    onnx.save_model(model, output_onnx_path, save_as_external_data=False)
    print(f"Successfully generated complete single-file ONNX model at {output_onnx_path} (size: {os.path.getsize(output_onnx_path)/(1024*1024):.2f} MB)")

if __name__ == '__main__':
    build_combined_onnx()
