from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.onnx import export
import onnx

model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

dummy_input = tokenizer("Sample text", return_tensors="pt")

export(
    model,
    (dummy_input["input_ids"], dummy_input["attention_mask"]),
    "sentiment_model.onnx",
    input_names=["input_ids", "attention_mask"],
    output_names=["logits"],
    dynamic_axes={
        "input_ids": {0: "batch_size"},
        "attention_mask": {0: "batch_size"}
    },
    opset_version=14  
)

onnx_model = onnx.load("sentiment_model.onnx")

onnx.checker.check_model(onnx_model)

print("ONNX model is valid.")