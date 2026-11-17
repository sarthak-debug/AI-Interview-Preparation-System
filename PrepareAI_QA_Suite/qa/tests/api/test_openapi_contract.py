"""Contract tests: the Swagger/OpenAPI spec FastAPI publishes must match what the frontend uses."""


def test_swagger_docs_page_is_served(client):
    assert client.get("/docs").status_code == 200


def test_openapi_spec_lists_both_endpoints(client):
    spec = client.get("/openapi.json").json()
    assert "post" in spec["paths"]["/upload"]
    assert "post" in spec["paths"]["/evaluate"]


def test_evaluate_request_schema_requires_question_and_answer(client):
    schemas = client.get("/openapi.json").json()["components"]["schemas"]
    assert set(schemas["AnswerRequest"]["required"]) == {"question", "answer"}
