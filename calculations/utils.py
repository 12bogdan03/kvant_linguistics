from collections import Counter, OrderedDict
from math import sqrt


def generate_frequency_dictionary(words):
    d = dict(Counter(words))
    result = OrderedDict()
    items = list(d.items())
    items.sort(key=lambda item: item[1], reverse=True)
    for item in items:
        result[item[0]] = item[1]
    return result


def get_absolute_frequency(word, sample):
    return sample.count(word)


def get_parts_list(general_sample, number_of_samples):
    sample_length = len(general_sample) // number_of_samples
    parts = [general_sample[i:i + sample_length] for i in
            range(0, len(general_sample), sample_length)]
    if len(parts) > number_of_samples:
        return parts[:number_of_samples]
    return parts


def get_frequencies_list(word, parts):
    frequencies = list()
    for p in parts:
        frequencies.append(get_absolute_frequency(word, p))
    return frequencies


def generate_variation_series(word, general_sample, number_of_samples):
    parts = get_parts_list(general_sample, number_of_samples)
    frequencies = get_frequencies_list(word, parts)

    frequencies = Counter(frequencies)

    return frequencies


def get_average_frequency(word, general_sample, number_of_samples):
    parts = get_parts_list(general_sample, number_of_samples)
    frequencies = get_frequencies_list(word, parts)

    frequencies = Counter(frequencies)

    multiplications = [frequencies[i]*i for i in frequencies]
    multiplications_sum = sum(multiplications)
    return multiplications_sum/len(parts)


def get_relative_frequency_1(word, general_sample, number_of_samples):
    parts = get_parts_list(general_sample, number_of_samples)
    frequencies = get_frequencies_list(word, parts)

    variation_series = [frequencies[i]/len(parts[i]) for i in
                        range(len(parts))]
    frequencies_count = [frequencies.count(i) for i in frequencies]

    multiplications = [variation_series[i]*frequencies_count[i]
                       for i in range(len(variation_series))]
    multiplications_sum = sum(multiplications)
    return multiplications_sum/sum(frequencies_count)


def get_relative_frequency_2(word, general_sample, number_of_samples):
    parts = get_parts_list(general_sample, number_of_samples)
    frequencies = get_frequencies_list(word, parts)

    parts_length = 0
    for p in parts:
        parts_length += len(p)

    return sum(frequencies)/parts_length


def get_average_quadratic_deviation(word, general_sample, number_of_samples):
    parts = get_parts_list(general_sample, number_of_samples)
    frequencies = get_frequencies_list(word, parts)

    frequencies = Counter(frequencies)
    Xi = [i for i in frequencies]
    Ni = [frequencies[i] for i in frequencies]

    average_frequency = get_average_frequency(word, general_sample,
                                              number_of_samples)

    #  temporary variable, to sum numerator later
    n = [((Xi[i] - average_frequency)**2)*Ni[i] for i in range(len(Xi))]
    numerator = sum(n)
    denominator = sum(Ni)

    return sqrt(numerator/denominator)


def get_confidence_interval_2_sigma(word, general_sample, number_of_samples):
    parts = get_parts_list(general_sample, number_of_samples)
    average_quadratic_deviation = get_average_quadratic_deviation(word,
                                                                  general_sample,
                                                                  number_of_samples)
    average_frequency = get_average_frequency(word, general_sample,
                                              number_of_samples)
    minimum = average_frequency - 2*average_quadratic_deviation
    maximum = average_frequency + 2*average_quadratic_deviation
    frequencies = get_frequencies_list(word, parts)
    number_of_appropriate_frequencies = 0

    for f in frequencies:
        if minimum <= f <= maximum:
            number_of_appropriate_frequencies += 1

    return (minimum, maximum,
            (number_of_appropriate_frequencies*100)/len(frequencies))


def get_variation_of_average_frequency(word, general_sample, number_of_samples):
    average_quadratic_deviation = get_average_quadratic_deviation(word,
                                                                  general_sample,
                                                                  number_of_samples)
    parts = get_parts_list(general_sample, number_of_samples)
    return average_quadratic_deviation/sqrt(len(parts))


def get_confidence_interval_2_variation_of_average_frequency(word,
                                                             general_sample,
                                                             number_of_samples):
    parts = get_parts_list(general_sample, number_of_samples)

    variation_of_average_frequency = get_variation_of_average_frequency(word,
                                                                        general_sample,
                                                                        number_of_samples)
    average_frequency = get_average_frequency(word, general_sample,
                                              number_of_samples)
    minimum = average_frequency - 2 * variation_of_average_frequency
    maximum = average_frequency + 2 * variation_of_average_frequency

    frequencies = get_frequencies_list(word, parts)
    number_of_appropriate_frequencies = 0

    for f in frequencies:
        if minimum <= f <= maximum:
            number_of_appropriate_frequencies += 1

    return (minimum, maximum,
            (number_of_appropriate_frequencies * 100)/len(frequencies))


