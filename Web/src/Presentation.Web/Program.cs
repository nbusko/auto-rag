using AutoRag.Application.Interfaces;
using AutoRag.Application.Mappers;
using AutoRag.Application.Services;
using AutoRag.Domain.Interfaces.Repositories;
using AutoRag.Infrastructure.External.FastApi;
using AutoRag.Infrastructure.Persistence;
using AutoRag.Infrastructure.Repositories;
using AutoRag.Infrastructure.Storage;
using AutoRag.Infrastructure;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using Minio;
using MudBlazor.Services;
using Pgvector.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);
var cfg = builder.Configuration;

/* ---------- Connection string ---------- */
var connectionString =
        cfg.GetConnectionString("DefaultConnection") ??
        cfg.GetConnectionString("Pg") ??
        throw new InvalidOperationException("Connection string not found");

/* ---------- DbContext (pgvector enabled) ---------- */
builder.Services.AddDbContext<AutoRagContext>(o =>
    o.UseNpgsql(connectionString, npg => npg.UseVector()));

/* ---------- current user accessor ---------- */
builder.Services.AddScoped<ICurrentUser, CurrentUserAccessor>();

/* ---------- MinIO ---------- */
builder.Services.Configure<MinioSettings>(cfg.GetSection("Minio"));

builder.Services.AddSingleton<IMinioClient>(sp =>
{
    var opt = sp.GetRequiredService<IOptions<MinioSettings>>().Value;
    var uri = new Uri(opt.Endpoint, UriKind.Absolute);
    var host = uri.IsDefaultPort ? uri.Host : $"{uri.Host}:{uri.Port}";
    var useSsl = uri.Scheme == Uri.UriSchemeHttps;

    var c = new MinioClient()
        .WithEndpoint(host)
        .WithCredentials(opt.AccessKey, opt.SecretKey);

    if (useSsl) c = c.WithSSL();
    return c.Build();
});

/* ---------- Repositories ---------- */
builder.Services.AddScoped<IUserRepository, UserRepository>();
builder.Services.AddScoped<IYearDataRepository, YearDataRepository>();
builder.Services.AddScoped<IRagConfigRepository, RagConfigRepository>();
builder.Services.AddScoped<IChatHistoryRepository, ChatHistoryRepository>();
builder.Services.AddScoped<IShareLinkRepository, ShareLinkRepository>();
builder.Services.AddScoped<IDocumentEmbeddingRepository, DocumentEmbeddingRepository>();

/* ---------- External clients ---------- */
builder.Services.AddHttpClient<IExternalWeatherService, ExternalWeatherClient>(c =>
    c.BaseAddress = new Uri(cfg["ExternalApis:Weather"]!));

builder.Services.AddHttpClient<IAssistantService, AssistantClient>(c =>
    c.BaseAddress = new Uri(cfg["ExternalApis:Assistant"]!));

builder.Services.AddHttpClient<IRagService, RagServiceClient>(c =>
{
    var baseUrl = cfg["ExternalApis:RagService"] ?? "http://rag_service:5050/";
    c.BaseAddress = new Uri(baseUrl);
});

builder.Services.AddHttpClient<IDocumentProcessorService, DocumentProcessorClient>(c =>
{
    var baseUrl = cfg["ExternalApis:DocumentProcessor"] ?? "http://document_processor:5030/";
    c.BaseAddress = new Uri(baseUrl);
});

/* ---------- Services ---------- */
builder.Services.AddScoped<IAuthService, AuthService>();
builder.Services.AddScoped<IAccountService, AccountService>();
builder.Services.AddScoped<IYearDataService, YearDataService>();
builder.Services.AddScoped<IRagConfigService, RagConfigService>();
builder.Services.AddScoped<IChatService, ChatService>();
builder.Services.AddScoped<IFileStorageService, MinioFileStorageService>();
builder.Services.AddScoped<IShareService, ShareService>();

/* ---------- misc ---------- */
builder.Services.AddAutoMapper(typeof(YearDataProfile).Assembly);
builder.Services.AddMudServices();
builder.Services.AddRazorPages();
builder.Services.AddServerSideBlazor();

var app = builder.Build();

app.UseStaticFiles();
app.UseRouting();
app.MapBlazorHub();
app.MapRazorPages();
app.MapFallbackToPage("/_Host");

app.Run();