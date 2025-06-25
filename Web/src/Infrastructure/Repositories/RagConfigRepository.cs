using AutoRag.Domain.Entities;
using AutoRag.Domain.Interfaces.Repositories;
using AutoRag.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;

namespace AutoRag.Infrastructure.Repositories;

public sealed class RagConfigRepository : IRagConfigRepository
{
    private readonly AutoRagContext _ctx;
    public RagConfigRepository(AutoRagContext ctx)=>_ctx=ctx;

    public async Task<RagConfig?> GetAsync(Guid ragId, CancellationToken ct = default)
        => await _ctx.RagConfigs.AsNoTracking()
               .FirstOrDefaultAsync(x => x.Id == ragId, ct);

    public async Task UpsertAsync(Guid ragId, RagConfig cfg, CancellationToken ct = default)
    {
        var existing = await _ctx.RagConfigs.FirstOrDefaultAsync(x=>x.Id==ragId, ct);

        if (existing is null)
        {
            cfg.Id = ragId;
            await _ctx.RagConfigs.AddAsync(cfg, ct);
        }
        else
        {
            /* копируем ВСЕ актуальные поля */
            existing.Prompt             = cfg.Prompt;
            existing.DocumentId         = cfg.DocumentId;
            existing.TopK               = cfg.TopK;
            existing.Temperature        = cfg.Temperature;
            existing.Threshold          = cfg.Threshold;

            existing.LlmModel           = cfg.LlmModel;
            existing.RetrievePrompt     = cfg.RetrievePrompt;
            existing.AugmentationPrompt = cfg.AugmentationPrompt;

            existing.SplitMethod        = cfg.SplitMethod;
            existing.BatchSize          = cfg.BatchSize;
            existing.SplitPrompt        = cfg.SplitPrompt;
            existing.TablePrompt        = cfg.TablePrompt;

            _ctx.RagConfigs.Update(existing);
        }
        await _ctx.SaveChangesAsync(ct);
    }
}