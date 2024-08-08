# def iterate_nested_json_for_loop(json_obj):
#     ans={}
#     for key, value in json_obj.items():
#         if isinstance(value, dict):
#             iterate_nested_json_for_loop(value)
#         else:
#             print(f"{key}: {value}") 
#             # ans[key]=value
#     # for k,v in ans:
#     #   print(k,' ',v)

# def iterate_nested_json_recursive(json_obj):
#     print("recursive way-------->")
#     for key, value in json_obj.items():
#         if isinstance(value, dict):
#             iterate_nested_json_recursive(value)
#         else:
#             print(f"{key}: {value}")


# data = {
#   "state": "Maharashtra",
#   "village": "Belebhat",
#   "district": "Kolhapur",
#   "uniqueid": "aacc148a-9670-4a95-88e8-80f8802a676f",
#   "village_code": "568109",
#   "agricultural_data": {
#     "area": 8,
#     "crop_type": "chilli",
#     "soil_type": "clay",
#     "weather_data": {
#       "humidity": {
#         "average_percentage": 7
#       },
#       "Rain_fall": {
#         "total_mm": 2122,
#         "rainy_days": 2417
#       },
#       "temprature": {
#         "max": 321,
#         "min": 148,
#         "average": 290
#       }
#     },
#     "area_cultivated": 268,
#     "yeild_perhectare": 14,
#     "irrigation_method": "flooing",
#     "pesticide_and_fertilizer_usage": {
#       "pesticides": [
#         {
#           "type": "Fungicide",
#           "quantity_l": 106
#         }
#       ],
#       "fertilizers": [
#         {
#           "type": "NPK",
#           "quantity_kg": 567
#         },
#         {
#           "type": "Compost",
#           "quantity_kg": 777
#         }
#       ]
#     }
#   }
# }

# print("Using For Loop")
# # iterate_nested_json_for_loop(data)
# iterate_nested_json_recursive(data)


# import time

# def say_hello():
#     time.sleep(2)
#     print("Hello, Async World? (not yet)")

# say_hello()

# import asyncio

# async def say_hello_async():
#     await asyncio.sleep(2)
#     print("Hello, Async World!")

# asyncio.run(say_hello_async())


import asyncio

async def say_hello_async():
    await asyncio.sleep(2)  # Simulates waiting for 2 seconds
    print("Hello, Async World!")

async def do_something_else():
    print("Starting another task...")
    await asyncio.sleep(2)  # Simulates doing something else for 1 second
    print("Finished another task!")

async def main():
    # Schedule both tasks to run concurrently
    await asyncio.gather(
        say_hello_async(),
        do_something_else(),
    )

asyncio.run(main())




