using AutoRag.Application.DTOs;
using AutoRag.Application.Interfaces;
using Microsoft.Extensions.Options;
using Minio;
using Minio.DataModel;
using Minio.DataModel.Args;
using Minio.Exceptions;
using System.Collections.Concurrent;

namespace AutoRag.Infrastructure.Storage;

public sealed class MinioFileStorageService : IFileStorageService
{
    private readonly IMinioClient  _minio;
    private readonly MinioSettings _settings;

    // маркер, что бакет уже проверяли/создавали
    private readonly ConcurrentDictionary<string, byte> _bucketInit = new();

    public MinioFileStorageService(IMinioClient client, IOptions<MinioSettings> opt)
    {
        _minio    = client;
        _settings = opt.Value;
    }

    /* ---------- upload ---------- */
    public async Task<DocumentInfoDto> UploadAsync(string fileName,
                                                   Stream content,
                                                   CancellationToken ct = default)
    {
        await EnsureBucketAsync(ct);

        var id        = Guid.NewGuid();
        var objectKey = $"{id}/{fileName}";

        await _minio.PutObjectAsync(
            new PutObjectArgs()
                .WithBucket      (_settings.Bucket)
                .WithObject      (objectKey)
                .WithStreamData  (content)
                .WithObjectSize  (content.Length)
                .WithContentType ("application/octet-stream"),
            ct);

        return new DocumentInfoDto(id, fileName, content.Length)
        {
            UploadedAt = DateTime.UtcNow
        };
    }

    /* ---------- list ---------- */
    public async Task<IReadOnlyList<DocumentInfoDto>> ListAsync(CancellationToken ct = default)
    {
        await EnsureBucketAsync(ct);

        // получаем асинхронный поток объектов
        IAsyncEnumerable<Item> objects = _minio.ListObjectsAsync(
            new ListObjectsArgs()
                .WithBucket   (_settings.Bucket)
                .WithRecursive(true));  // обход «папок» рекурсивно

        var dict = new Dictionary<Guid, DocumentInfoDto>();

        await foreach (var obj in objects.WithCancellation(ct))
        {
            // ожидаем ключ вида "{guid}/{filename}"
            int slash = obj.Key.IndexOf('/');
            if (slash <= 0) continue;

            var idPart   = obj.Key[..slash];
            var fileName = obj.Key[(slash + 1)..];

            if (!Guid.TryParse(idPart, out var id)) continue;

            if (!dict.ContainsKey(id))
            {
                dict[id] = new DocumentInfoDto(id, fileName, (long)obj.Size)
                {
                    UploadedAt = obj.LastModified.ToUniversalTime()
                };
            }
        }

        return dict.Values
                   .OrderByDescending(d => d.UploadedAt)
                   .ToList();
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
}
