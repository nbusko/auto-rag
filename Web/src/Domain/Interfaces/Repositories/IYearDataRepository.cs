using AutoRag.Domain.Entities;
namespace AutoRag.Domain.Interfaces.Repositories;
public interface IYearDataRepository : IGenericRepository<YearData,int>
{
    Task<IReadOnlyList<YearData>> GetByYearAsync(int year, CancellationToken ct = default);
}
