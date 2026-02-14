import os
import time
import json
import logging
import requests
from typing import Any, Dict, Optional
from ..tools.http_client import HttpClient
from ..tools.tool_registry import registry


log = logging.getLogger(__name__)


class HttpClient:
    def __init__(self, base_url: str | None = None, token: str | None = None, timeout_s: float = 30):
        self.base_url = (base_url or os.getenv("PI_ENTITY_BASE_URL", "")).rstrip("/")
        self.token = token or os.getenv("PI_ENTITY_BEARER_TOKEN", "")
        self.timeout = timeout_s


    def _headers(self) -> Dict[str, str]:
        h = {"Content-Type": "application/json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h


    def request(self, method: str, path: str, *, params: Optional[Dict[str, Any]] = None,
                json_body: Optional[Dict[str, Any]] = None, retries: int = 2) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        last_err = None
        for attempt in range(retries + 1):
            try:
                resp = requests.request(method, url, params=params, json=json_body, headers=self._headers(), timeout=self.timeout)
                if resp.status_code >= 400:
                    log.warning("HTTP %s %s → %s: %s", method, url, resp.status_code, resp.text[:400])
                    resp.raise_for_status()
                return resp.json() if resp.text else {}
            except Exception as e:
                last_err = e
                time.sleep(0.3 * (attempt + 1))
                raise RuntimeError(f"Request failed for {method} {url}: {last_err}")


registry.register(Tool(
    name="create_entity_schema_from_json",
    description="Create an EntitySchema from a JSON payload (name, universes, tags, json fields, primaryDb, piFeatures).",
    parameters={"type": "object", "properties": {"body": {"type": "object"}}, "required": ["body"], "additionalProperties": False},
    handler=lambda args: client.request("POST", "/v1.0/schemas/json-schema", json_body=args["body"])
))


registry.register(Tool(
    name="update_entity_schema",
    description="Full update of an EntitySchema by schemaID (add/update/delete attributes, access flags, piFeatures).",
    parameters={
        "type": "object",
        "properties": {"schemaID": {"type": "string"}, "body": {"type": "object"}},
        "required": ["schemaID", "body"],
        "additionalProperties": False
    },
    handler=lambda args: client.request("PUT", f"/v1.0/schemas/{args['schemaID']}", json_body=args["body"])
))


registry.register(Tool(
    name="partial_update_entity_schema",
    description="Partial metadata update of an EntitySchema.",
    parameters={
        "type": "object",
        "properties": {"schemaId": {"type": "string"}, "body": {"type": "object"}},
        "required": ["schemaId", "body"],
        "additionalProperties": False
    },
    handler=lambda args: client.request("PATCH", f"/v1.0/schemas/{args['schemaId']}", json_body=args["body"])
))


registry.register(Tool(
    name="clone_entity_schema",
    description="Clone an EntitySchema (constructId, assigningTo, optional migrateData).",
    parameters={"type": "object", "properties": {"body": {"type": "object"}}, "required": ["body"], "additionalProperties": False},
    handler=lambda args: client.request("POST", "/v1.0/schemas/clone", json_body=args["body"])
))


registry.register(Tool(
    name="get_pi_features",
    description="List PI features and supported DB types.",
    parameters={"type": "object", "properties": {}},
    handler=lambda args: client.request("GET", "/v1.0/schemas/pi-features")
))


registry.register(Tool(
    name="enable_cdc_bulk",
    description="Enable CDC in bulk for schemas.",
    parameters={"type": "object", "properties": {"body": {"type": "object"}}, "required": ["body"], "additionalProperties": False},
    handler=lambda args: client.request("POST", "/v1.0/schemas/enablecdc", json_body=args["body"])
))


registry.register(Tool(
    name="delete_cdc",
    description="Delete a CDC pipeline by dbType + cdcId.",
    parameters={
        "type": "object",
        "properties": {
            "dbType": {"type": "string"},
            "cdcId": {"type": "string"}
        },
        "required": ["dbType", "cdcId"],
        "additionalProperties": False
    },
    handler=lambda args: client.request("POST", "/v1.0/schemas/deletecdc", params={"dbType": args["dbType"], "cdcId": args["cdcId"]})
))