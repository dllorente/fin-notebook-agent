# Importamos las librerías necesarias
from functools import lru_cache
import importlib
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Definimos la clase Settings que hereda de BaseSettings
class Settings(BaseSettings):
    DATABASE_URL: str = Field(default="sqlite:///./chat_sessions.db")

    # Configuración del modelo: Lee el archivo .env y codifica el archivo en utf-8
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Evita errores si el .env tiene variables extra no declaradas
    )
    # Agnóstico de proveedor
    llm_provider: str = Field(default="openai", validation_alias=AliasChoices("LLM_PROVIDER"))
    llm_model: str = Field(default="gpt-4o-mini", validation_alias=AliasChoices("LLM_MODEL", "MODEL_NAME"))
    #llm_api_key: str = Field(..., validation_alias=AliasChoices("LLM_API_KEY", "OPENAI_API_KEY"))
    openai_api_key: str = Field(default="", validation_alias=AliasChoices("OPENAI_API_KEY"))
    anthropic_api_key: str = Field(default="", validation_alias=AliasChoices("ANTHROPIC_API_KEY"))
    groq_api_key: str = Field(default="", validation_alias=AliasChoices("GROQ_API_KEY"))

    embedding_model: str = Field(
        default="text-embedding-3-small",
        validation_alias=AliasChoices("EMBEDDING_MODEL"),
    )
    embedding_provider: str = Field(default="openai", validation_alias=AliasChoices("EMBEDDING_PROVIDER"))
    data_dir: str = Field(default="data", validation_alias=AliasChoices("DATA_DIR"))
    vectorstore_dir: str = Field(default=".vectorstore", validation_alias=AliasChoices("VECTORSTORE_DIR"))
    chunk_size: int = Field(validation_alias=AliasChoices("CHUNK_SIZE"))
    chunk_overlap: int = Field(validation_alias=AliasChoices("CHUNK_OVERLAP"))
    langchain_tracing_v2: bool = Field(default = False, validation_alias=AliasChoices("LANGCHAIN_TRACING_V2"))
    langchain_endpoint: str = Field(default="", validation_alias=AliasChoices("LANGCHAIN_ENDPOINT"))
    langchain_api_key: str = Field(default="", validation_alias=AliasChoices("LANGCHAIN_API_KEY"))
    langchain_project: str = Field(default="fin-notebook-agent", validation_alias=AliasChoices("LANGCHAIN_PROJECT"))
    
# Mapa de proveedor → (módulo, clase, campo de api_key)
LLM_REGISTRY = {
    "openai": ("langchain_openai", "ChatOpenAI", "openai_api_key"),
    "anthropic": ("langchain_anthropic", "ChatAnthropic", "anthropic_api_key"),
    "groq": ("langchain_groq", "ChatGroq", "groq_api_key"),
    "mistral": ("langchain_mistralai", "ChatMistralAI", "mistral_api_key"),
}
EMBEDDINGS_REGISTRY = {
    "openai": ("langchain_openai", "OpenAIEmbeddings", "openai_api_key"),
    "huggingface": ("langchain_huggingface", "HuggingFaceEmbeddings", None),
    "cohere": ("langchain_cohere", "CohereEmbeddings", "cohere_api_key"),
}

@lru_cache(maxsize=1)  # Cacheamos la función para que no se vuelva a ejecutar cada vez que se llama
def get_settings() -> Settings:
    return Settings()  # Devuelve una instancia de Settings

@lru_cache(maxsize=1)
def get_llm() -> BaseChatModel:
    settings = get_settings()
    provider = settings.llm_provider.lower()
    if provider not in LLM_REGISTRY:
        raise ValueError(
            f"Proveedor LLM no soportado: '{provider}'. "
            f"Valores válidos: {list(LLM_REGISTRY.keys())}"
        )
    module_name, class_name, api_key_field = LLM_REGISTRY[provider]
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    api_key = getattr(settings, api_key_field, "")
    print(f"\n💾 Modelo seleccionado en {module_name}")

    return cls(model=settings.llm_model, api_key=api_key)

@lru_cache(maxsize=1)
def get_embeddings() -> Embeddings:
    settings = get_settings()
    provider = settings.embedding_provider

    if provider not in EMBEDDINGS_REGISTRY:
        raise ValueError(
            f"Proveedor de embeddings no soportado: '{provider}'. "
            f"Valores válidos: {list(EMBEDDINGS_REGISTRY.keys())}"
        )

    module_name, class_name, api_key_field = EMBEDDINGS_REGISTRY[provider]
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)

    kwargs = {"model": settings.embedding_model} if provider != "huggingface" else {"model_name": settings.embedding_model}
    if api_key_field:
        kwargs["api_key"] = getattr(settings, api_key_field, "")
    print(f"\n💾 Embedding seleccionado en {module_name}")

    return cls(**kwargs)
