import uvicorn
from fastapi import FastAPI, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    static_token: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
app = FastAPI()
security = HTTPBearer()


class Data(BaseModel):
    item: str


@app.get("/data", response_model=Data)
async def get_data(
    access_token: HTTPAuthorizationCredentials = Security(security),
) -> Data:
    """
    Get Data
    """
    if access_token.credentials != settings.static_token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return Data(item="helm")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )
