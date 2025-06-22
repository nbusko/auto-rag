using AutoRag.Domain.Common;
namespace AutoRag.Domain.Interfaces.Repositories;
public interface IGenericRepository<TEntity,in TId> where TEntity : BaseEntity<TId>
{
    Task<TEntity?> GetByIdAsync(TId id, CancellationToken ct = default);
    Task AddAsync    (TEntity entity, CancellationToken ct = default);
    Task UpdateAsync (TEntity entity, CancellationToken ct = default);
    Task DeleteAsync (TId id, CancellationToken ct = default);
}
