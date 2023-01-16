import json
from functools import reduce

categories = [
    {"_id": "629d286bec74d540eb5fb0e7", "name": "Roupas de cima",
        "description": "Camisas, camisetas, polos, blusas ou regatas", "sort": 1},
    {"_id": "629d286bec74d540eb5fb0e8", "name": "Pernas",
        "description": "Calças, shorts, saias ou bermudas", "sort": 2},
    {"_id": "629d286bec74d540eb5fb0e9", "name": "Pés",
        "description": "Calçados ou meias", "sort": 3},
	{"_id": "629d286bec74d540eb5fb0ea", "name": "Peças sobrepostas",
        "description": "Casacos, jaquetas, moletons ou sobretudos", "sort": 4},
    {"_id": "629d286bec74d540eb5fb0eb", "name": "Peças únicas",
        "description": "Vestidos ou macacões", "sort": 5},
    {"_id": "629d286bec74d540eb5fb0ec", "name": "Acessórios de cabeça",
        "description": "Bonés, chapéus, óculos, brincos ou laços", "sort": 6},
    {"_id": "629d286bec74d540eb5fb0ed", "name": "Acessórios de pescoço",
        "description": "Colares, correntes, gravatas ou cachecóis", "sort": 7},
    {"_id": "629d286bec74d540eb5fb0ee", "name": "Acessórios de braços e mãos",
        "description": "Bolsas, pulseiras, relógios, anéis ou luvas", "sort": 8},
    {"_id": "629d286bec74d540eb5fb0ef", "name": "Cintura",
        "description": "Cintos ou laços", "sort": 9}
]
clothes = [
    {
        "_id": "62a413f666724c5f403cf980",
        "category_id": "629d286bec74d540eb5fb0e9",
        "closet_id": "72177720299676310",
        "image": "https://live.staticflickr.com/65535/52137525213_e856c41ae9_n.jpg",
        "occasions": [
            "6315604bdaf4e3d095035213",
            "6315604bdaf4e3d095035214",
            "6315604bdaf4e3d095035216",
            "6315604bdaf4e3d095035215",
            "6315604bdaf4e3d095035212"
        ],
        "seasons": [
            "primavera",
            "verão",
            "outono"
        ],
        "type": "casual"
    },
    {
        "_id": "62a413f966724c5f403cf981",
        "category_id": "629d286bec74d540eb5fb0e9",
        "closet_id": "72177720299676310",
        "image": "https://live.staticflickr.com/65535/52137741934_a4a99fcabf_n.jpg",
        "occasions": [
            "6315604bdaf4e3d095035213",
            "6315604bdaf4e3d095035214",
            "6315604bdaf4e3d095035216",
            "6315604bdaf4e3d095035215",
            "6315604bdaf4e3d095035217",
            "6315604bdaf4e3d095035219",
            "6315604bdaf4e3d09503521a",
            "6315604bdaf4e3d09503521c"
        ],
        "seasons": [
            "primavera",
            "verão",
            "outono",
            "inverno"
        ],
        "type": "casual"
    },
    {
        "_id": "62a4140866724c5f403cf986",
        "category_id": "629d286bec74d540eb5fb0e8",
        "closet_id": "72177720299676310",
        "image": "https://live.staticflickr.com/65535/52137503691_33070fd125_n.jpg",
        "occasions": [
            "6315604bdaf4e3d095035212",
            "6315604bdaf4e3d095035213",
            "6315604bdaf4e3d095035214",
            "6315604bdaf4e3d095035215",
            "6315604bdaf4e3d095035216",
            "6315604bdaf4e3d095035217",
            "6315604bdaf4e3d095035218",
            "6315604bdaf4e3d095035219",
            "6315604bdaf4e3d09503521a"
        ],
        "seasons": [
            "primavera",
            "verão",
            "outono",
            "inverno"
        ],
        "type": "casual"
    },
    {
        "_id": "62a4169a66724c5f403cf987",
        "category_id": "629d286bec74d540eb5fb0e8",
        "closet_id": "72177720299676310",
        "image": "https://live.staticflickr.com/65535/52137515811_b8022953f4_n.jpg",
        "occasions": [
            "6315604bdaf4e3d095035213",
            "6315604bdaf4e3d095035214",
            "6315604bdaf4e3d095035216",
            "6315604bdaf4e3d095035215",
            "6315604bdaf4e3d095035217",
            "6315604bdaf4e3d095035218",
            "6315604bdaf4e3d095035219",
            "6315604bdaf4e3d09503521a"
        ],
        "seasons": [
            "primavera",
            "verão",
            "outono",
            "inverno"
        ],
        "type": "casual"
    },
    {
        "_id": "62a7f1bf4ff9bba04173359a",
        "category_id": "629d286bec74d540eb5fb0e7",
        "closet_id": "72177720299676310",
        "image": "https://live.staticflickr.com/65535/52145403355_86bf6d6cab_n.jpg",
        "occasions": [
            "6315604bdaf4e3d095035213",
            "6315604bdaf4e3d095035214",
            "6315604bdaf4e3d095035216",
            "6315604bdaf4e3d095035215",
            "6315604bdaf4e3d095035217",
            "6315604bdaf4e3d095035218",
            "6315604bdaf4e3d095035219",
            "6315604bdaf4e3d09503521a"
        ],
        "seasons": [
            "primavera",
            "verão"
        ],
        "type": "casual"
    },
    {
        "_id": "62c9d85bd168f9c20acb7950",
        "category_id": "629d286bec74d540eb5fb0e7",
        "closet_id": "72177720299676310",
        "image": "https://live.staticflickr.com/65535/52205398840_b6e41d506c_n.jpg",
        "occasions": [
            "6315604bdaf4e3d095035213",
            "6315604bdaf4e3d095035214",
            "6315604bdaf4e3d095035215",
            "6315604bdaf4e3d095035216",
            "6315604bdaf4e3d095035217",
            "6315604bdaf4e3d095035219",
            "6315604bdaf4e3d09503521a"
        ],
        "seasons": [
            "primavera",
            "verão"
        ],
        "type": "casual"
    },
    {
        "_id": "62c9e3fbd168f9c20acb795a",
        "category_id": "629d286bec74d540eb5fb0e7",
        "closet_id": "72177720299676310",
        "image": "https://live.staticflickr.com/65535/52205256934_2cfce4c495_n.jpg",
        "occasions": [
            "6315604bdaf4e3d095035213",
            "6315604bdaf4e3d095035214",
            "6315604bdaf4e3d095035216",
            "6315604bdaf4e3d095035215",
            "6315604bdaf4e3d09503521a",
            "6315604bdaf4e3d095035219"
        ],
        "seasons": [
            "primavera",
            "verão"
        ],
        "type": "casual"
    },
    {
        "_id": "62cce00abce9ce70a9a56914",
        "category_id": "629d286bec74d540eb5fb0e8",
        "closet_id": "72177720299676310",
        "image": "https://live.staticflickr.com/65535/52210782224_9c450ceac7_n.jpg",
        "occasions": [
            "6315604bdaf4e3d095035214",
            "6315604bdaf4e3d095035213",
            "6315604bdaf4e3d095035216",
            "6315604bdaf4e3d095035215",
            "6315604bdaf4e3d095035217",
            "6315604bdaf4e3d095035218",
            "6315604bdaf4e3d095035219",
            "6315604bdaf4e3d09503521a"
        ],
        "seasons": [
            "primavera",
            "verão",
            "inverno",
            "outono"
        ],
        "type": "casual"
    },
    {
        "_id": "62cf902d501ba2742df1fa91",
        "category_id": "629d286bec74d540eb5fb0e9",
        "closet_id": "72177720299676310",
        "image": "https://live.staticflickr.com/65535/52215069973_f7bf69327f_n.jpg",
        "occasions": [
            "6315604bdaf4e3d095035212",
            "6315604bdaf4e3d095035213",
            "6315604bdaf4e3d095035215",
            "6315604bdaf4e3d095035216",
            "6315604bdaf4e3d095035214"
        ],
        "seasons": [
            "primavera",
            "verão"
        ],
        "type": "casual"
    },
    {
        "_id": "62cf9c58c973e41fdbfde779",
        "category_id": "629d286bec74d540eb5fb0e7",
        "closet_id": "72177720299676310",
        "image": "https://live.staticflickr.com/65535/52215124508_6fab503a0f_n.jpg",
        "occasions": [
            "6315604bdaf4e3d095035213",
            "6315604bdaf4e3d09503521c",
            "6315604bdaf4e3d09503521d"
        ],
        "seasons": [
            "primavera",
            "verão"
        ],
        "type": "casual"
    },
    {
        "_id": "62d0d70867f3eaba19fd0b53",
        "category_id": "629d286bec74d540eb5fb0e7",
        "closet_id": "72177720299676310",
        "image": "https://live.staticflickr.com/65535/52217114716_edc4eae397_n.jpg",
        "occasions": [
            "6315604bdaf4e3d095035213",
            "6315604bdaf4e3d095035214",
            "6315604bdaf4e3d095035215",
            "6315604bdaf4e3d095035216",
            "6315604bdaf4e3d095035217",
            "6315604bdaf4e3d095035219",
            "6315604bdaf4e3d09503521a"
        ],
        "seasons": [
            "primavera",
            "verão"
        ],
        "type": "casual"
    },
    {
        "_id": "62df6ea1183a033991f1ea0d",
        "category_id": "629d286bec74d540eb5fb0ee",
        "closet_id": "72177720299676310",
        "image": "https://live.staticflickr.com/65535/52241887273_30de5e7d9e_n.jpg",
        "occasions": [
            "6315604bdaf4e3d095035212",
            "6315604bdaf4e3d095035213",
            "6315604bdaf4e3d095035214",
            "6315604bdaf4e3d095035216",
            "6315604bdaf4e3d095035217",
            "6315604bdaf4e3d095035219",
            "6315604bdaf4e3d09503521a",
            "6315604bdaf4e3d09503521c",
            "6315604bdaf4e3d09503521e"
        ],
        "seasons": [
            "primavera",
            "verão",
            "inverno",
            "outono"
        ],
        "type": "casual"
    },
    {
        "_id": "62df6fcb183a033991f1ea0e",
        "category_id": "629d286bec74d540eb5fb0ec",
        "closet_id": "72177720299676310",
        "image": "https://live.staticflickr.com/65535/52242371835_00e15ba8cc_n.jpg",
        "occasions": [
            "6315604bdaf4e3d095035213",
            "6315604bdaf4e3d095035217",
            "6315604bdaf4e3d09503521a",
            "6315604bdaf4e3d09503521b",
            "6315604bdaf4e3d09503521c",
            "6315604bdaf4e3d09503521d"
        ],
        "seasons": [
            "primavera",
            "verão"
        ],
        "type": "casual"
    },
    {
        "_id": "62e881a9d778ffcff674dace",
        "category_id": "629d286bec74d540eb5fb0e7",
        "closet_id": "72177720299676310",
        "image": "https://live.staticflickr.com/65535/52257353078_592981c715_n.jpg",
        "occasions": [
            "6315604bdaf4e3d095035213",
            "6315604bdaf4e3d095035214",
            "6315604bdaf4e3d095035212",
            "6315604bdaf4e3d095035216"
        ],
        "seasons": [
            "Inverno",
            "Outono"
        ],
        "type": "casual"
    },
    {
        "_id": "62e8872913adc71d29f9a0f7",
        "category_id": "629d286bec74d540eb5fb0e9",
        "closet_id": "72177720299676310",
        "image": "https://live.staticflickr.com/65535/52257861670_1c20994936_n.jpg",
        "occasions": [
            "6315604bdaf4e3d095035213",
            "6315604bdaf4e3d095035214",
            "6315604bdaf4e3d095035216",
            "6315604bdaf4e3d095035215",
            "6315604bdaf4e3d095035217",
            "6315604bdaf4e3d095035218",
            "6315604bdaf4e3d095035219",
            "6315604bdaf4e3d09503521a"
        ],
        "seasons": [
            "primavera",
            "verão",
            "inverno",
            "outono"
        ],
        "type": "casual"
    },
    {
        "_id": "62fc60f398e43430688253f8",
        "category_id": "629d286bec74d540eb5fb0ec",
        "closet_id": "72177720299676310",
        "image": "https://live.staticflickr.com/65535/52291172091_87173b6664_n.jpg",
        "occasions": [
            "6315604bdaf4e3d095035213",
            "6315604bdaf4e3d095035216",
            "6315604bdaf4e3d095035217",
            "6315604bdaf4e3d09503521a",
            "6315604bdaf4e3d09503521b",
            "6315604bdaf4e3d09503521d"
        ],
        "seasons": [
            "primavera",
            "verão"
        ],
        "type": "casual"
    },
    {
        "_id": "62fc62a098e43430688253fa",
        "category_id": "629d286bec74d540eb5fb0ee",
        "closet_id": "72177720299676310",
        "image": "https://live.staticflickr.com/65535/52291185188_0dd455be71_n.jpg",
        "occasions": [
            "6315604bdaf4e3d095035213",
            "6315604bdaf4e3d095035214",
            "6315604bdaf4e3d095035215",
            "6315604bdaf4e3d095035216",
            "6315604bdaf4e3d095035217",
            "6315604bdaf4e3d095035218",
            "6315604bdaf4e3d095035219",
            "6315604bdaf4e3d09503521a"
        ],
        "seasons": [
            "primavera",
            "verão",
            "outono",
            "inverno"
        ],
        "type": "casual"
    },
    {
        "_id": "6316c43f9ae66942d36d846e",
        "category_id": "629d286bec74d540eb5fb0e7",
        "closet_id": "72177720299676310",
        "image": "https://live.staticflickr.com/65535/52338066380_7dbb9a9274_n.jpg",
        "occasions": [
            "6315604bdaf4e3d095035212",
            "6315604bdaf4e3d095035213",
            "6315604bdaf4e3d095035214",
            "6315604bdaf4e3d095035215",
            "6315604bdaf4e3d095035219",
            "6315604bdaf4e3d09503521a",
            "6315604bdaf4e3d09503521e"
        ],
        "seasons": [
            "primavera",
            "verão"
        ],
        "type": "casual"
    }
]
daily_look_setup = {
    "_id": "634e227711217434f4f266a8",
    "days_of_week": [
        {
            "day_of_week": "domingo",
            "occasions": [
                {
                    "casual": [
                        "dia"
                    ],
                    "occasion_id": "6315604bdaf4e3d095035220",
                    "social": [
                        "noite"
                    ]
                }
            ],
            "sort": 0
        },
        {
            "day_of_week": "segunda",
            "occasions": [
                {
                    "casual": [
                        "dia"
                    ],
                    "occasion_id": "6315604bdaf4e3d095035215",
                    "social": []
                }
            ],
            "sort": 1
        },
        {
            "day_of_week": "terça",
            "occasions": [
                {
                    "casual": [
                        "dia"
                    ],
                    "occasion_id": "6315604bdaf4e3d095035215",
                    "social": []
                },
                {
                    "casual": [
                        "noite"
                    ],
                    "occasion_id": "6315604bdaf4e3d09503521c",
                    "social": []
                }
            ],
            "sort": 2
        },
        {
            "day_of_week": "quarta",
            "occasions": [
                {
                    "casual": [
                        "dia"
                    ],
                    "occasion_id": "6315604bdaf4e3d095035215",
                    "social": []
                },
                {
                    "casual": [
                        "noite"
                    ],
                    "occasion_id": "6315604bdaf4e3d095035212",
                    "social": []
                }
            ],
            "sort": 3
        },
        {
            "day_of_week": "quinta",
            "occasions": [],
            "sort": 4
        },
        {
            "day_of_week": "sexta",
            "occasions": [
                {
                    "casual": [
                        "dia"
                    ],
                    "occasion_id": "6315604bdaf4e3d095035212",
                    "social": []
                }
            ],
            "sort": 5
        },
        {
            "day_of_week": "sábado",
            "occasions": [],
            "sort": 6
        }
    ],
    "user_id": "6298301fed1909971532ca92"
}
type = "casual"

