using Microsoft.EntityFrameworkCore;
using AutoRag.Domain.Common;
using AutoRag.Domain.Interfaces.Repositories;
using AutoRag.Infrastructure.Persistence;
namespace AutoRag.Infrastructure.Repositories;
public class GenericRepository<TEntity,TId>:IGenericRepository<TEntity,TId> where TEntity:BaseEntity<TId>
{
    protected readonly AutoRagContext _ctx;
    protected readonly DbSet<TEntity> _set;
    public GenericRepository(AutoRagContext ctx){_ctx=ctx;_set=ctx.Set<TEntity>();}

    public async Task<TEntity?> GetByIdAsync(TId id, CancellationToken ct=default)
        => await _set.FindAsync(new object?[]{id}, ct);

    public async Task AddAsync(TEntity entity, CancellationToken ct=default)
    { await _set.AddAsync(entity,ct); await _ctx.SaveChangesAsync(ct); }

    public async Task UpdateAsync(TEntity entity, CancellationToken ct=default)
    { _set.Update(entity); await _ctx.SaveChangesAsync(ct); }

    public async Task DeleteAsync(TId id, CancellationToken ct=default)
    { var e=await GetByIdAsync(id,ct); if(e!=null){_set.Remove(e); await _ctx.SaveChangesAsync(ct);} }
}
