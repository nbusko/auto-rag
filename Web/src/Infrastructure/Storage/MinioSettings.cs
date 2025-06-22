namespace AutoRag.Infrastructure.Storage;

public sealed class MinioSettings
{
    public string Endpoint  { get; init; } = string.Empty;
    public string AccessKey { get; init; } = string.Empty;
    public string SecretKey { get; init; } = string.Empty;
    public string Bucket    { get; init; } = "autorag";
}