from sklearn.preprocessing import OneHotEncoder


class OneHotEncoder:
    def __init__(self):
        self.categories = []

    def fit(self, data):
        unique_values = set(data)
        self.categories = list(unique_values)

    def transform(self, data):
        encoded_data = []
        for value in data:
            encoded_row = [1 if value ==
                           category else 0 for category in self.categories]
            encoded_data.append(encoded_row)
        return encoded_data


class OneHotDecoder:
    def __init__(self, categories):
        self.categories = categories

    def transform(self, encoded_data):
        decoded_data = [self.categories[row.index(1)] for row in encoded_data]
        return decoded_data


if __name__ == '__main__':
    data = ['Python', 'C++', 'C#', 'PHP']
    encoder = OneHotEncoder()
    encoder.fit(data)

    encoded_data = encoder.transform(data)
    print('Encoded data:', encoded_data)

    # Test the OneHotDecoder class
    decoder = OneHotDecoder(encoder.categories)
    decoded_data = decoder.transform(encoded_data)
    print('Decoded data:', decoded_data)
