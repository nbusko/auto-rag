using AutoRag.Domain.Interfaces.Repositories;
namespace AutoRag.Domain.Interfaces.Factories;
public interface IRepositoryFactory { IYearDataRepository YearDataRepository { get; } }
