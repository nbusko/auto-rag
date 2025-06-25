using AutoMapper;
using AutoRag.Application.DTOs;
using AutoRag.Application.Interfaces;
using AutoRag.Domain.Entities;
using AutoRag.Domain.Interfaces.Repositories;

namespace AutoRag.Application.Services;

public sealed class RagConfigService : IRagConfigService
{
    private readonly IRagConfigRepository         _repo;
    private readonly IDocumentEmbeddingRepository _embRepo;
    private readonly IFileStorageService          _storage;
    private readonly IDocumentProcessorService    _processor;
    private readonly IMapper                      _mapper;
    private readonly ICurrentUser                 _current;

    public RagConfigService(IRagConfigRepository      repo,
                            IDocumentEmbeddingRepository embRepo,
                            IFileStorageService          storage,
                            IDocumentProcessorService    processor,
                            IMapper mapper,
                            ICurrentUser current)
        => (_repo,_embRepo,_storage,_processor,_mapper,_current)
         = (repo,embRepo,storage,processor,mapper,current);

    private Guid RagId => _current.RagId ?? throw new InvalidOperationException("Not authenticated");

    public async Task<RagConfigDto?> GetAsync(CancellationToken ct = default)
        => _mapper.Map<RagConfigDto?>(await _repo.GetAsync(RagId, ct));

    public async Task<bool> SaveAsync(RagConfigDto dto, CancellationToken ct = default)
    {
        /* 1. сохраняем конфигурацию RAG */
        var entity = _mapper.Map<RagConfig>(dto);
        await _repo.UpsertAsync(RagId, entity, ct);

        /* 2. если выбран документ – создаём / обновляем его эмбеддинги */
        if (dto.SelectedDocumentId is Guid docId && docId != Guid.Empty)
        {
            /* скачать файл из хранилища */
            await using var stream = await _storage.DownloadAsync(docId, ct);

            /* вызвать document-processor */
            var res = await _processor.ProcessDocumentAsync(docId, stream, ct);
            if (res.Status != "success" || res.Embeddings is null || res.Texts is null)
                throw new InvalidOperationException($"Document processor error: {res.Message}");

            /* сохранить эмбеддинги */
            await _embRepo.ReplaceAsync(docId, res.Texts, res.Embeddings, ct);
        }

        return true;
    }
}