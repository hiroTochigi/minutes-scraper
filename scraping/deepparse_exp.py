from deepparse.parser import AddressParser

address_parser = AddressParser(model_type="bpemb", device=0)

# you can parse one address
parsed_address = address_parser("4219 E 31st St, Tulsa, OK")
print(parsed_address)
# or multiple addresses
parsed_address = address_parser(["4219 E 31st St Tulsa OK", "350 rue des Lilas Ouest Québec Québec G1L 1B6"])
print(parsed_address)

# you can also get the probability of the predicted tags
parsed_address = address_parser("4219 E 31st St, Tulsa, OK", with_prob=True)
print(parsed_address)
