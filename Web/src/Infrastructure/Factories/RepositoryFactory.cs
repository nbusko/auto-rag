using AutoRag.Domain.Interfaces.Factories;
using AutoRag.Domain.Interfaces.Repositories;
using AutoRag.Infrastructure.Persistence;
using AutoRag.Infrastructure.Repositories;
namespace AutoRag.Infrastructure.Factories;
public sealed class RepositoryFactory:IRepositoryFactory
{
    private readonly AutoRagContext _ctx;
    public RepositoryFactory(AutoRagContext ctx)=>_ctx=ctx;
    public IYearDataRepository YearDataRepository => new YearDataRepository(_ctx);
}
