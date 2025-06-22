using AutoRag.Application.DTOs;
using AutoRag.Application.Interfaces;

namespace AutoRag.Infrastructure.ServicesStub;

public sealed class FileStorageServiceStub : IFileStorageService
{
    private readonly List<DocumentInfoDto> _docs = new();

    public async Task<DocumentInfoDto> UploadAsync(string fileName, Stream content, CancellationToken ct = default)
    {
        var doc = new DocumentInfoDto(Guid.NewGuid(), fileName, content.Length)
        {
            UploadedAt = DateTime.UtcNow
        };
        _docs.Add(doc);
        await Task.CompletedTask;
        return doc;
    }

    public Task<IReadOnlyList<DocumentInfoDto>> ListAsync(CancellationToken ct = default)
        => Task.FromResult<IReadOnlyList<DocumentInfoDto>>(_docs);
}
