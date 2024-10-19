from dataclasses import asdict, dataclass

# Define a mapping between spreadsheet headers and Item class field names
HEADER_TO_FIELD_MAP = {
    '#': 'index',
    'City': 'city',
    'Neighborhood': 'neighborhood',
    'Image': 'image',
    'Zipcodes': 'zipcode',
    'Ranking in City': 'ranking_in_city',
    'Overall Grade': 'overall_grade',
    'Short descreption': 'short_description',
    'Population': 'population',
    'Median Home Value': 'median_home_value',
    'Rent': 'rent',
    'Rent/Value': 'rent_value',
    'Rent / Own': 'rent_own',
    'Schools': 'schools',
    'Housing': 'housing',
    'Good for Families': 'good_for_families',
    'Jobs': 'jobs',
    'Cost Of Living': 'cost_of_living',
    'Outdoors activivties': 'outdoor_activities',
    'Crime & Safety': 'crime_safety',
    'Nightlife': 'nightLife',
    'Diversity': 'diversity',
    'Weather': 'weather',
    'Heath & Fitness': 'health_fitness',
    'Commute': 'commute',
    '# of MF for sale': 'no_of_MF_for_sale',
    'Average price / unit From Redfin': 'avg_pri_UFR',
    'YOY Growth': 'YOY_Growth1',
    '# of homes sold': 'no_of_homes_sold',
    'YOY Growth': 'YOY_Growth2',
    'Median Days on Market': 'MDOM',
    'YOY Growth': 'YOY_Growth',
    'Sale to list price': 'sale_to_list_price',
    'Avg home sale to list price': 'avg_home_sale',
    'Days to pending': 'Days_to_pending'
}


@dataclass
class MergedItem:
    city: str | None
    neighborhood: str | None
    image: str | None
    zipcode: str | None
    ranking_in_city: str | None
    overall_grade: str | None
    short_description: str | None
    population: str | None
    median_home_value: str | None
    rent: str | None
    rent_value: str | None
    rent_own: str | None
    schools: str | None
    housing: str | None
    good_for_families: str | None
    jobs: str | None
    cost_of_living: str | None
    outdoor_activities: str | None
    crime_safety: str | None
    nightLife: str | None
    diversity: str | None
    weather: str | None
    health_fitness: str | None
    commute: str | None
    no_of_MF_for_sale: str | None
    avg_pri_UFR: str | None
    YOY_Growth1: str | None
    no_of_homes_sold: str | None
    YOY_Growth2: str | None
    MDOM: str | None
    YOY_Growth: str | None
    sale_to_list_price: str | None
    avg_home_sale: str | None
    Days_to_pending: str | None