def get_by_index(array, index):
    try:
        return array[index]
    except IndexError as e:
        return False

def generate_lookset_look(lookset, look, type, occasion_id):
    lookset_stringfy = json.dumps(lookset)
    look_stringfy = json.dumps(look)
    if look_stringfy in lookset_stringfy:
        return
    keys = look.keys()
    keys = filter(lambda key: look[key] != None, keys)
    if len(list(keys)) > 0:
        result = {
            "data": look,
            "occasion": occasion_id,
            "period": None,
            "timestamp": None,
            "season": None,
            "type": type
        }
        return result

# recursive
def generate_lookset_look_and_add_into_lookset2(
    clothes_by_category,
    occasion_ids,
    lookset, # array
    look_template,
    type,
    clothes=[],
    category_count=0 # zero-based index/counter
):
    for clothe_index, clothe in enumerate(clothes_by_category[category_count].get("clothes")): # para cada peça na categoria atual faça
        category = clothes_by_category[category_count]["category"].replace(' ', '')
        category = f"{category:012s}_clothe_index: {clothe_index}"
        print(f"{category}, category_count: {category_count}")
        clothes[category_count] = clothe
        next_clothes_by_category = get_by_index(clothes_by_category, category_count+1)
        if next_clothes_by_category and next_clothes_by_category.get("total_clothes") > 0: # se a próxima categoria tiver peças
            lookset = generate_lookset_look_and_add_into_lookset2(
                clothes_by_category, 
                occasion_ids, 
                lookset, 
                look_template, 
                type, 
                clothes,
                category_count+1
            )
        look = json.loads(json.dumps(look_template))
        for previous_clothe_index, previous_clothe in enumerate(clothes):
            look[clothes_by_category[previous_clothe_index]["category_id"]] = previous_clothe
        data = generate_lookset_look(lookset, look, type, "occasion_id")
        if data is not None:
            lookset.append(data)
        continue
    return lookset

