#!/bin/bash
uvicorn rag_server:app --host 0.0.0.0 --port 5151 --reload
