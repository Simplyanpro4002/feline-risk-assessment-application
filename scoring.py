def get_question_score(question_id, answer):
    """
    Get the score for a specific question based on the answer provided
    """
    scoring_map = {
        1: {'a': 4, 'b': 3, 'c': 2, 'd': 1},  # Q1
        2: {'a': 1, 'b': 2, 'c': 3, 'd': 4},  # Q2
        3: {'a': 1, 'b': 2, 'c': 3, 'd': 4},  # Q3
        4: {'a': 1, 'b': 2, 'c': 3},          # Q4
        5: {'a': 1, 'b': 2, 'c': 3},          # Q5
        6: {'a': 1, 'b': 2, 'c': 3, 'd': 4},  # Q6
        7: {'a': 1, 'b': 2, 'c': 3, 'd': 4},  # Q7
        8: {'a': 1, 'b': 2, 'c': 3, 'd': 4},  # Q8
        9: {'a': 1, 'b': 3},                   # Q9
        10: {'a': 1, 'b': 3},                  # Q10
        11: {'a': 1, 'b': 2, 'c': 3, 'd': 4}, # Q11
        12: {'a': 1, 'b': 2, 'c': 3},         # Q12
        13: {'a': 1, 'b': 2, 'c': 3, 'd': 4}, # Q13
        14: {'a': 1, 'b': 2, 'c': 3, 'd': 4}, # Q14
        15: {'a': 4, 'b': 3, 'c': 2, 'd': 1}  # Q15
    }
    
    return scoring_map[question_id].get(answer.lower(), 0)

def calculate_raw_score(answers):
    """
    Calculate the raw score from all answers
    """
    total_score = 0
    for question_id, answer in answers.items():
        total_score += get_question_score(int(question_id), answer)
    return total_score

def calculate_standard_score(raw_score):
    """
    Convert raw score to standard score (0-100)
    Formula: ((User Total Score - 15) / (55 - 15)) × 100
    """
    return ((raw_score - 15) / (55 - 15)) * 100

def get_risk_profile(standard_score):
    """
    Get risk profile based on standard score with cat-themed descriptions
    """
    if standard_score < 25:
        return {
            'group': 1,
            'name': 'The Safety Seeker',
            'cat_type': 'Whiskers the Worrier',
            'core_traits': [
                'Views risk as danger',
                'Needs security, dislikes uncertainty',
                'Strongly loss-averse and avoids change',
                'Always chooses the safest portfolio option'
            ],
            'personality': "A cautious and conservative heir. Whiskers buries savings like they're catnip stashes and never takes chances with Grandma's fortune."
        }
    elif standard_score < 35:
        return {
            'group': 2,
            'name': 'The Cautious Climber',
            'cat_type': 'Tabby the Traditionalist',
            'core_traits': [
                'Dislikes risk, but not to the extreme',
                'Prioritizes stability with cautious optimism',
                'Avoids big changes unless necessary',
                'Would rather pounce than leap'
            ],
            'personality': 'Tabby is slightly braver than Whiskers but still prefers a calm investment nap over a speculative chase.'
        }
    elif standard_score < 45:
        return {
            'group': 3,
            'name': 'The Measured Mouser',
            'cat_type': 'Simba the Strategist',
            'core_traits': [
                'Balances caution with growth',
                'Mildly risk-tolerant but very aware of losses',
                'Prefers tested methods, open to small experiments'
            ],
            'personality': 'Simba will stalk an opportunity carefully before making a move - patient, but not paralyzed.'
        }
    elif standard_score < 55:
        return {
            'group': 4,
            'name': 'The Balanced Beast',
            'cat_type': 'Luna the Level-Headed',
            'core_traits': [
                'Moderate risk-taker',
                'Optimistic, adaptable, prefers practical choices',
                'Neither too adventurous nor too reserved'
            ],
            'personality': "Luna is Grandma's favorite middle kitten - bold enough to grow, calm enough to preserve."
        }
    elif standard_score < 65:
        return {
            'group': 5,
            'name': 'The Opportunistic Observer',
            'cat_type': 'Felix the Forecast Feline',
            'core_traits': [
                'Sees risk as a potential reward',
                'Confident and future-focused',
                'Mixes safety with ambition'
            ],
            'personality': 'Felix is the cool cat at the investor lounge, always tracking the next hot trend - but with a safety net.'
        }
    elif standard_score < 75:
        return {
            'group': 6,
            'name': 'The Bold Beneficiary',
            'cat_type': 'Juno the Jackpot Hunter',
            'core_traits': [
                'Enjoys high-risk, high-reward scenarios',
                'Thinks fast, acts faster',
                'Believes discomfort is part of growth'
            ],
            'personality': "Juno's scratching post is the stock market. Grandma trusted them to shake up the family tree."
        }
    else:
        return {
            'group': 7,
            'name': 'The Risk Royalty',
            'cat_type': 'Leo the Legendary',
            'core_traits': [
                'Extreme confidence, thrives on volatility',
                'Values purchasing power over stability',
                'Expects high returns and strategizes aggressively'
            ],
            'personality': "Leo's idea of fun is market turbulence. The favorite to turn Grandma's fortune into an empire - or a meme stock."
        } 