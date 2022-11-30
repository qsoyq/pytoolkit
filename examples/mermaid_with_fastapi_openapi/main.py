import uvicorn

from fastapi import FastAPI

from pytoolkit.patch.mermaid import patch_fastapi

app = FastAPI()


@app.get("/")
def index():
    """
    <pre class="mermaid">
            graph TD
            A[Client] -->|tcp_123| B
            B(Load Balancer)
            B -->|tcp_456| C[Server1]
            B -->|tcp_456| D[Server2]
    </pre>
    """
    return "success"


if __name__ == '__main__':
    patch_fastapi()
    uvicorn.run("main:app")
