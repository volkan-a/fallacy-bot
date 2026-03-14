from datetime import datetime
from scripts.data_manager import DataManager

test_post = {
    'id': '123',
    'title': 'Test',
    'content': 'Test content',
    'url': 'http',
    'author': 'me',
    'score': 100,
    'created_utc': 123456789,
    'subreddit': 'test',
    'analysis': {
        'has_fallacy': True,
        'fallacy_type': 'Ad Hominem',
        'confidence': 0.9,
        'confidence_level': 'High',
        'explanation': 'test',
        'quote': 'test'
    }
}

dm = DataManager(data_dir="data/test_dm")
dm.add_entries([test_post])
print(dm.get_entries()[0])
