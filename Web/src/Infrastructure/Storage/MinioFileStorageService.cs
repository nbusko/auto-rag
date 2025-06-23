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
    private const string IndexObjectKey = "_index.json";

    private readonly IMinioClient _minio;          // интерфейс вместо класса
    private readonly MinioSettings _settings;

    private static readonly ConcurrentDictionary<Guid, DocumentInfoDto> _indexCache = new();
    private static readonly ConcurrentDictionary<string, byte> _bucketInit = new();

    public MinioFileStorageService(IMinioClient client, IOptions<MinioSettings> opt)
    {
        _minio = client;
        _settings = opt.Value;
    }

    /* ---------- upload ---------- */
    public async Task<DocumentInfoDto> UploadAsync(string fileName, Stream content, CancellationToken ct = default)
    {
        await EnsureBucketAsync(ct);

        var id = Guid.NewGuid();
        var objectKey = $"{id}/{fileName}";

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

        _indexCache[id] = info;
        await SaveIndexAsync(ct);

        return info;
    }

    /* ---------- list ---------- */
    public async Task<IReadOnlyList<DocumentInfoDto>> ListAsync(CancellationToken ct = default)
    {
        await EnsureBucketAsync(ct);

        if (_indexCache.IsEmpty)
            await LoadIndexAsync(ct);

        return _indexCache.Values
                          .OrderByDescending(d => d.UploadedAt)
                          .ToList()
                          .AsReadOnly();
    }

    /* ---------- helpers ---------- */
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

    private async Task LoadIndexAsync(CancellationToken ct)
    {
        try
        {
            using var ms = new MemoryStream();

            await _minio.GetObjectAsync(
                new GetObjectArgs()
                    .WithBucket(_settings.Bucket)
                    .WithObject(IndexObjectKey)
                    .WithCallbackStream(stream => stream.CopyTo(ms)),
                ct);

            ms.Position = 0;
            var list = await JsonSerializer.DeserializeAsync<List<DocumentInfoDto>>(ms, cancellationToken: ct)
                       ?? [];

            foreach (var d in list)
                _indexCache[d.Id] = d;
        }
        catch (ObjectNotFoundException)
        {
            // индекса ещё нет – это нормально
        }
    }

    private async Task SaveIndexAsync(CancellationToken ct)
    {
        await using var ms = new MemoryStream();
        await JsonSerializer.SerializeAsync(ms, _indexCache.Values.ToList(), cancellationToken: ct);
        ms.Position = 0;

        await _minio.PutObjectAsync(
            new PutObjectArgs()
                .WithBucket(_settings.Bucket)
                .WithObject(IndexObjectKey)
                .WithStreamData(ms)
                .WithObjectSize(ms.Length)
                .WithContentType("application/json"),
            ct);
    }
}