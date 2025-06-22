using AutoRag.Application.Mappers;
using AutoRag.Application.Services;
using AutoRag.Domain.Interfaces.Factories;
using AutoRag.Domain.Interfaces.Repositories;
using AutoRag.Application.Interfaces;
using AutoRag.Infrastructure.External.FastApi;
using AutoRag.Infrastructure.Factories;
using AutoRag.Infrastructure.Persistence;
using AutoRag.Infrastructure.Repositories;
using AutoRag.Infrastructure.ServicesStub;
using Microsoft.EntityFrameworkCore;
using MudBlazor.Services;

var builder = WebApplication.CreateBuilder(args);
var cfg = builder.Configuration;

builder.Services.AddDbContext<AutoRagContext>(o =>
    o.UseNpgsql(cfg.GetConnectionString("Pg")));

builder.Services.AddScoped<IYearDataRepository, YearDataRepository>();
builder.Services.AddScoped<IRepositoryFactory, RepositoryFactory>();

builder.Services.AddHttpClient<IExternalWeatherService, ExternalWeatherClient>(c =>
    c.BaseAddress = new Uri(cfg["ExternalApis:Weather"]!));

builder.Services.AddScoped<IYearDataService, YearDataService>();
builder.Services.AddScoped<IServiceFactory, ServiceFactory>();
builder.Services.AddScoped<IAuthService, AuthServiceStub>();
builder.Services.AddScoped<IFileStorageService, FileStorageServiceStub>();

builder.Services.AddScoped<IRagConfigRepository, RagConfigRepository>();
builder.Services.AddScoped<IRagConfigService, RagConfigService>();

builder.Services.AddScoped<IChatService, ChatServiceStub>();
builder.Services.AddScoped<IAccountService, AccountServiceStub>();

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