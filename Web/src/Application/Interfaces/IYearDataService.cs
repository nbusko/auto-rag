using AutoRag.Application.DTOs;
namespace AutoRag.Application.Interfaces;
public interface IYearDataService
{
    Task<YearDataDto> GetYearReportAsync(int year, CancellationToken ct = default);
} 