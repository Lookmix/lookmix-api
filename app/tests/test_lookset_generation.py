import json
from functools import reduce

seasons = [
  "Primavera",
  "Verão",
  "Outono",
  "Inverno"
]
occasions = [
    {
        "_id": "6315604bdaf4e3d095035212",
        "name": "básico/comum",
        "card_look_title": "Look básico/comum",
        "type": "rotina",
        "tags": [
            "básico",
            "básica",
            "comum",
            "basic",
            "limpa",
            "lisa",
            "limpo",
            "liso",
            "neutro",
            "neutra"
        ]
    },
    {
        "_id": "6315604bdaf4e3d095035213",
        "name": "dia"
    },
    {
        "_id": "6315604bdaf4e3d095035214",
        "name": "noite"
    },
    {
        "_id": "6315604bdaf4e3d095035215",
        "name": "trabalho",
        "card_look_title": "Look para o trabalho",
        "type": "rotina",
        "tags": [
            "trabalho",
            "formal",
            "dress code",
            "uniforme"
        ]
    },
    {
        "_id": "6315604bdaf4e3d095035216",
        "name": "curso/faculdade",
        "card_look_title": "Look para curso/faculdade",
        "type": "rotina",
        "tags": [
            "curso",
            "faculdade",
            "escola",
            "universidade",
            "universitário",
            "universitária",
            "estudante",
            "colegial",
            "cursinho",
            "uniforme",
            "farda"
        ]
    },
    {
        "_id": "6315604bdaf4e3d095035217",
        "name": "festa/evento",
        "card_look_title": "Look para festa/evento",
        "type": "eventual",
        "tags": [
            "show",
            "música",
            "comemoração",
            "festa",
            "balada",
            "evento",
            "aniversário",
            "festival",
            "atração",
            "diversão"
        ]
    },
    {
        "_id": "6315604bdaf4e3d095035218",
        "name": "restaurante",
        "card_look_title": "Look para restaurante/bar",
        "type": "eventual",
        "tags": [
            "restaurante",
            "bar",
            "barzinho",
            "buteco",
            "gastronomia"
        ]
    },
    {
        "_id": "6315604bdaf4e3d095035219",
        "name": "shopping",
        "card_look_title": "Look para shopping/compras",
        "type": "eventual",
        "tags": [
            "shopping",
            "compras"
        ]
    },
    {
        "_id": "6315604bdaf4e3d09503521a",
        "name": "viagem",
        "card_look_title": "Look para viagem",
        "type": "eventual",
        "tags": [
            "viagem",
            "férias"
        ]
    },
    {
        "_id": "6315604bdaf4e3d09503521b",
        "name": "praia",
        "card_look_title": "Look para praia/piscina",
        "type": "eventual",
        "tags": [
            "praia",
            "piscina",
            "verão",
            "sol",
            "roupa de banho"
        ]
    },
    {
        "_id": "6315604bdaf4e3d09503521c",
        "name": "atividade física",
        "card_look_title": "Look para atividade física",
        "type": "rotina",
        "tags": [
            "exercício",
            "academia",
            "musculação",
            "esporte",
            "futebol",
            "corrida",
            "caminhada",
            "bicicleta",
            "esportivo",
            "malhar",
            "treino"
        ]
    },
    {
        "_id": "6315604bdaf4e3d09503521d",
        "name": "natureza",
        "card_look_title": "Look para natureza",
        "type": "eventual",
        "tags": [
            "sítio",
            "chácara",
            "natureza",
            "parque",
            "trilha",
            "jardim",
            "praça",
            "acampamento"
        ]
    },
    {
        "_id": "6315604bdaf4e3d09503521e",
        "name": "entretenimento urbano",
        "card_look_title": "Look para entretenimento urbano",
        "type": "eventual",
        "tags": [
            "cinema",
            "teatro",
            "estádio de futebol",
            "museu",
            "cultura",
            "arte"
        ]
    },
    {
        "_id": "6315604bdaf4e3d09503521f",
        "name": "encontro/date",
        "card_look_title": "Look para encontro/date",
        "type": "eventual",
        "tags": [
            "encontro",
            "date"
        ]
    },
    {
        "_id": "6315604bdaf4e3d095035220",
        "name": "prática religiosa",
        "card_look_title": "Look para prática religiosa",
        "type": "rotina",
        "tags": [
            "templo religioso",
            "religiso",
            "religisa"
        ]
    }
]
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
        "_id": "62c9c91d336080751568ceae",
        "category_id": "629d286bec74d540eb5fb0e7",
        "closet_id": "72177720299676310",
        "image": "https://live.staticflickr.com/65535/52204773396_8dcc9479d5_n.jpg",
        "occasions": [
            "6315604bdaf4e3d095035214",
            "6315604bdaf4e3d095035215",
            "6315604bdaf4e3d095035218",
            "6315604bdaf4e3d095035217",
            "6315604bdaf4e3d09503521a"
        ],
        "seasons": [
            "inverno",
            "outono"
        ],
        "type": "social"
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
        "_id": "62fc629e98e43430688253f9",
        "category_id": "629d286bec74d540eb5fb0ee",
        "closet_id": "72177720299676310",
        "image": "https://live.staticflickr.com/65535/52291448274_69f0ca273c_n.jpg",
        "occasions": [
            "6315604bdaf4e3d095035214",
            "6315604bdaf4e3d095035213",
            "6315604bdaf4e3d095035215",
            "6315604bdaf4e3d095035217",
            "6315604bdaf4e3d095035218",
            "6315604bdaf4e3d09503521a"
        ],
        "seasons": [
            "primavera",
            "verão",
            "inverno",
            "outono"
        ],
        "type": "social"
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
  "_id": "63d708d10eea647190f3cb7f",
  "days_of_week": [
    {
      "day_of_week": "domingo",
      "occasions": [
        {
          "casual": [
            "6315604bdaf4e3d095035213"
          ],
          "occasion_id": "6315604bdaf4e3d095035220",
          "social": [
            "6315604bdaf4e3d095035214"
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
            "6315604bdaf4e3d095035213"
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
            "6315604bdaf4e3d095035214"
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
            "6315604bdaf4e3d095035213"
          ],
          "occasion_id": "6315604bdaf4e3d095035212",
          "social": []
        },
        {
          "casual": [],
          "occasion_id": "6315604bdaf4e3d095035215",
          "social": [
            "6315604bdaf4e3d095035214"
          ]
        }
      ],
      "sort": 3
    },
    {
      "day_of_week": "quinta",
      "occasions": [
        {
          "casual": [
            "6315604bdaf4e3d095035213"
          ],
          "occasion_id": "6315604bdaf4e3d095035215",
          "social": []
        }
      ],
      "sort": 4
    },
    {
      "day_of_week": "sexta",
      "occasions": [
        {
          "casual": [
            "6315604bdaf4e3d095035213"
          ],
          "occasion_id": "6315604bdaf4e3d095035215",
          "social": []
        }
      ],
      "sort": 5
    },
    {
      "day_of_week": "sábado",
      "occasions": [
        {
          "casual": [
            "6315604bdaf4e3d095035213"
          ],
          "occasion_id": "6315604bdaf4e3d09503521c",
          "social": []
        }
      ],
      "sort": 6
    }
  ],
  "user_id": "6298301fed1909971532ca92"
}

