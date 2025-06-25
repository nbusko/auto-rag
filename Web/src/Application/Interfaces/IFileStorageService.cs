using AutoRag.Application.DTOs;

namespace AutoRag.Application.Interfaces;

public interface IFileStorageService
{
    Task<DocumentInfoDto> UploadAsync(string fileName, Stream content, CancellationToken ct = default);
    Task<IReadOnlyList<DocumentInfoDto>> ListAsync(CancellationToken ct = default);

    Task<Stream> DownloadAsync(Guid documentId, CancellationToken ct = default);
}
