
from app import app, tasks
import pytest


@pytest.fixture(autouse=True)
def reset_tasks():
    tasks.clear()
    yield
    tasks.clear()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Student Task Manager" in response.data


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_add_task(client):
    response = client.post(
        "/add",
        data={"title": "Complete assignment"}
    )
    assert response.status_code == 302
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Complete assignment"
    assert tasks[0]["completed"] is False


def test_complete_task(client):
    client.post("/add", data={"title": "Study for exam"})
    task_id = tasks[0]["id"]

    response = client.get(f"/complete/{task_id}")

    assert response.status_code == 302
    assert tasks[0]["completed"] is True


def test_delete_task(client):
    client.post("/add", data={"title": "Submit lab record"})
    task_id = tasks[0]["id"]

    response = client.get(f"/delete/{task_id}")

    assert response.status_code == 302
    assert len(tasks) == 0


def test_api_tasks(client):
    client.post("/add", data={"title": "Revise Kubernetes"})

    response = client.get("/api/tasks")

    assert response.status_code == 200
    assert response.json[0]["title"] == "Revise Kubernetes"