type = "casual"

def get_look_count_by_day_of_week(casual=True):
    occasion_key = "casual"
    if not casual:
        occasion_key = "social"
    look_count_by_day_of_week = []
    days_of_week = daily_look_setup["days_of_week"]
    for day in days_of_week:
        daily_look_count = 0
        occasion_ids = []
        for occasion in day["occasions"]:
            daily_look_count += len(occasion[occasion_key])
            occasion_ids.append(occasion["occasion_id"])
        occasion_and_look_count_by_day_of_week = {
            "daily_look_count": daily_look_count,
            "occasion_ids": occasion_ids
        }
        look_count_by_day_of_week.append(occasion_and_look_count_by_day_of_week)
    return look_count_by_day_of_week


def get_occasions_from_daily_look_setup():
    days_of_week = daily_look_setup.get("days_of_week")
    day_of_week_occasions = map(lambda day: day.get("occasions"), days_of_week)
    occasion_ids_map = map(lambda occasions: (
        map(lambda occasion: occasion.get("occasion_id"), occasions)), day_of_week_occasions)
    occasion_ids = reduce(lambda prev, curr: list(
        prev) + list(curr), occasion_ids_map, [])
    occasion_ids = set(occasion_ids)
    return occasion_ids


def set_looks_ranking(looks):
    lookcount_by_day_of_week = get_look_count_by_day_of_week()
    ranking = 0
    result = []
    occasions = map(lambda look: look.get("occasion"), looks)
    occasions = set(occasions)
    looks_by_occasion = {}
    for occasion_id in occasions:
        looks_by_occasion[occasion_id] = list(filter(
            lambda look: look.get("occasion") == occasion_id,
        looks))
    while len(result) < len(looks):
        # print("lookcount_by_day_of_week", lookcount_by_day_of_week)
        for day_of_week in lookcount_by_day_of_week:
            # print("day_of_week.get('occasion_ids')", day_of_week.get("occasion_ids"))
            for occasion_id in day_of_week.get("occasion_ids"):
                if occasion_id not in occasions:
                    print(f"{occasion_id} not in {occasions}")
                    continue
                if len(looks_by_occasion[occasion_id]) < 1:
                    print(f"list of {occasion_id} has length {len(looks_by_occasion[occasion_id])} that is < 1")
                    continue
                # FAZ O POP DESSE ELEMENTO
                look = looks_by_occasion[occasion_id].pop(0)
                # ATRIBUI O VALOR DE RANKING NA CHAVE SORT
                look["sort"] = ranking
                #  ADICIONA EM RESULT
                result.append(look)
            ranking += 1
    # TODO: ORGANIZAR PELA TEMPERATURA/CLIMA DO DIA


    # LOOKSET 
    # CREATED_AT: 2022-01-22 23:25:10.456
    # DAYS_COUNT: 1 -> count days between created_at and today (not persistent)

    # - HOJE = DOM -> DAYS_COUNT = 1
    # - CONSULTA LOOKS NO DB COM O RANKING === 1
    # - RESULTADO RETORNADO DEVE REFLETIR A EXATA
    # QUANTIDADE DE LOOKS POR OCASIÃO, DEFINIDOS PARA 
    # O DIA DA SEMANA (DOM)
    return result


