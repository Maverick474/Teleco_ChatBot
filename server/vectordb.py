from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
import os
from dotenv import load_dotenv

load_dotenv()

class VectorDBManager:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
        self.vectorstore = None  # Don't initialize yet
        self._initialize_on_demand = True  # Flag to lazy load
    
    def _preprocess_documents(self):
        """Load documents from PDF files"""
        print("Loading documents from ./teleco_db...")
        
        loader = DirectoryLoader(
            "./teleco_db",
            glob="**/*.pdf",
            loader_cls=PyPDFLoader,
            use_multithreading=True
        )
        raw_docs = loader.load()
        
        if not raw_docs:
            print("No documents found in ./teleco_db - returning empty list")
            return []  # Return empty list instead of raising error
        
        print(f"Loaded {len(raw_docs)} documents")
        
        # Category assignment (use directory path first)
        for doc in raw_docs:
            source_path = doc.metadata["source"].lower()
            
            if "billing" in source_path:
                doc.metadata["category"] = "billing"
            elif "packages" in source_path:
                doc.metadata["category"] = "packages"
            elif "troubleshooting" in source_path or "support" in source_path:
                doc.metadata["category"] = "troubleshooting"
            elif "policies" in source_path or "sla" in source_path:
                doc.metadata["category"] = "policies"
            else:
                # Fallback to content analysis
                text = doc.page_content.lower()
                if any(kw in text for kw in ["bill", "payment", "$", "20", "45", "overage", "gb", "mb", "fee", "late"]):
                    doc.metadata["category"] = "billing"
                elif any(kw in text for kw in ["plan", "package", "upgrade", "1234", "premium", "basic", "sim", "roaming"]):
                    doc.metadata["category"] = "packages"
                elif any(kw in text for kw in ["router", "outage", "troubleshoot", "5678", "reboot", "light", "fiber", "ethernet"]):
                    doc.metadata["category"] = "troubleshooting"
                else:
                    doc.metadata["category"] = "policies"
        
        # Continue with splitting...
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        splits = text_splitter.split_documents(raw_docs)
        
        # Add chunk metadata
        for i, split in enumerate(splits):
            source = split.metadata["source"]
            filename = source.split('/')[-1].split('.')[0]
            split.metadata["chunk_id"] = f"{filename}_chunk{i}"
            split.metadata["language"] = "en"
            split.metadata["title"] = filename
        
        print(f"Created {len(splits)} searchable chunks")
        return splits

    def _init_vectorstore(self):
        """Initialize or load persistent ChromaDB vectorstore"""
        
        # Create knowledge base directory if missing
        os.makedirs("./teleco_db", exist_ok=True) # stores documents only
        os.makedirs("./data", exist_ok=True) # stores vector databases
        
        # Check if vectorstore exists
        if os.path.exists("./data") and os.listdir("./data"):
            print("Loading existing ChromaDB vectorstore")
            vectorstore = Chroma(
                persist_directory="./data",
                embedding_function=self.embeddings,
                collection_name="teleco_knowledge"
            )
        else:
            print("No existing vectorstore found, checking for documents...")
            documents = self._preprocess_documents()
            
            if documents:  # Only create if we have documents
                print("Creating new ChromaDB vectorstore from documents")
                vectorstore = Chroma.from_documents(
                    documents=documents,
                    embedding=self.embeddings,
                    persist_directory="./data",
                    collection_name="teleco_knowledge",
                    collection_metadata={"hnsw:space": "cosine"}
                )
                print(f"Added {len(documents)} document chunks to ChromaDB")
            else:
                # Create empty vectorstore
                print("Creating empty ChromaDB vectorstore")
                vectorstore = Chroma(
                    persist_directory="./data",
                    embedding_function=self.embeddings,
                    collection_name="teleco_knowledge"
                )
        
        self._initialize_on_demand = False
        return vectorstore

    def get_vectorstore(self):
        """Lazy load the vectorstore when needed"""
        if self.vectorstore is None:
            self.vectorstore = self._init_vectorstore()
        return self.vectorstore

    def add_document(self, file_path: str):
        """Add a new document to the vectorstore"""
        # Ensure vectorstore is initialized
        if self.vectorstore is None:
            self.vectorstore = self._init_vectorstore()
        
        # Load the new document
        loader = PyPDFLoader(file_path)
        raw_docs = loader.load()
        
        # Apply same preprocessing
        for doc in raw_docs:
            source_path = doc.metadata["source"].lower()
            
            if "billing" in source_path:
                doc.metadata["category"] = "billing"
            elif "packages" in source_path:
                doc.metadata["category"] = "packages"
            elif "troubleshooting" in source_path or "support" in source_path:
                doc.metadata["category"] = "troubleshooting"
            elif "policies" in source_path or "sla" in source_path:
                doc.metadata["category"] = "policies"
            else:
                # Fallback to content analysis
                text = doc.page_content.lower()
                if any(kw in text for kw in ["bill", "payment", "$", "20", "45", "overage", "gb", "mb", "fee", "late"]):
                    doc.metadata["category"] = "billing"
                elif any(kw in text for kw in ["plan", "package", "upgrade", "1234", "premium", "basic", "sim", "roaming"]):
                    doc.metadata["category"] = "packages"
                elif any(kw in text for kw in ["router", "outage", "troubleshoot", "5678", "reboot", "light", "fiber", "ethernet"]):
                    doc.metadata["category"] = "troubleshooting"
                else:
                    doc.metadata["category"] = "policies"
        
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        splits = text_splitter.split_documents(raw_docs)
        
        # Add chunk metadata
        for i, split in enumerate(splits):
            source = split.metadata["source"]
            filename = os.path.basename(source).split('.')[0]
            split.metadata["chunk_id"] = f"{filename}_chunk{i}"
            split.metadata["language"] = "en"
            split.metadata["title"] = filename
        
        # Add to vectorstore
        self.vectorstore.add_documents(splits)
        print(f"Added {len(splits)} chunks from {file_path} to vectorstore")
        
        return True

    def similarity_search(self, query: str, k: int = 3, filter: dict = None):
        """Perform similarity search in the vectorstore"""
        # Ensure vectorstore is initialized
        if self.vectorstore is None:
            self.vectorstore = self._init_vectorstore()
        
        return self.vectorstore.similarity_search(query, k=k, filter=filter)