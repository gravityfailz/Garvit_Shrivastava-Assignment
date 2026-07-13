
from app.database import Base, engine
from app import models  # noqa: F401 — registers all models on Base.metadata


def init_db():
    Base.metadata.create_all(bind=engine)
    print("All tables created (or already existed).")


if __name__ == "__main__":
    init_db()