def get_by_index(array, index):
    try:
        return array[index]
    except IndexError as e:
        return False

def look_already_exist(lookset, look):
    lookset_stringfy = json.dumps(lookset)
    look_stringfy = json.dumps(look)
    if look_stringfy in lookset_stringfy:
        return True
    return False

def generate_lookset_look(lookset, look, type, occasion_id):
    if look_already_exist(lookset, look):
        return
    category_ids = look.keys()
    category_ids = list(filter(lambda category_id: look[category_id] != None, category_ids))
    if len(category_ids) > 1:
        seasons = reduce(lambda prev, curr_category_id: 
            list(prev) + list(look[curr_category_id].get("seasons")), category_ids, []
        )
        result = {
            "data": look,
            "occasion": occasion_id,
            "period": None, # day/night
            "sort": None,
            "season": seasons,
            "type": type
        }
        return result

# recursive
def generate_lookset_look_and_add_into_lookset2(
    clothes_by_category,
    occasion_id,
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
                occasion_id,
                lookset,
                look_template,
                type,
                clothes,
                category_count+1
            )
        look = json.loads(json.dumps(look_template))
        for previous_clothe_index, previous_clothe in enumerate(clothes):
            # if previous_clothe is not None and occasion_id not in previous_clothe["occasions"]:
            #     continue
            look[clothes_by_category[previous_clothe_index]["category_id"]] = previous_clothe
        data = generate_lookset_look(lookset, look, type, occasion_id)
        if data is not None:
            lookset.append(data)
        continue
    return lookset

# procedural
def generate_lookset_look_and_add_into_lookset3(
    clothes_by_category,
    occasion_id,
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
            data = generate_lookset_look(lookset, look, type, occasion_id)
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
                data = generate_lookset_look(lookset, look, type, occasion_id)
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
                    data = generate_lookset_look(lookset, look, type, occasion_id)
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
                        data = generate_lookset_look(lookset, look, type, occasion_id)
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
                            data = generate_lookset_look(lookset, look, type, occasion_id)
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
                                data = generate_lookset_look(lookset, look, type, occasion_id)
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
                                    data = generate_lookset_look(lookset, look, type, occasion_id)
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
                                        data = generate_lookset_look(lookset, look, type, occasion_id)
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
                                            data = generate_lookset_look(lookset, look, type, occasion_id)
                                            if data is not None:
                                                lookset.append(data)
                                            continue
    return lookset


def generate_lookset(categories, fetch_clothes, type, occasion_id):
    if len(categories) < 1 or len(fetch_clothes) < 1:
        return
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
    # lookset = generate_lookset_look_and_add_into_lookset3(
    lookset = generate_lookset_look_and_add_into_lookset2( # recursive mode only
        clothes_by_category,
        occasion_id,
        [], # lookset
        look_template,
        type
        , clothes # recursive mode only
    )
    return lookset

response = []
occasion_ids = get_occasions_from_daily_look_setup()
print(occasion_ids)
for occasion_id in occasion_ids:
    clothes_by_occasion = filter(
        lambda clothe: occasion_id in clothe.get("occasions"), 
    clothes)
    clothes_by_occasion = list(clothes_by_occasion)
    print(f"----------- clothes_by_occasion {occasion_id}: ", len(clothes_by_occasion))
    if len(clothes_by_occasion) < 1:
        continue
    for season in seasons:
        clothes_by_season = filter(
            lambda clothe: season.lower() in clothe.get("seasons"), 
        clothes_by_occasion)
        clothes_by_season = list(clothes_by_season)
        print("clothes by season:", len(clothes_by_season))
        result = generate_lookset(
            categories=categories,
            fetch_clothes=clothes_by_season,
            type=type,
            occasion_id=occasion_id
        )
        for look in result:
            if look_already_exist(response, look):
                continue
            response.append(look)

response = set_looks_ranking(response)
# Serializing json
json_object = json.dumps(response, indent=4)
# Writing to sample.json
with open("recursive4.json", "w") as outfile:
# with open("procedure4.json", "w") as outfile:
    outfile.write(json_object)
print(len(response))