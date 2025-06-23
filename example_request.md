### RAG:
```
    base request
    {
        user_id: 'uuid4',
    }

    get by user_id from tables
    {
        prompt_retrieve: '' // not required
        prompt_augmentation: '' // not required
        prompt_generation: '' // not required
        top_k: int // not required
        temperature: float // not required
        threshold: float // not required
        document_id: uuid // required
        llm: '' // not required
    }

    response
    {
        status: 'success' or 'not found' in case og threshold or empty ans from llm
        user_id: 'uuid'
        answer: ''
    }
```

## Postgres Update

    base request
    {
        user_id: 'uuid4',
        embedder: '' // not required (пока что просто заглушка но в теории можно разные)

    }

