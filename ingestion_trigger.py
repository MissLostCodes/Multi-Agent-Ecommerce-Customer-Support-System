from app.rag.ingestion import IngestionPipeline

if __name__ == "__main__":
    pipeline = IngestionPipeline()
    pipeline.run()