def get_coefficient_of_variation(word, general_sample, number_of_samples):
    average_quadratic_deviation = get_average_quadratic_deviation(word,
                                                                  general_sample,
                                                                  number_of_samples)
    average_frequency = get_average_frequency(word,
                                              general_sample,
                                              number_of_samples)
    return average_quadratic_deviation/average_frequency


def get_max_coefficient_of_variation(general_sample, number_of_samples):
    parts = get_parts_list(general_sample, number_of_samples)
    return sqrt(len(parts)-1)


def get_coefficient_of_stability(word, general_sample, number_of_samples):
    coefficient_of_variation = get_coefficient_of_variation(word,
                                                            general_sample,
                                                            number_of_samples)
    max_coefficient_of_variation = get_max_coefficient_of_variation(general_sample,
                                                                    number_of_samples)
    return 1-(coefficient_of_variation/max_coefficient_of_variation)


def get_relative_error(word, general_sample, number_of_samples):
    variation_of_average_frequency = get_variation_of_average_frequency(word,
                                                                        general_sample,
                                                                        number_of_samples)
    average_frequency = get_average_frequency(word, general_sample, number_of_samples)
    return (1.96*variation_of_average_frequency)/average_frequency


def generate_characteristics_dict(word, words, number_of_samples):
    characterictics_dict = dict()

    abs_freq = get_absolute_frequency(word, words)
    avg_freq = get_average_frequency(word, words,
                                     number_of_samples)
    rel_freq_1 = get_relative_frequency_1(word, words,
                                          number_of_samples)
    rel_freq_2 = get_relative_frequency_2(word, words,
                                          number_of_samples)
    avg_quadratic_dev = get_average_quadratic_deviation(word,
                                                        words,
                                                        number_of_samples)

    minimum = str(round(get_confidence_interval_2_sigma(word,
                                                        words,
                                                        number_of_samples)[0], 2))
    maximum = str(round(get_confidence_interval_2_sigma(word, words,
                                                        number_of_samples)[1], 2))
    percentage = str(get_confidence_interval_2_sigma(word, words,
                                                     number_of_samples)[2])
    # довірчий інтервал 2σ
    confidence_interval_1 = 'min:' + minimum + ', ' + 'max:' + maximum + '  охоплює ' + percentage + '%' + ' вибірки'
    var_of_avg_freq = get_variation_of_average_frequency(word,
                                                         words,
                                                         number_of_samples)

    minimum = str(round(get_confidence_interval_2_variation_of_average_frequency(word,
                                                                                 words,
                                                                                 number_of_samples)[0], 2))
    maximum = str(round(get_confidence_interval_2_variation_of_average_frequency(word,
                                                                                 words, 10)[1], 2))
    percentage = str(get_confidence_interval_2_variation_of_average_frequency(word,
                                                                              words,
                                                                              number_of_samples)[2])
    confidence_interval_2 = 'min:' + minimum + ', ' + 'max:' + maximum + '  охоплює ' + percentage + '%' + ' вибірки'

    coef_of_variation = get_coefficient_of_variation(word, words,
                                                     number_of_samples)
    max_coef_of_variation = get_max_coefficient_of_variation(words,
                                                             number_of_samples)
    coef_of_stability = get_coefficient_of_stability(word,
                                                     words,
                                                     number_of_samples)
    relative_error = get_relative_error(word, words,
                                        number_of_samples)

    characterictics_dict['Абсолютна частота'] = abs_freq
    characterictics_dict['Середня частота'] = avg_freq
    characterictics_dict['Середня відн. частота(метод 1)'] = rel_freq_1
    characterictics_dict['Середня відн. частота(метод 2)'] = rel_freq_2
    characterictics_dict['Середнє квадрат. відхилення'] = avg_quadratic_dev
    characterictics_dict['Інтервал 2σ'] = confidence_interval_1
    characterictics_dict['Міра колив.сер.част.'] = var_of_avg_freq
    characterictics_dict['Інтервал 2σх'] = confidence_interval_2
    characterictics_dict['Коефіцієнт варіації'] = coef_of_variation
    characterictics_dict['Макс.коефіцієнт варіації'] = max_coef_of_variation
    characterictics_dict['Коефіцієнт стабільності'] = coef_of_stability
    characterictics_dict['Відносна похибка дослідження'] = relative_error

    return characterictics_dict
