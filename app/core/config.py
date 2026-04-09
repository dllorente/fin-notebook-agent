# Importamos las librerías necesarias
from app.index.document_loader import settings
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache
from pydantic import Field, AliasChoices  


# Definimos la clase Settings que hereda de BaseSettings
class Settings(BaseSettings):
    # Configuración del modelo: Lee el archivo .env y codifica el archivo en utf-8
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore", #Evita errores si el .env tiene variables extra no declaradas
    )
    # Agnóstico de proveedor
    llm_provider: str = Field(default="openai", validation_alias=AliasChoices("LLM_PROVIDER"))
    llm_model: str = Field(default="gpt-4o-mini", validation_alias=AliasChoices("LLM_MODEL", "MODEL_NAME"))
    llm_api_key: str = Field(
        ...,
        validation_alias=AliasChoices("LLM_API_KEY", "OPENAI_API_KEY")
    )
    embedding_model: str = Field(default="text-embedding-3-small", validation_alias=AliasChoices("EMBEDDING_MODEL"))
    embedding_provider: str = Field(
    default="openai",
    validation_alias=AliasChoices("EMBEDDING_PROVIDER")
)
    data_dir: str = Field(default="data", validation_alias=AliasChoices("DATA_DIR"))
    vectorstore_dir: str = Field(default=".vectorstore", validation_alias=AliasChoices("VECTORSTORE_DIR"))
    chunk_size: int = 1000
    chunk_overlap: int = 200


@lru_cache(maxsize=1) # Cacheamos la función para que no se vuelva a ejecutar cada vez que se llama
def get_settings() -> Settings:
    return Settings() # Devuelve una instancia de Settings
    
def get_llm() -> BaseChatModel:
# Lee get_settings().llm_provider
# Si es "openai" → devuelve ChatOpenAI(...) # Si es "anthropic" → devuelve ChatAnthropic(...)
# Si no reconoce el proveedor → lanza ValueError con mensaje claro
    settings=get_settings()
    provider= settings.llm_provider.lower()
    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=settings.llm_model,
            api_key=settings.llm_api_key
        )

    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model= settings.llm_model,
            api_key= settings.llm_api_key)
    else :
        raise ValueError(
            f"Proveedor LLM no soportado: '{provider}'. "
            f"Valores válidos: 'openai', 'anthropic'")


def get_embeddings() -> Embeddings:
# Lee get_settings().embedding_provider
# Si es "openai" → devuelve OpenAIEmbeddings(...)
# Si es "huggingface" → devuelve HuggingFaceEmbeddings(...)
# Si no reconoce → lanza ValueError
    settings = get_settings()
    embedding_provider=settings.embedding_provider

    if embedding_provider=="openai":
    # Devuelve OpenAIEmbeddings con model y api_key
        from langchain_openai import OpenAIEmbeddings 
        return OpenAIEmbeddings(
            model= settings.embedding_model,
            api_key= settings.llm_api_key
        )
    elif embedding_provider=="huggingface":
    # Devuelve HuggingFaceEmbeddings con model_name
    # Ojo: HuggingFace no necesita api_key para modelos locales
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(
            model_name= settings.embedding_model
        )
    else:
        raise  ValueError(
            f"Proveedor de embeddings no soportado: '{embedding_provider}'. "
            f"Valores válidos: 'openai', 'huggingface'"
        )