# procedural
def generate_lookset_look_and_add_into_lookset3(
    clothes_by_category,
    occasion_ids,
    lookset,
    look_template,
    type
):
    for clothe_indexa, a in enumerate(clothes_by_category[0].get("clothes")):  # para cada peça na categoria 0 faça
        next_clothes_by_category = get_by_index(clothes_by_category, 1)
        category = clothes_by_category[0]["category"].replace(' ', '')
        category = f"{category:012s}_clothe_index: {clothe_indexa}"
        print(f"{category}, category_count: {0}")
        if not next_clothes_by_category or next_clothes_by_category.get("total_clothes") == 0: # se categoria 1 não tiver peças
            # for occasion_id in occasion_ids:  # para cada ocasião cadastrada na rotina semanal
            look = json.loads(json.dumps(look_template))
            # if occasion_id in a["occasions"]:
            look[clothes_by_category[0]["category_id"]] = a
            data = generate_lookset_look(lookset, look, type, "occasion_id")
            if data is not None:
                lookset.append(data)
            continue
        for clothe_indexb, b in enumerate(clothes_by_category[1].get("clothes")):
            next_clothes_by_category = get_by_index(clothes_by_category, 2)
            category = clothes_by_category[1]["category"].replace(' ', '')
            category = f"{category:012s}_clothe_index: {clothe_indexb}"
            print(f"{category}, category_count: {1}")
            if not next_clothes_by_category or next_clothes_by_category.get("total_clothes") == 0:
                # for occasion_id in occasion_ids:
                look = json.loads(json.dumps(look_template))
                # if occasion_id in a["occasions"]:
                look[clothes_by_category[0]["category_id"]] = a
                # if occasion_id in b["occasions"]:
                look[clothes_by_category[1]["category_id"]] = b
                data = generate_lookset_look(lookset, look, type, "occasion_id")
                if data is not None:
                    lookset.append(data)
                continue
            for clothe_indexc, c in enumerate(clothes_by_category[2].get("clothes")):
                next_clothes_by_category = get_by_index(clothes_by_category, 3)
                category = clothes_by_category[2]["category"].replace(' ', '')
                category = f"{category:012s}_clothe_index: {clothe_indexc}"
                print(f"{category}, category_count: {2}")
                if not next_clothes_by_category or next_clothes_by_category.get("total_clothes") == 0:
                    # for occasion_id in occasion_ids:
                    look = json.loads(json.dumps(look_template))
                    # if occasion_id in a["occasions"]:
                    look[clothes_by_category[0]["category_id"]] = a
                    # if occasion_id in b["occasions"]:
                    look[clothes_by_category[1]["category_id"]] = b
                    # if occasion_id in c["occasions"]:
                    look[clothes_by_category[2]["category_id"]] = c
                    data = generate_lookset_look(lookset, look, type, "occasion_id")
                    if data is not None:
                        lookset.append(data)
                    continue
                for clothe_indexd, d in enumerate(clothes_by_category[3].get("clothes")):
                    next_clothes_by_category = get_by_index(clothes_by_category, 4)
                    category = clothes_by_category[3]["category"].replace(' ', '')
                    category = f"{category:012s}_clothe_index: {clothe_indexd}"
                    print(f"{category}, category_count: {3}")
                    if not next_clothes_by_category or next_clothes_by_category.get("total_clothes") == 0:
                        # for occasion_id in occasion_ids:
                        look = json.loads(json.dumps(look_template))
                        # if occasion_id in a["occasions"]:
                        look[clothes_by_category[0]["category_id"]] = a
                        # if occasion_id in b["occasions"]:
                        look[clothes_by_category[1]["category_id"]] = b
                        # if occasion_id in c["occasions"]:
                        look[clothes_by_category[2]["category_id"]] = c
                        # if occasion_id in d["occasions"]:
                        look[clothes_by_category[3]["category_id"]] = d
                        data = generate_lookset_look(lookset, look, type, "occasion_id")
                        if data is not None:
                            lookset.append(data)
                        continue
                    for clothe_indexe, e in enumerate(clothes_by_category[4].get("clothes")):
                        next_clothes_by_category = get_by_index(clothes_by_category, 5)
                        category = clothes_by_category[4]["category"].replace(' ', '')
                        category = f"{category:012s}_clothe_index: {clothe_indexe}"
                        print(f"{category}, category_count: {4}")
                        if not next_clothes_by_category or next_clothes_by_category.get("total_clothes") == 0:
                            # for occasion_id in occasion_ids:
                            look = json.loads(json.dumps(look_template))
                            # if occasion_id in a["occasions"]:
                            look[clothes_by_category[0]["category_id"]] = a
                            # if occasion_id in b["occasions"]:
                            look[clothes_by_category[1]["category_id"]] = b
                            # if occasion_id in c["occasions"]:
                            look[clothes_by_category[2]["category_id"]] = c
                            # if occasion_id in d["occasions"]:
                            look[clothes_by_category[3]["category_id"]] = d
                            # if occasion_id in e["occasions"]:
                            look[clothes_by_category[4]["category_id"]] = e
                            data = generate_lookset_look(lookset, look, type, "occasion_id")
                            if data is not None:
                                lookset.append(data)
                            continue
                        for clothe_indexf, f in enumerate(clothes_by_category[5].get("clothes")):
                            next_clothes_by_category = get_by_index(clothes_by_category, 6)
                            category = clothes_by_category[5]["category"].replace(' ', '')
                            category = f"{category:012s}_clothe_index: {clothe_indexf}"
                            print(f"{category}, category_count: {5}")
                            if not next_clothes_by_category or next_clothes_by_category.get("total_clothes") == 0:
                                # for occasion_id in occasion_ids:
                                look = json.loads(json.dumps(look_template))
                                # if occasion_id in a["occasions"]:
                                look[clothes_by_category[0]["category_id"]] = a
                                # if occasion_id in b["occasions"]:
                                look[clothes_by_category[1]["category_id"]] = b
                                # if occasion_id in c["occasions"]:
                                look[clothes_by_category[2]["category_id"]] = c
                                # if occasion_id in d["occasions"]:
                                look[clothes_by_category[3]["category_id"]] = d
                                # if occasion_id in e["occasions"]:
                                look[clothes_by_category[4]["category_id"]] = e
                                # if occasion_id in f["occasions"]:
                                look[clothes_by_category[5]["category_id"]] = f
                                data = generate_lookset_look(lookset, look, type, "occasion_id")
                                if data is not None:
                                    lookset.append(data)
                                continue
                            for clothe_indexg, g in enumerate(clothes_by_category[6].get("clothes")):
                                next_clothes_by_category = get_by_index(clothes_by_category, 7)
                                category = clothes_by_category[6]["category"].replace(' ', '')
                                category = f"{category:012s}_clothe_index: {clothe_indexg}"
                                print(f"{category}, category_count: {6}")
                                if not next_clothes_by_category or next_clothes_by_category.get("total_clothes") == 0:
                                    # for occasion_id in occasion_ids:
                                    look = json.loads(json.dumps(look_template))
                                    # if occasion_id in a["occasions"]:
                                    look[clothes_by_category[0]["category_id"]] = a
                                    # if occasion_id in b["occasions"]:
                                    look[clothes_by_category[1]["category_id"]] = b
                                    # if occasion_id in c["occasions"]:
                                    look[clothes_by_category[2]["category_id"]] = c
                                    # if occasion_id in d["occasions"]:
                                    look[clothes_by_category[3]["category_id"]] = d
                                    # if occasion_id in e["occasions"]:
                                    look[clothes_by_category[4]["category_id"]] = e
                                    # if occasion_id in f["occasions"]:
                                    look[clothes_by_category[5]["category_id"]] = f
                                    # if occasion_id in g["occasions"]:
                                    look[clothes_by_category[6]["category_id"]] = g
                                    data = generate_lookset_look(lookset, look, type, "occasion_id")
                                    if data is not None:
                                        lookset.append(data)
                                    continue
                                for clothe_indexh, h in clothes_by_category[7].get("clothes"):
                                    next_clothes_by_category = get_by_index(clothes_by_category, 8)
                                    category = clothes_by_category[7]["category"].replace(' ', '')
                                    category = f"{category:012s}_clothe_index: {clothe_indexh}"
                                    print(f"{category}, category_count: {7}")
                                    if not next_clothes_by_category or next_clothes_by_category.get("total_clothes") == 0:
                                        # for occasion_id in occasion_ids:
                                        look = json.loads(json.dumps(look_template))
                                        # if occasion_id in a["occasions"]:
                                        look[clothes_by_category[0]["category_id"]] = a
                                        # if occasion_id in b["occasions"]:
                                        look[clothes_by_category[1]["category_id"]] = b
                                        # if occasion_id in c["occasions"]:
                                        look[clothes_by_category[2]["category_id"]] = c
                                        # if occasion_id in d["occasions"]:
                                        look[clothes_by_category[3]["category_id"]] = d
                                        # if occasion_id in e["occasions"]:
                                        look[clothes_by_category[4]["category_id"]] = e
                                        # if occasion_id in f["occasions"]:
                                        look[clothes_by_category[5]["category_id"]] = f
                                        # if occasion_id in g["occasions"]:
                                        look[clothes_by_category[6]["category_id"]] = g
                                        # if occasion_id in h["occasions"]:
                                        look[clothes_by_category[7]["category_id"]] = h
                                        data = generate_lookset_look(lookset, look, type, "occasion_id")
                                        if data is not None:
                                            lookset.append(data)
                                        continue
                                    for clothe_indexi, i in enumerate(clothes_by_category[8].get("clothes")):
                                        next_clothes_by_category = get_by_index(clothes_by_category, 9)
                                        category = clothes_by_category[8]["category"].replace(' ', '')
                                        category = f"{category:012s}_clothe_index: {clothe_indexi}"
                                        print(f"{category}, category_count: {8}")
                                        if not next_clothes_by_category or next_clothes_by_category.get("total_clothes") == 0:
                                            # for occasion_id in occasion_ids:
                                            look = json.loads(json.dumps(look_template))
                                            # if occasion_id in a["occasions"]:
                                            look[clothes_by_category[0]["category_id"]] = a
                                            # if occasion_id in b["occasions"]:
                                            look[clothes_by_category[1]["category_id"]] = b
                                            # if occasion_id in c["occasions"]:
                                            look[clothes_by_category[2]["category_id"]] = c
                                            # if occasion_id in d["occasions"]:
                                            look[clothes_by_category[3]["category_id"]] = d
                                            # if occasion_id in e["occasions"]:
                                            look[clothes_by_category[4]["category_id"]] = e
                                            # if occasion_id in f["occasions"]:
                                            look[clothes_by_category[5]["category_id"]] = f
                                            # if occasion_id in g["occasions"]:
                                            look[clothes_by_category[6]["category_id"]] = g
                                            # if occasion_id in h["occasions"]:
                                            look[clothes_by_category[7]["category_id"]] = h
                                            # if occasion_id in i["occasions"]:
                                            look[clothes_by_category[8]["category_id"]] = i
                                            data = generate_lookset_look(lookset, look, type, "occasion_id")
                                            if data is not None:
                                                lookset.append(data)
                                            continue
    return lookset


