pip install optimum[exporters] onnxruntime

optimum-cli export onnx --model neuralmind/bert-base-portuguese-cased --task feature-extraction ./app/resources/models/bertimbau_onnx/

pip uninstall onnxruntime
pip install onnxruntime