using AutoRag.Application.Mappers;
using AutoRag.Application.Services;
using AutoRag.Application.Interfaces;
using AutoRag.Domain.Interfaces.Factories;
using AutoRag.Domain.Interfaces.Repositories;
using AutoRag.Infrastructure.External.FastApi;
using AutoRag.Infrastructure.Factories;
using AutoRag.Infrastructure.Persistence;
using AutoRag.Infrastructure.Repositories;
using AutoRag.Infrastructure.Storage;
using AutoRag.Infrastructure.ServicesStub;
using Microsoft.EntityFrameworkCore;
using Minio;
using Microsoft.Extensions.Options;
using MudBlazor.Services;

var builder = WebApplication.CreateBuilder(args);
var cfg = builder.Configuration;

/* ---------- Connection string ---------- */
var connectionString =
        cfg.GetConnectionString("DefaultConnection") ??
        cfg.GetConnectionString("Pg") ??
        throw new InvalidOperationException(
            "Connection string not found: specify ConnectionStrings:DefaultConnection or Pg");

builder.Services.AddDbContext<AutoRagContext>(o =>
    o.UseNpgsql(connectionString));

/* ---------- MinIO ---------- */
builder.Services.Configure<MinioSettings>(cfg.GetSection("Minio"));

builder.Services.AddSingleton<MinioClient>(sp =>
{
    var opts = sp.GetRequiredService<IOptions<MinioSettings>>().Value;

    return new MinioClient()
                .WithEndpoint(opts.Endpoint)
                .WithCredentials(opts.AccessKey, opts.SecretKey)
                .Build();
});

/* ---------- DI ---------- */
builder.Services.AddScoped<IYearDataRepository, YearDataRepository>();
builder.Services.AddScoped<IRagConfigRepository, RagConfigRepository>();
builder.Services.AddScoped<IRepositoryFactory, RepositoryFactory>();

builder.Services.AddHttpClient<IExternalWeatherService, ExternalWeatherClient>(c =>
    c.BaseAddress = new Uri(cfg["ExternalApis:Weather"]!));

builder.Services.AddScoped<IYearDataService, YearDataService>();
builder.Services.AddScoped<IRagConfigService, RagConfigService>();
builder.Services.AddSingleton<IFileStorageService, MinioFileStorageService>(); // реальное хранилище

/* ---- stubs ---- */
builder.Services.AddScoped<IChatService,    ChatServiceStub>();
builder.Services.AddScoped<IAccountService, AccountServiceStub>();
builder.Services.AddScoped<IAuthService,    AuthServiceStub>();
/* ---------------- */

builder.Services.AddScoped<IServiceFactory, ServiceFactory>();

/* ---------- misc ---------- */
builder.Services.AddAutoMapper(typeof(YearDataProfile).Assembly);
builder.Services.AddMudServices();
builder.Services.AddRazorPages();
builder.Services.AddServerSideBlazor();

var app = builder.Build();

/* ---------- HTTP pipeline ---------- */
app.UseStaticFiles();
app.UseRouting();

app.MapBlazorHub();
app.MapRazorPages();
app.MapFallbackToPage("/_Host");

app.Run();