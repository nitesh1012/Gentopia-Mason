from gentopia.tools import BaseTool, BaseModel, Field
from typing import Optional, Type, Any

class TravelPlannerArgs(BaseModel):
    cities: str = Field(..., description="A comma-separated list of cities for the travel itinerary.")

class TravelPlanner(BaseTool):
    name = "travel_planner"
    description = "A tool that generates travel itineraries for cities provided by the user."

    args_schema: Optional[Type[BaseModel]] = TravelPlannerArgs

    def _run(self, cities: str) -> str:
        """
        Generates a travel itinerary for a list of cities provided by the user.

        Args:
            cities (str): A comma-separated string of city names.

        Returns:
            str: Itinerary for the specified cities.
        """
        city_list = [city.strip() for city in cities.split(",")]

        
        itinerary = []

        for city in city_list:
            itinerary.append(f"Here are suggested activities for your trip to {city}:\n")
            itinerary.append(f"1. Explore popular landmarks in {city}.")
            itinerary.append(f"2. Enjoy local cuisine in {city}.")
            itinerary.append(f"3. Visit historical or cultural museums in {city}.")
            itinerary.append(f"4. Take a guided tour or explore the downtown area of {city}.\n")

        
        return "\n".join(itinerary)

    async def _arun(self, cities: str) -> str:
        return self._run(cities)
