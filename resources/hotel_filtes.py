def normalize_path_params(estrelas_min=0,
                          estrelas_max=5,
                          diaria_min=0,
                          diaria_max=1000,
                          limit=50,
                          offset=0,
                          cidade=None, **data):
    if not cidade:
        params = {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'limit': limit,
            'offset': offset
        }
    else:
        params = {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'cidade': cidade,
            'limit': limit,
            'offset': offset
        }
    return params


def hotels_query(with_city: bool):
    return "SELECT * FROM hoteis " \
           "WHERE (estrelas > ? and estrelas < ?) " \
           "and (diaria > ? and diaria < ?) " \
           "{} LIMIT ? OFFSET ?".format("and cidade = ?" if with_city else "")