def generate_lookset(categories, fetch_clothes, daily_look_setup, type):
    lookset = []
    if len(categories) < 1 or len(fetch_clothes) < 1:
        return
    days_of_week = daily_look_setup.get("days_of_week")
    day_of_week_occasions = map(lambda day: day.get("occasions"), days_of_week)
    occasion_ids_map = map(lambda occasions: (
        map(lambda occasion: occasion.get("occasion_id"), occasions)), day_of_week_occasions)
    occasion_ids = reduce(lambda prev, curr: list(
        prev) + list(curr), occasion_ids_map, [])
    occasion_ids = set(occasion_ids)
    clothes_by_category = []
    for category in categories:
        category_id = category.get("_id")
        clothes = filter(lambda clothe: clothe.get(
            "category_id") == category_id, fetch_clothes)
        clothes = list(clothes)
        total_clothes = len(clothes)
        clothes_by_category.append({
            "category_id": category_id,
            "category": category.get("name"),
            "total_clothes": total_clothes,
            "clothes": clothes
        })
    clothes_by_category.sort(
        key=(lambda clothe: clothe["total_clothes"]), reverse=True)
    # se o primeiro estiver vazio os outros também estarão já que
    # está ordenado do maior para o menor
    if clothes_by_category[0].get("total_clothes") == 0:
        return
    category_ids = map(lambda category: category.get("_id"), categories)
    look_template = {}
    clothes = [] # recursive mode only
    for category_id in category_ids:
        look_template[category_id] = None
        clothes.append(None)  # recursive mode only
    print(f"clothes_by_category length: {len(clothes_by_category)}")
    lookset = generate_lookset_look_and_add_into_lookset3(
    # lookset = generate_lookset_look_and_add_into_lookset2( # recursive mode only
        clothes_by_category,
        occasion_ids,
        lookset,
        look_template,
        type
        # , clothes # recursive mode only
    )
    return lookset


response = generate_lookset(
    categories=categories,
    daily_look_setup=daily_look_setup,
    fetch_clothes=clothes,
    type=type
)
# Serializing json
json_object = json.dumps(response, indent=4)
# Writing to sample.json
# with open("recursive3.json", "w") as outfile:
with open("procedure3.json", "w") as outfile:
    outfile.write(json_object)
print(len(response))