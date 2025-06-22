using AutoRag.Application.DTOs;
namespace AutoRag.Application.Interfaces; 
public interface IExternalWeatherService
{ 
    Task<WeatherInfo> GetWeatherByYearAsync(int year, CancellationToken ct = default);
}
