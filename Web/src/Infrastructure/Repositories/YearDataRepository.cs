using Microsoft.EntityFrameworkCore;
using AutoRag.Domain.Entities;
using AutoRag.Domain.Interfaces.Repositories;
using AutoRag.Infrastructure.Persistence;
namespace AutoRag.Infrastructure.Repositories;
public sealed class YearDataRepository:GenericRepository<YearData,int>,IYearDataRepository
{
    public YearDataRepository(AutoRagContext ctx):base(ctx){}
    public async Task<IReadOnlyList<YearData>> GetByYearAsync(int year, CancellationToken ct=default)
        => await _set.Where(x=>x.Year==year).ToListAsync(ct);
}
