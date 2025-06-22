using System.Linq;
using AutoMapper;
using AutoRag.Application.DTOs;
using AutoRag.Domain.Interfaces.Repositories;
using AutoRag.Application.Interfaces;
namespace AutoRag.Application.Services; 
public sealed class YearDataService : IYearDataService
{
    private readonly IYearDataRepository _repo;
    private readonly IExternalWeatherService _weather;
    private readonly IMapper _mapper;
    public YearDataService(IYearDataRepository r,IExternalWeatherService w,IMapper m)=>( _repo,_weather,_mapper)=(r,w,m);

    public async Task<YearDataDto> GetYearReportAsync(int year, CancellationToken ct = default)
    {
        var data = (await _repo.GetByYearAsync(year, ct)).FirstOrDefault()
                   ?? throw new KeyNotFoundException("Year not found");
        var dto = _mapper.Map<YearDataDto>(data);
        var weather = await _weather.GetWeatherByYearAsync(year, ct);
        return dto with { WeatherSummary = weather.Summary };
    }
}
