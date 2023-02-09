from duffel_api import Duffel

access_token = 'duffel_test_oIhQWAsHL9jNbWw0xrNv6fgHyowzSM-AVq9grhkWJAY'
client = Duffel(access_token = access_token)

slices = [
  {
    "origin": "CPH",
    "destination": "BKK",
    "departure_date": "2022-10-24"
  }
]
passengers = [{ "type": "adult" }]
offers = client.offer_requests.create().slices(slices).passengers(passengers).cabin_class("business").execute().offers


print(offers)



