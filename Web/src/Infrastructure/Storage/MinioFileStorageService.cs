using System.Collections.Concurrent;
using System.Text.Json;
using AutoRag.Application.DTOs;
using AutoRag.Application.Interfaces;
using Microsoft.Extensions.Options;
using Minio;
using Minio.DataModel.Args;
using Minio.Exceptions;

namespace AutoRag.Infrastructure.Storage;

public sealed class MinioFileStorageService : IFileStorageService
{
    private readonly IMinioClient _minio;
    private readonly MinioSettings _settings;
    private readonly ICurrentUser _current;

    private static readonly ConcurrentDictionary<Guid, ConcurrentDictionary<Guid, DocumentInfoDto>> _indices = new();
    private static readonly ConcurrentDictionary<string, byte> _bucketInit = new();

    public MinioFileStorageService(IMinioClient client,
                                   IOptions<MinioSettings> opt,
                                   ICurrentUser current)
    {
        _minio   = client;
        _settings = opt.Value;
        _current  = current;
    }

    /* ------------------------------------------------ upload --------------------------------------------- */
    public async Task<DocumentInfoDto> UploadAsync(string fileName, Stream content, CancellationToken ct = default)
    {
        var ragId = RequireRagId(); 
        await EnsureBucketAsync(ct);

        var id        = Guid.NewGuid();
        var objectKey = $"{ragId}/{id}/{fileName}";

        await _minio.PutObjectAsync(
            new PutObjectArgs()
                .WithBucket(_settings.Bucket)
                .WithObject(objectKey)
                .WithStreamData(content)
                .WithObjectSize(content.Length)
                .WithContentType("application/octet-stream"),
            ct);

        var info = new DocumentInfoDto(id, fileName, content.Length)
        {
            UploadedAt = DateTime.UtcNow
        };

        GetIndex(ragId)[id] = info;
        await SaveIndexAsync(ragId, ct);

        return info;
    }

    /* ------------------------------------------------ list ------------------------------------------------ */
    public async Task<IReadOnlyList<DocumentInfoDto>> ListAsync(CancellationToken ct = default)
    {
        if (_current.RagId is null)
            return Array.Empty<DocumentInfoDto>();

        var ragId = _current.RagId.Value;
        await EnsureBucketAsync(ct);

        if (GetIndex(ragId).IsEmpty)
            await LoadIndexAsync(ragId, ct);

        return GetIndex(ragId).Values
                              .OrderByDescending(d => d.UploadedAt)
                              .ToList()
                              .AsReadOnly();
    }

    public async Task<Stream> DownloadAsync(Guid documentId, CancellationToken ct = default)
    {
        var ragId = RequireRagId();
        await EnsureBucketAsync(ct);

        if (!GetIndex(ragId).TryGetValue(documentId, out var info))
            throw new KeyNotFoundException("Document not found");

        var ms = new MemoryStream();

        await _minio.GetObjectAsync(
            new GetObjectArgs()
                .WithBucket(_settings.Bucket)
                .WithObject($"{ragId}/{documentId}/{info.FileName}")
                .WithCallbackStream(s => s.CopyTo(ms)),
            ct);

        ms.Position = 0;
        return ms;
    }

    /* ------------------------------------------- helpers -------------------------------------------------- */
    private Guid RequireRagId()
        => _current.RagId ?? throw new InvalidOperationException("Unauthenticated");

    private ConcurrentDictionary<Guid, DocumentInfoDto> GetIndex(Guid ragId)
        => _indices.GetOrAdd(ragId, _ => new());

    private async Task EnsureBucketAsync(CancellationToken ct)
    {
        if (_bucketInit.ContainsKey(_settings.Bucket)) return;

        try
        {
            var exists = await _minio.BucketExistsAsync(
                new BucketExistsArgs().WithBucket(_settings.Bucket),
                ct);

            if (!exists)
            {
                await _minio.MakeBucketAsync(
                    new MakeBucketArgs().WithBucket(_settings.Bucket),
                    ct);
            }
        }
        catch (MinioException ex)
        {
            throw new InvalidOperationException("MinIO bucket init failed", ex);
        }

        _bucketInit.TryAdd(_settings.Bucket, 0);
    }

    private string IndexKey(Guid ragId) => $"{ragId}/_index.json";

    private async Task LoadIndexAsync(Guid ragId, CancellationToken ct)
    {
        try
        {
            using var ms = new MemoryStream();

            await _minio.GetObjectAsync(
                new GetObjectArgs()
                    .WithBucket(_settings.Bucket)
                    .WithObject(IndexKey(ragId))
                    .WithCallbackStream(stream => stream.CopyTo(ms)),
                ct);

            ms.Position = 0;
            var list = await JsonSerializer.DeserializeAsync<List<DocumentInfoDto>>(ms, cancellationToken: ct)
                       ?? [];

            foreach (var d in list)
                GetIndex(ragId)[d.Id] = d;
        }
        catch (ObjectNotFoundException)
        { }
    }

    private async Task SaveIndexAsync(Guid ragId, CancellationToken ct)
    {
        await using var ms = new MemoryStream();
        await JsonSerializer.SerializeAsync(ms, GetIndex(ragId).Values.ToList(), cancellationToken: ct);
        ms.Position = 0;

        await _minio.PutObjectAsync(
            new PutObjectArgs()
                .WithBucket(_settings.Bucket)
                .WithObject(IndexKey(ragId))
                .WithStreamData(ms)
                .WithObjectSize(ms.Length)
                .WithContentType("application/json"),
            ct);
    }
}