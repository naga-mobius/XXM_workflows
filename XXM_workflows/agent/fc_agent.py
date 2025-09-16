import os
import json
from typing import Any, Dict, List
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from ..tools.tool_registry import registry


class FCAgent:
    def __init__(self, base_model: str, adapter_path: str | None = None, device_map: str | None = None):
        self.tok = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(base_model, trust_remote_code=True)
        if adapter_path:
            self.model = PeftModel.from_pretrained(self.model, adapter_path)
        if device_map:
            self.model.to(device_map)


    def tools(self) -> List[Dict[str, Any]]:
        return registry.all_specs()


    def chat_once(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Very small loop: ask model for a tool call JSON, run it, return tool result."""
        system = (
            "You are a precise assistant. If a tool matches the user goal, "
            "respond ONLY with a single JSON object: {\"tool\": <name>, \"arguments\": {...}}. "
            "Do not explain. Use the provided tool schema strictly."
        )
        payload = [
            {"role": "system", "content": system},
            {"role": "system", "content": json.dumps({"tools": self.tools()})},
        ] + messages


        prompt = "\n\n".join(f"{m['role'].upper()}: {m['content']}" for m in payload)
        inputs = self.tok(prompt, return_tensors="pt")
        out = self.model.generate(**inputs, max_new_tokens=256)
        text = self.tok.decode(out[0], skip_special_tokens=True)
        json_str = text.split("{" ,1)[1].rsplit("}",1)[0]
        call = json.loads("{"+json_str+"}")


        tool = registry.get(call["tool"])
        result = tool.handler(call.get("arguments", {}))
        return {"tool": tool.name, "result": result}