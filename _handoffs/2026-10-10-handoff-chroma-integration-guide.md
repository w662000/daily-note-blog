---
layout: default
title: 交接文档 · Chroma Integration Guide
date: 2026-10-13 23:30:00 +0800
---

# Chroma Integration Guide

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\src-0215\optional-skills\mlops\chroma\references\integration.md

Integration with LangChain, LlamaIndex, and frameworks.

## LangChain

```python
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(),
    persist_directory="./chroma_db"
)

# Query
results = vectorstore.similarity_search("query", k=3)

# As retriever
retriever = vectorstore.as_retriever()
```

## LlamaIndex

```python
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

db = chromadb.PersistentClient(path="./chroma_db")
collection = db.get_or_create_collection("docs")

vector_store = ChromaVectorStore(chroma_collection=collection)
```

## Resources

- **Docs**: https://docs.trychroma.com
