class SteamGame:
    def __init__(self, id, developers=[], tags=[], release_year=None):
        self.id: int = id
        self.developers: list[str] = developers
        self.tags: list[str] = tags
        self.release_year: str = release_year
    
    def get_wordcloud_str(self):
        ret = []
        ret.extend(self.developers)
        ret.extend(self.tags)
        if self.release_year: ret.append(self.release_year)
        ret = [x.replace(' ', '') for x in ret]
        return ' '.join(ret)