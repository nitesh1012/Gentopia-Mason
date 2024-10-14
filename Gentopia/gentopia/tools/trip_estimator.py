from gentopia.tools import BaseTool
from pydantic import BaseModel, Field
from typing import AnyStr, Optional, Type, Any
from amadeus import Client, ResponseError


amadeus = Client(
    client_id='',  # Your API client ID
    client_secret=''  # Your API client secret key
)


class EstimateTripCostArgs(BaseModel):
    origin: str = Field(..., description="The IATA code of the origin airport, e.g., JFK for New York.")
    destination: str = Field(..., description="The IATA code of the destination airport, e.g., CDG for Paris.")
    days: int = Field(..., description="The number of days the user plans to stay.")
    travel_class: str = Field(..., description="The type of travel class (economy, business).")


class EstimateTripCost(BaseTool):
    name = "estimate_trip_cost"
    description = "Estimates the trip cost for a specified location, number of days, and travel class."

    args_schema: Optional[Type[BaseModel]] = EstimateTripCostArgs

    
    def _run(self, origin: str, destination: str, days: int, travel_class: str) -> str:
        try:
            
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate="2024-10-30",  
                adults=1,
                travelClass=travel_class.upper(),  
                max=1 
            )

            
            flight_cost = response.data[0]['price']['total']

            
            cost_per_day = 100  
            if travel_class.lower() == "business":
                cost_per_day = 200  

            
            accommodation_cost = cost_per_day * days

            
            total_cost = float(flight_cost) + accommodation_cost

            
            return (f"The estimated cost for your trip from {origin} to {destination} for {days} days in {travel_class} class is:\n"
                    f"Flight Cost: ${flight_cost}\n"
                    f"Accommodation Cost: ${accommodation_cost}\n"
                    f"Total Estimated Cost: ${total_cost}")

        except ResponseError as error:
            return f"An error occurred while fetching flight prices: {error}"

    
    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError  



if __name__ == "__main__":
    
    trip_estimator = EstimateTripCost()

    
    origin = "JFK"  
    destination = "CDG"
    days = 5
    travel_class = "economy"

    
    result = trip_estimator._run(origin, destination, days, travel_class)
    print(result)
