"""HTTP launcher for Railway. Builds config.json from env vars and serves the MCP server over streamable HTTP."""
import json
import os

import uvicorn
from mcp.server.transport_security import TransportSecuritySettings

league = os.environ["LEAGUE_ID"]
with open("config.json", "w") as f:
    json.dump(
        {
            "username": os.environ["SLEEPER_USERNAME"],
            "default_league_id": league,
            "leagues": [{"name": "main", "league_id": league}],
        },
        f,
    )

import server  # noqa: E402

host = os.environ["PUBLIC_HOST"]
app = server.mcp.streamable_http_app(
    streamable_http_path="/mcp/" + os.environ["MCP_PATH_TOKEN"],
    stateless_http=True,
    json_response=True,
    transport_security=TransportSecuritySettings(
        allowed_hosts=[host, host + ":*"],
        allowed_origins=["https://claude.ai", "https://" + host],
    ),
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
