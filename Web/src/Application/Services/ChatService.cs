using AutoRag.Application.DTOs;
using AutoRag.Application.Interfaces;
using AutoRag.Domain.Entities;
using AutoRag.Domain.Interfaces.Repositories;
using Pgvector;

namespace AutoRag.Application.Services;

public sealed class ChatService : IChatService
{
    private readonly IChatHistoryRepository _repo;
    private readonly IRagConfigRepository _cfgRepo;
    private readonly IDocumentEmbeddingRepository  _embRepo;
    private readonly IRagService  _rag;
    private readonly ICurrentUser _current;

    public ChatService(IChatHistoryRepository r,
                       IRagConfigRepository cfg,
                       IDocumentEmbeddingRepository emb,
                       IRagService rag,
                       ICurrentUser cur)
                       => (_repo,_cfgRepo,_embRepo,_rag,_current) = (r,cfg,emb,rag,cur);

    private Guid RagId  => _current.RagId  ?? throw new InvalidOperationException("Not authenticated");
    private Guid UserId => _current.UserId ?? throw new InvalidOperationException("Not authenticated");

    public async Task<ChatResponseDto> SendAsync(ChatRequestDto req, CancellationToken ct = default)
    {
        var userMsg = new ChatMessage
        {
            Id = Guid.NewGuid(),
            RagId = RagId,
            MessageType = "user",
            UserId = UserId,
            Text = req.Message
        };
        await _repo.AddAsync(userMsg, ct);

        var cfg = await _cfgRepo.GetAsync(RagId, ct) ?? throw new InvalidOperationException("RAG not configured");
        var docId = cfg.DocumentId ?? throw new InvalidOperationException("Document not selected");
        var embs = await _embRepo.GetByDocumentIdAsync(docId, ct);

        static IReadOnlyList<float> ToFloatList(Vector v)
            => v.ToArray().Select(f => (float)f).ToList().AsReadOnly();

        var ragReq = new RagRequestDto(
            RagId.ToString(),
            req.Message,
            docId,
            embs.Select(e => (IReadOnlyList<float>)ToFloatList(e.Embedding)).ToList(),
            embs.Select(e => e.Content).ToList(),
            cfg.TopK,
            (float)cfg.Temperature,
            (float)cfg.Threshold)
        {
            LlmModel = cfg.LlmModel,
            PromptGeneration = cfg.Prompt,
            PromptRetrieve = cfg.RetrievePrompt,
            PromptAugmentation = cfg.AugmentationPrompt
        };

        var answer = await _rag.GenerateAnswerAsync(ragReq, ct);

        var assistantMsg = new ChatMessage
        {
            Id = Guid.NewGuid(),
            RagId = RagId,
            MessageType = "assistant",
            UserId = UserId,
            Text = answer
        };
        await _repo.AddAsync(assistantMsg, ct);

        return new ChatResponseDto(answer);
    }

    public async Task<IReadOnlyList<ChatMessageDto>> GetHistoryAsync(CancellationToken ct = default)
    {
        var list = await _repo.GetByRagAndUserAsync(RagId, UserId, ct);
        return list.OrderBy(m => m.Id)
                   .Select(m => new ChatMessageDto(m.MessageType, m.Text, DateTime.UtcNow))
                   .ToList()
                   .AsReadOnly();
    }
}