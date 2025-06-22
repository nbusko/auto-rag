using AutoRag.Application.Interfaces;
using AutoRag.Domain.Interfaces.Factories;
using Microsoft.Extensions.DependencyInjection;
namespace AutoRag.Infrastructure.Factories;
public sealed class ServiceFactory:IServiceFactory
{
    private readonly IServiceProvider _sp;
    public ServiceFactory(IServiceProvider sp)=>_sp=sp;
    public IYearDataService YearDataService => _sp.GetRequiredService<IYearDataService>();

    IYearDataService IServiceFactory.YearDataService => throw new NotImplementedException();
}
