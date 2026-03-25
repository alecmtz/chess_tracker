data = [{'preRating': 2070, 'postRating': 2076, 'ratingSource': 'R', 'name': 'Evanston 3x3 3/21/2026', 'endDate': '2026-03-21', 'stateCode': 'IL', 'sectionName': 'Gold'}, {'preRating': 1865, 'postRating': 1882, 'ratingSource': 'Q', 'name': 'Evanston 3x3 3/21/2026', 'endDate': '2026-03-21', 'stateCode': 'IL', 'sectionName': 'Gold'}]
final_list = []
for dictionary in data:
    new_list = [
        123456,
        dictionary["endDate"],
        dictionary["stateCode"],
        dictionary["name"],
        dictionary["sectionName"],
        dictionary["ratingSource"],
        dictionary["preRating"],
        dictionary["postRating"],
    ]
    final_list.append(new_list)

print(final_list)