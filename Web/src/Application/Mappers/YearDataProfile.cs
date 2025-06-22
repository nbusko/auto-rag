using AutoMapper;
using AutoRag.Domain.Entities;
using AutoRag.Application.DTOs;
namespace AutoRag.Application.Mappers;
public sealed class YearDataProfile : Profile
{
    public YearDataProfile()
    {
        CreateMap<YearData, YearDataDto>().ForMember(d=>d.WeatherSummary,o=>o.Ignore());
    }
}
