# Skilander HiScore API

(c) Hiihtoliitto 2024

## Install

Modify `docker-compose.yaml` to your liking and
run `docker compose up -d` 

## Usage

Fairly simple API

### GET /*level*

Returns 10 best scores to level. Level is value from 0 to 4

### GET /all

Return 10 best scores for all levels

### POST /*level*/submit
Body application/json:

```
[ 1, 0.000000, 0.000000, "SPK" ]
```

Table consist of user_id, time, collectibles percentage, initials.

### POST /*user_id*/hiscores
Body application/json:
```
[                                                               # full score list
    [                                                           # level 0
        [                                                       # a score
            user_id, time, collectibles percentage, initials
        ]
    ]
]
```