using AutoRag.Application.Interfaces;
using AutoRag.Application.Mappers;
using AutoRag.Application.Services;
using AutoRag.Domain.Interfaces.Repositories;
using AutoRag.Infrastructure.External.FastApi;
using AutoRag.Infrastructure.Factories;
using AutoRag.Infrastructure.Persistence;
using AutoRag.Infrastructure.Repositories;
using AutoRag.Infrastructure.Storage;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using Minio;
using MudBlazor.Services;

var builder = WebApplication.CreateBuilder(args);
var cfg = builder.Configuration;

/* ---------- Connection string ---------- */
var connectionString =
        cfg.GetConnectionString("DefaultConnection") ??
        cfg.GetConnectionString("Pg") ??
        throw new InvalidOperationException("Connection string not found");

builder.Services.AddDbContext<AutoRagContext>(o => o.UseNpgsql(connectionString));

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
builder.Services.AddScoped<IYearDataRepository,     YearDataRepository>();
builder.Services.AddScoped<IRagConfigRepository,    RagConfigRepository>();
builder.Services.AddScoped<IChatHistoryRepository,  ChatHistoryRepository>();

/* ---------- External clients ---------- */
builder.Services.AddHttpClient<IExternalWeatherService, ExternalWeatherClient>(c =>
    c.BaseAddress = new Uri(cfg["ExternalApis:Weather"]!));

builder.Services.AddHttpClient<IAssistantService, AssistantClient>(c =>
    c.BaseAddress = new Uri(cfg["ExternalApis:Assistant"]!));

/* ---------- Services ---------- */
builder.Services.AddScoped<IYearDataService, YearDataService>();
builder.Services.AddScoped<IRagConfigService, RagConfigService>();
builder.Services.AddScoped<IChatService,      ChatService>();
builder.Services.AddSingleton<IFileStorageService, MinioFileStorageService>();

/* ---- заглушки ---- */
builder.Services.AddScoped<IAccountService, AutoRag.Infrastructure.ServicesStub.AccountServiceStub>();
builder.Services.AddScoped<IAuthService,    AutoRag.Infrastructure.ServicesStub.AuthServiceStub>();

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