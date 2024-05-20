from fastapi import FastAPI #, Path, Query
from pydantic import BaseModel
from contextlib import asynccontextmanager
from transformers import AutoModel, AutoTokenizer


from api import texts, stats
from db.db_setup import engine
from db.models import text, comparison, request_count


@asynccontextmanager
async def lifespan(app:FastAPI):
    # Check if CUDA (GPU support) is available, and set the device accordingly
    #device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    # Load the UAE-Large-V1 model from the Hugging Face 
    model = AutoModel.from_pretrained('WhereIsAI/UAE-Large-V1')#.to(device)
    app.state.MODEL = model
    print("UAE-Large-V1 loaded")
    # Load the tokenizer associated with the UAE-Large-V1 model
    tokenizer = AutoTokenizer.from_pretrained('WhereIsAI/UAE-Large-V1')
    app.state.TOKENIZER = tokenizer
    print("tokenizer loaded")
    yield
    model.close()
    tokenizer.close()

text.Base.metadata.create_all(bind=engine)
comparison.Base.metadata.create_all(bind=engine)
request_count.Base.metadata.create_all(bind=engine)


app = FastAPI(
    lifespan=lifespan,
    title="TEXT-COMPARE",
    description="compare two texts",
    version="0.0.1",
    terms_or_service="http://",
    contact={
        "name":"Sujin",
        "email":"sujin@email.com",
    },
    license_info={
        "name":"Prosperix"
    },
)

app.include_router(texts.router)
app.include_router(stats.router)

