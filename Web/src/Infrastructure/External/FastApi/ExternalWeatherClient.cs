using AutoRag.Application.DTOs;
using AutoRag.Application.Interfaces;
using System.Net.Http.Json;
namespace AutoRag.Infrastructure.External.FastApi;
public sealed class ExternalWeatherClient : IExternalWeatherService
{
    private readonly HttpClient _http;
    public ExternalWeatherClient(HttpClient http)=>_http=http;
    public async Task<WeatherInfo> GetWeatherByYearAsync(int year, CancellationToken ct = default)
        => await _http.GetFromJsonAsync<WeatherInfo>($"weather/{year}", ct)
            ?? throw new InvalidOperationException("No weather data");
}
