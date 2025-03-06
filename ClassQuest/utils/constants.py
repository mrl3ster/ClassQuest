import random

BADGE_IMAGES = [
    "https://images.unsplash.com/photo-1548126466-4470dfd3a209",
    "https://images.unsplash.com/photo-1571008840902-28bf8f9cd71a",
    "https://images.unsplash.com/photo-1571008592377-e362723e8998",
    "https://images.unsplash.com/photo-1552035509-b247fe8e5078",
    "https://images.unsplash.com/photo-1548051718-3acad2d13740"
]

# Sci-fi themed SVG avatars
AVATAR_IMAGES = [
    '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <circle cx="50" cy="50" r="45" fill="#0a0f2c" stroke="#00ff9f" stroke-width="2"/>
        <path d="M50 20 L30 70 L70 70 Z" fill="none" stroke="#00ff9f" stroke-width="2"/>
        <circle cx="50" cy="45" r="10" fill="#00ff9f"/>
    </svg>''',  # Alien Glyph - Neon Green

    '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <rect x="10" y="30" width="80" height="40" fill="#0a0f2c" stroke="#00f7ff" stroke-width="2"/>
        <circle cx="50" cy="50" r="15" fill="none" stroke="#00f7ff" stroke-width="2"/>
        <path d="M20 50 L40 50 M60 50 L80 50" stroke="#00f7ff" stroke-width="2"/>
    </svg>''',  # Space Station - Neon Blue

    '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <path d="M50 10 L90 90 L50 70 L10 90 Z" fill="#0a0f2c" stroke="#b400ff" stroke-width="2"/>
        <circle cx="50" cy="40" r="10" fill="#b400ff"/>
    </svg>''',  # Starship - Neon Purple

    '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <circle cx="50" cy="50" r="40" fill="#0a0f2c" stroke="#ff9100" stroke-width="2"/>
        <path d="M30 30 L70 70 M70 30 L30 70" stroke="#ff9100" stroke-width="2"/>
        <circle cx="50" cy="50" r="10" fill="#ff9100"/>
    </svg>''',  # Quantum Symbol - Neon Orange

    '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <polygon points="50,10 90,40 90,60 50,90 10,60 10,40" fill="#0a0f2c" stroke="#ff00e4" stroke-width="2"/>
        <circle cx="50" cy="50" r="15" fill="none" stroke="#ff00e4" stroke-width="2"/>
        <circle cx="50" cy="50" r="5" fill="#ff00e4"/>
    </svg>'''  # Cyber Hexagon - Neon Pink
]

# Card pack definitions
CARD_PACKS = {
    "basic": {
        "name": "Basic Pack",
        "description": "A standard pack with a mix of cards. Contains 3 cards.",
        "price": 50,
        "cards_per_pack": 3,
        "probabilities": {
            "Common": 70,
            "Uncommon": 20,
            "Rare": 8,
            "Epic": 2,
            "Legendary": 0
        }
    },
    "premium": {
        "name": "Premium Pack",
        "description": "Higher chance of rare cards. Contains 4 cards with at least 1 Rare or better.",
        "price": 150,
        "cards_per_pack": 4,
        "probabilities": {
            "Common": 40,
            "Uncommon": 35,
            "Rare": 15,
            "Epic": 8,
            "Legendary": 2
        },
        "guaranteed": ["Rare", "Epic", "Legendary"]
    },
    "ultimate": {
        "name": "Ultimate Pack",
        "description": "The best pack available! Contains 5 cards with guaranteed Epic and high chance of Legendary.",
        "price": 300,
        "cards_per_pack": 5,
        "probabilities": {
            "Common": 20,
            "Uncommon": 30,
            "Rare": 25,
            "Epic": 15,
            "Legendary": 10
        },
        "guaranteed": ["Epic", "Legendary"]
    }
}

DEFAULT_STATS = {
    "gold": 0,
    "xp": 0,
    "hp": 100,
    "level": 1,
    "avatar_url": AVATAR_IMAGES[0]  # Default avatar is the Alien Glyph
}